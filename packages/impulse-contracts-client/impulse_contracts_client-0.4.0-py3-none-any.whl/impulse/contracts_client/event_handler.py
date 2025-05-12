import logging
from typing import Dict, List, Tuple
from urllib.parse import urlparse

from web3 import Web3
from web3.contract import Contract


class EventHandler:
    """Handles contract event processing and logging"""

    def __init__(self, logger: logging.Logger, web3_provider: str = None):
        self.logger = logger
        self.event_filters: Dict[Tuple[str, str], any] = {}  # (contract_address, event_name) -> filter
        self.w3 = None  # Will be set when filters are created

        # Determine if we should use filters based on provider URL
        self.use_filters = False
        if web3_provider:
            try:
                parsed_url = urlparse(web3_provider)
                # Only enable filters for localhost connections
                if parsed_url.hostname in ('localhost', '127.0.0.1') or \
                   (parsed_url.port and parsed_url.port == 8545):
                    self.use_filters = True
                    self.logger.info("Using localhost RPC, event filters enabled")
                else:
                    self.logger.info("Non-localhost RPC, event filters disabled")
            except Exception as e:
                self.logger.warning(f"Could not parse RPC URL, disabling filters: {e}")

        # Define contract event mappings
        self.contract_events = {
            'AccessManager': [
                'RoleGranted',
                'RoleRevoked'
            ],
            'NodeManager': [
                'NodeRegistered',
                'NodeUnregistered',
                'NodeUpdated',
                'StakeValidated',
                'StakeRequirementUpdated'
            ],
            'LeaderManager': [
                'CommitSubmitted',
                'SecretRevealed',
                'LeaderElected'
            ],
            'JobManager': [
                'JobSubmitted',
                'JobStatusUpdated',
                'JobAssigned',
                'AssignmentRoundStarted',
                'JobConfirmed',
                'JobCompleted',
                'JobFailed',
                'PaymentProcessed'
            ],
            'NodeEscrow': [
                'Deposited',
                'WithdrawRequested',
                'WithdrawCancelled',
                'Withdrawn',
                'PenaltyApplied',
                'SlashApplied',
                'RewardApplied'
            ],
            'JobEscrow': [
                'Deposited',
                'WithdrawRequested',
                'WithdrawCancelled',
                'Withdrawn',
                'PaymentReleased'
            ],
            'WhitelistManager': [
                'CPAdded',
                'CPRemoved'
            ],
            'ImpulseToken': [
                'Transfer',
                'Approval'
            ],
            'IncentiveManager': [
                'LeaderRewardApplied',
                'JobAvailabilityRewardApplied',
                'DisputerRewardApplied',
                'LeaderNotExecutedPenaltyApplied',
                'JobNotConfirmedPenaltyApplied'
            ]
        }

    def setup_event_filters(self, contracts: Dict[str, Contract], from_block: int) -> None:
        """Set up filters for all contract events

        Args:
            contracts: Dictionary mapping contract names to Contract objects
            from_block: Block number to start filtering from
        """
        if not self.use_filters:
            self.logger.info("Event filters disabled, skipping setup")
            return

        # Store the web3 instance from one of the contracts for cleanup
        if contracts and list(contracts.values()):
            first_contract = list(contracts.values())[0]
            self.w3 = first_contract.web3

        # Clean up any existing filters
        self.cleanup_filters()

        # Create new filters
        for contract_name, contract in contracts.items():
            if contract_name in self.contract_events:
                self._create_event_filters(
                    contract,
                    self.contract_events[contract_name],
                    from_block
                )

    def create_event_filter(self, contract: Contract, event_name: str, from_block: int) -> None:
        """Create a new event filter for a specific contract event"""
        if not self.use_filters:
            return

        event = getattr(contract.events, event_name)
        try:
            event_filter = event.create_filter(from_block=from_block)
            self.event_filters[(contract.address, event_name)] = event_filter
            self.logger.info(f"Created filter for {event_name} events from block {from_block}")
        except Exception as e:
            self.logger.error(f"Failed to create filter for {event_name}: {e}")

    def _create_event_filters(self, contract: Contract, event_names: List[str], from_block: int) -> None:
        """Create filters for multiple events from a contract"""
        for event_name in event_names:
            self.create_event_filter(contract, event_name, from_block)

    def process_events(self) -> None:
        """Process all pending events from all filters"""
        if not self.use_filters or not self.event_filters:
            return

        expired_filters = []

        for (contract_address, event_name), event_filter in list(self.event_filters.items()):
            try:
                for event in event_filter.get_new_entries():
                    self._log_event(event_name, event)
            except Exception as e:
                if "filter not found" in str(e).lower():
                    self.logger.warning(f"Filter for {event_name} expired or not found, marking for removal")
                    expired_filters.append((contract_address, event_name))
                else:
                    self.logger.error(f"Error processing {event_name} events: {e}")

        # Remove expired filters
        for key in expired_filters:
            if key in self.event_filters:
                self.logger.info(f"Removing expired filter for {key[1]}")
                del self.event_filters[key]

    def cleanup_filters(self) -> None:
        """Clean up all existing filters"""
        if not self.use_filters:
            return

        for (contract_address, event_name), event_filter in list(self.event_filters.items()):
            try:
                if self.w3 and hasattr(event_filter, 'filter_id'):
                    self.w3.eth.uninstall_filter(event_filter.filter_id)
                    self.logger.info(f"Uninstalled filter for {event_name}")
            except Exception as e:
                self.logger.warning(f"Error uninstalling filter for {event_name}: {e}")

        # Clear the dictionary
        self.event_filters.clear()

    def _log_event(self, event_name: str, event: dict) -> None:
        """Format and log a contract event"""
        # Extract event arguments
        args = event['args']
        formatted_args = []
        for key, value in args.items():
            # Format value based on type
            if isinstance(value, bytes):
                formatted_value = value.hex()
            elif isinstance(value, int):
                # Check if it might be wei
                if key.lower().endswith(('amount', 'balance', 'stake')):
                    formatted_value = f"{Web3.from_wei(value, 'ether')} ETH"
                else:
                    formatted_value = str(value)
            else:
                formatted_value = str(value)
            formatted_args.append(f"{key}: {formatted_value}")

        # Build event message
        event_msg = f"Event {event_name} emitted:"
        for arg in formatted_args:
            event_msg += f"\n    {arg}"

        self.logger.info(event_msg)
