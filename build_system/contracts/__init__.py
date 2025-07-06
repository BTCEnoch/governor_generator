"""
TAP Protocol Smart Contracts Module
Enochian Governor Generation System

This module provides TAP Protocol smart contracts for:
- Governor registry and management
- Tokenomics and reward distribution
- Contract building and deployment tools
"""

from .contract_builder import (
    TAPContractBuilder,
    ContractInfo,
    DeploymentConfig,
    build_governor_contracts,
    deploy_contracts_to_testnet
)

__all__ = [
    "TAPContractBuilder",
    "ContractInfo", 
    "DeploymentConfig",
    "build_governor_contracts",
    "deploy_contracts_to_testnet"
]

# Module version
__version__ = "1.0.0"

# TAP Protocol contract files
GOVERNOR_CONTRACT = "governor_contracts.tap"
TOKENOMICS_CONTRACT = "tokenomics_contracts.tap"

# Available contracts
CONTRACTS = {
    "GovernorRegistry": {
        "file": GOVERNOR_CONTRACT,
        "type": "governance",
        "description": "Governor registration and management contract"
    },
    "WisdomTokenEconomics": {
        "file": TOKENOMICS_CONTRACT,
        "type": "economics", 
        "description": "Tokenomics and reward distribution contract"
    }
}
