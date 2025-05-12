import json
import logging
import os
import tarfile
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from eth_account import Account
from eth_account.types import PrivateKeyType
from eth_typing import ChecksumAddress
from impulse.contracts_client.constants import DEFAULT_IMPULSE_DIR
from impulse.contracts_client.error_handler import ErrorHandler
from impulse.contracts_client.event_handler import EventHandler
from web3 import Web3
from web3.contract import Contract
from web3.exceptions import ContractLogicError

from impulse.contracts_client.utils import tar_filter


def load_contract_artifacts(addresses_path: str = './addresses.json', abis_dir: Optional[str] = None) \
        -> Tuple[Dict[str, ChecksumAddress], str]:
    # Load contract addresses
    if not os.path.isfile(addresses_path):
        addresses_path = os.path.expanduser(f'{DEFAULT_IMPULSE_DIR}/addresses.json')
        # Download addresses.json and save to ~/.impulse/addresses.json
        os.makedirs(os.path.dirname(addresses_path), exist_ok=True)
        url = 'https://storage.googleapis.com/imp-artifacts/addresses.json'
        response = requests.get(url)
        response.raise_for_status()
        with open(addresses_path, 'w') as f:
            f.write(response.text)
    with open(addresses_path) as f:
        contracts_addresses = json.load(f)

    # Load contract ABIs
    abis_dir = abis_dir or os.path.expanduser(os.getenv('CC_ABIS_DIR', f'{DEFAULT_IMPULSE_DIR}/abis'))
    if os.path.isdir(abis_dir) and abis_dir.endswith('out'):  # Local Foundry output directory, local env
        return contracts_addresses, abis_dir
    # Download ABIs and save to ~/.impulse/abis
    os.makedirs(abis_dir, exist_ok=True)
    url = 'https://storage.googleapis.com/imp-artifacts/abis.tar.gz'
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with tempfile.NamedTemporaryFile() as temp_file:
        for chunk in response.iter_content(chunk_size=8192):
            temp_file.write(chunk)
        temp_file.flush()
        with tarfile.open(temp_file.name, 'r:gz') as tar:
            tar.extractall(path=os.path.dirname(abis_dir), filter=tar_filter)

    return contracts_addresses, abis_dir


@dataclass
class ImpulseConfig:
    """Configuration for Impulse SDK"""
    web3_provider: str
    private_key: PrivateKeyType
    contract_addresses: Dict[str, ChecksumAddress]
    abis_dir: str


class ImpulseError(Exception):
    """Base exception for Impulse SDK"""
    pass


class ContractError(ImpulseError):
    """Exception for contract-related errors"""
    pass


class ImpulseClient:
    """SDK for interacting with Impulse contracts"""

    def __init__(self, config: ImpulseConfig, logger: Optional[logging.Logger] = None):
        """Initialize the Impulse SDK"""
        self.config = config
        self.logger = logger or logging.getLogger("ImpulseSDK")

        # Initialize Web3 and account
        self.w3 = Web3(Web3.HTTPProvider(config.web3_provider))
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to {config.web3_provider}")

        # Initialize handlers (pass the web3_provider to EventHandler)
        self.error_handler = ErrorHandler()
        self.event_handler = EventHandler(self.logger, config.web3_provider)

        self.account = Account.from_key(config.private_key)
        self.address = self.account.address

        # Load ABIs and initialize contracts
        self.abis = self._load_abis(config.abis_dir)
        self._init_contracts(config.contract_addresses)

    def _load_abis(self, abis_dir: str) -> Dict[str, dict]:
        """Load contract ABIs from Foundry output directory"""
        abis = {}
        out_dir = Path(abis_dir)

        if not out_dir.exists():
            raise FileNotFoundError(
                f"Foundry output directory not found at {out_dir}. "
                "Please run 'forge build' first."
            )

        for file_path in out_dir.rglob('*.json'):
            contract_name = file_path.parent.stem.replace('.sol', '')
            if contract_name.endswith('.t'):
                continue

            try:
                contract_data = json.loads(file_path.read_text())
                if 'abi' in contract_data:
                    abis[contract_name] = contract_data['abi']
                    self.logger.debug(f"Loaded ABI for {contract_name}")
            except Exception as e:
                self.logger.warning(f"Failed to load ABI from {file_path}: {e}")

        if not abis:
            raise ValueError(
                f"No ABIs found in Foundry output directory: {out_dir}. "
                f"Please ensure contracts are compiled with 'forge build'."
            )

        return abis

    def _init_contracts(self, contract_addresses: Dict[str, ChecksumAddress]) -> None:
        """Initialize all contract interfaces"""
        try:
            self.access_manager = self._init_contract('AccessManager', contract_addresses)
            self.whitelist_manager = self._init_contract('WhitelistManager', contract_addresses)
            self.token = self._init_contract('ImpulseToken', contract_addresses)
            self.incentive_manager = self._init_contract('IncentiveManager', contract_addresses)
            self.node_manager = self._init_contract('NodeManager', contract_addresses)
            self.node_escrow = self._init_contract('NodeEscrow', contract_addresses)
            self.leader_manager = self._init_contract('LeaderManager', contract_addresses)
            self.job_manager = self._init_contract('JobManager', contract_addresses)
            self.job_escrow = self._init_contract('JobEscrow', contract_addresses)
            self.epoch_manager = self._init_contract('EpochManager', contract_addresses)
        except Exception as e:
            raise ContractError(f"Failed to initialize contracts: {e}")

    def _init_contract(self, name: str, addresses: Dict[str, ChecksumAddress]) -> Contract:
        """Initialize a single contract"""
        address = addresses[name]
        abi = self.abis[name]
        return self.w3.eth.contract(address=address, abi=abi)

    def _send_transaction(self, contract_function) -> dict:
        """Retry sending a transaction and waiting for receipt"""
        for i in range(3):
            r = self._send_transaction_inner(contract_function)
            if not isinstance(r, Exception):
                return r
            time.sleep(1)
        raise ContractError(f"Failed to send transaction: {r}")

    def _send_transaction_inner(self, contract_function) -> dict | Exception:
        """Helper to send a transaction and wait for receipt"""
        try:
            tx = contract_function.build_transaction({
                'from': self.address,
                'nonce': self.w3.eth.get_transaction_count(self.address),
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return receipt
        except ContractLogicError as e:
            error_message = self.error_handler.decode_contract_error(e)
            raise ContractError(f"Contract error: {error_message}")
        except Exception as e:
            return e

    # Token functions
    def approve_token_spending(self, spender: ChecksumAddress, amount: int) -> dict:
        """Approve token spending"""
        return self._send_transaction(
            self.token.functions.approve(spender, amount)
        )

    def get_token_balance(self, address: ChecksumAddress) -> int:
        """Get token balance for address"""
        return self.token.functions.balanceOf(address).call()

    # Node Escrow functions
    def deposit_stake(self, amount: int) -> dict:
        """Deposit stake into NodeEscrow"""
        return self._send_transaction(
            self.node_escrow.functions.deposit(amount)
        )

    def get_stake_balance(self, address: ChecksumAddress) -> int:
        """Get stake balance for address"""
        return self.node_escrow.functions.getBalance(address).call()

    def request_withdraw(self, amount: int) -> dict:
        """Request withdrawal from NodeEscrow"""
        return self._send_transaction(
            self.node_escrow.functions.requestWithdraw(amount)
        )

    def cancel_withdraw(self) -> dict:
        """Cancel pending withdrawal request"""
        return self._send_transaction(
            self.node_escrow.functions.cancelWithdraw()
        )

    def withdraw(self) -> dict:
        """Execute withdrawal after lock period"""
        return self._send_transaction(
            self.node_escrow.functions.withdraw()
        )

    # Node Manager functions
    def register_node(self, compute_rating: int) -> dict:
        """Register node with given compute rating"""
        return self._send_transaction(
            self.node_manager.functions.registerNode(compute_rating)
        )

    def unregister_node(self, node_id: int) -> dict:
        """Unregister an existing node"""
        return self._send_transaction(
            self.node_manager.functions.unregisterNode(node_id)
        )

    def get_node_info(self, node_id: int) -> tuple:
        """Get node information"""
        return self.node_manager.functions.getNodeInfo(node_id).call()

    def get_nodes_in_pool(self, pool_id: int) -> List[int]:
        """Get list of nodes in a specific pool"""
        return self.node_manager.functions.getNodesInPool(pool_id).call()

    def get_node_owner(self, node_id: int) -> str:
        """Get the owner address of a node"""
        return self.node_manager.functions.getNodeOwner(node_id).call()

    def get_stake_requirement(self, address: ChecksumAddress) -> int:
        """Get stake requirement for an address"""
        return self.node_manager.functions.getStakeRequirement(address).call()
    
    def request_withdrawal_from_job_escrow(self, amount: int) -> dict:
        """Request withdrawal from JobEscrow"""
        return self._send_transaction(
            self.job_escrow.functions.requestWithdraw(amount)
        )

    def cancel_withdraw_from_job_escrow(self) -> dict:
        """Cancel pending withdrawal request from JobEscrow"""
        return self._send_transaction(
            self.job_escrow.functions.cancelWithdraw()
        )

    def withdraw_from_job_escrow(self) -> dict:
        """Execute withdrawal from JobEscrow after lock period"""
        return self._send_transaction(
            self.job_escrow.functions.withdraw()
        )

    def get_withdraw_request_job_escrow(self, address: ChecksumAddress) -> tuple:
        """Get withdrawal request details from JobEscrow"""
        return self.job_escrow.functions.withdrawRequests(address).call()

    def get_withdraw_request_node_escrow(self, address: ChecksumAddress) -> tuple:
        """Get withdrawal request details from NodeEscrow"""
        return self.node_escrow.functions.withdrawRequests(address).call()

    # Epoch Manager functions
    def get_current_epoch(self) -> int:
        """Get current epoch number"""
        return self.epoch_manager.functions.getCurrentEpoch().call()

    def get_epoch_state(self) -> Tuple[int, int]:
        """Get current epoch state and time remaining"""
        if self.config.web3_provider.startswith('http://'):  # local env
            self._send_transaction(self.epoch_manager.functions.upTestCounter())
        return self.epoch_manager.functions.getEpochState().call()

    # Leader Manager functions
    def submit_commitment(self, node_id: int, commitment: bytes) -> dict:
        """Submit commitment for current epoch"""
        return self._send_transaction(
            self.leader_manager.functions.submitCommitment(node_id, commitment)
        )

    def reveal_secret(self, node_id: int, secret: bytes) -> dict:
        """Reveal secret for current epoch"""
        return self._send_transaction(
            self.leader_manager.functions.revealSecret(node_id, secret)
        )

    def elect_leader(self) -> dict:
        """Trigger leader election"""
        return self._send_transaction(
            self.leader_manager.functions.electLeader()
        )

    def get_current_leader(self) -> int:
        """Get current leader node ID"""
        return self.leader_manager.functions.getCurrentLeader().call()

    def get_leader_for_epoch(self, epoch: int) -> int:
        """Get leader node ID for an epoch"""
        return self.leader_manager.functions.getLeaderForEpoch(epoch).call()

    def get_final_random_value(self, epoch: int) -> bytes:
        """Get final random value for an epoch"""
        return self.leader_manager.functions.getFinalRandomValue(epoch).call()

    def get_nodes_who_revealed(self, epoch: int) -> List[int]:
        """Get list of nodes that revealed for an epoch"""
        return self.leader_manager.functions.getNodesWhoRevealed(epoch).call()

    # Job Manager functions
    def submit_job(self, args: str, model_name: str, ft_type: str) -> dict:
        """Submit a new job"""
        return self._send_transaction(
            self.job_manager.functions.submitJob(args, model_name, ft_type)
        )

    def start_assignment_round(self) -> dict:
        """Start job assignment round"""
        return self._send_transaction(
            self.job_manager.functions.startAssignmentRound()
        )

    def set_token_count_for_job(self, job_id: int, token_count: int) -> dict:
        """Set token count for a job"""
        return self._send_transaction(
            self.job_manager.functions.setTokenCountForJob(job_id, token_count)
        )

    def confirm_job(self, job_id: int) -> dict:
        """Confirm assigned job"""
        return self._send_transaction(
            self.job_manager.functions.confirmJob(job_id)
        )

    def complete_job(self, job_id: int) -> dict:
        """Mark job as complete"""
        return self._send_transaction(
            self.job_manager.functions.completeJob(job_id)
        )

    def fail_job(self, job_id: int, reason: str) -> dict:
        """Fail an assigned job"""
        return self._send_transaction(
            self.job_manager.functions.failJob(job_id, reason)
        )

    def process_job_payment(self, job_id: int) -> dict:
        """Process payment for completed job"""
        return self._send_transaction(
            self.job_manager.functions.processPayment(job_id)
        )

    def get_jobs_by_node(self, node_id: int) -> List[dict]:
        """Get detailed job information for a node"""
        jobs = self.job_manager.functions.getJobsDetailsByNode(node_id).call()
        return [{"id": j[0], "submitter": j[1], "assignedNode": j[2], "status": j[3],
                 "requiredPool": j[4], "args": j[5], "baseModelName": j[6],
                 "ftType": j[7], "numGpus": j[8],
                 "tokenCount": j[7], "createdAt": j[8]} for j in jobs]

    def get_assigned_node(self, job_id: int) -> int:
        """Get node assigned to a job"""
        return self.job_manager.functions.getAssignedNode(job_id).call()

    def get_job_status(self, job_id: int) -> int:
        """Get the status of a job"""
        return self.job_manager.functions.getJobStatus(job_id).call()

    def get_job_details(self, job_id: int) -> tuple:
        """Get detailed information about a job"""
        return self.job_manager.functions.getJobDetails(job_id).call()

    def get_jobs_by_submitter(self, submitter: ChecksumAddress) -> List[int]:
        """Get all job IDs submitted by an address"""
        return self.job_manager.functions.getJobsBySubmitter(submitter).call()

    # Job Escrow functions
    def deposit_job_funds(self, amount: int) -> dict:
        """Deposit funds into JobEscrow"""
        return self._send_transaction(
            self.job_escrow.functions.deposit(amount)
        )

    def get_job_escrow_balance(self, address: ChecksumAddress) -> int:
        """Get JobEscrow balance for address"""
        return self.job_escrow.functions.getBalance(address).call()
    
    # Whitelist Manager functions
    def add_cp(self, cp_address: ChecksumAddress) -> dict:
        """Add a computing provider to whitelist"""
        return self._send_transaction(
            self.whitelist_manager.functions.addCP(cp_address)
        )

    def remove_cp(self, cp_address: ChecksumAddress) -> dict:
        """Remove a computing provider from whitelist"""
        return self._send_transaction(
            self.whitelist_manager.functions.removeCP(cp_address)
        )

    def is_whitelisted(self, cp_address: ChecksumAddress) -> bool:
        """Check if address is whitelisted"""
        try:
            self.whitelist_manager.functions.requireWhitelisted(cp_address).call()
            return True
        except ContractLogicError:
            return False

    # Incentive Manager functions
    def process_incentives(self) -> dict:
        """Process incentives for current epoch"""
        return self._send_transaction(
            self.incentive_manager.functions.processAll()
        )

    # Event monitoring methods
    def setup_event_filters(self) -> None:
        """Set up filters for all relevant contract events"""
        contracts = {
            'AccessManager': self.access_manager,
            'WhitelistManager': self.whitelist_manager,
            'ImpulseToken': self.token,
            'IncentiveManager': self.incentive_manager,
            'NodeManager': self.node_manager,
            'NodeEscrow': self.node_escrow,
            'LeaderManager': self.leader_manager,
            'JobManager': self.job_manager,
            'JobEscrow': self.job_escrow
        }
        from_block = self.w3.eth.block_number
        self.event_handler.setup_event_filters(contracts, from_block)

    def process_events(self) -> None:
        """Process any new events from all filters"""
        self.event_handler.process_events()
