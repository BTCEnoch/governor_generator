#!/usr/bin/env python3
"""
TAP Protocol Contract Builder
Builds, compiles, and manages smart contracts for the Enochian Governor system
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ContractInfo:
    """Information about a TAP Protocol contract"""
    name: str
    file_path: Path
    contract_type: str
    size_bytes: int
    functions: List[str] = field(default_factory=list)
    events: List[str] = field(default_factory=list)
    compiled_hash: Optional[str] = None
    deployment_address: Optional[str] = None
    deployment_timestamp: Optional[datetime] = None

@dataclass
class DeploymentConfig:
    """Configuration for contract deployment"""
    network: str = "testnet"
    gas_limit: int = 5000000
    gas_price: int = 20
    deployer_address: Optional[str] = None
    constructor_args: Dict[str, Any] = field(default_factory=dict)

class TAPContractBuilder:
    """
    Builder for TAP Protocol smart contracts
    """
    
    def __init__(self, contracts_dir: Path = Path(".")):
        """Initialize the contract builder"""
        self.contracts_dir = Path(contracts_dir)
        self.build_dir = self.contracts_dir / "build"
        self.build_dir.mkdir(exist_ok=True)
        
        # Contract registry
        self.contracts: Dict[str, ContractInfo] = {}
        self.deployment_history: List[Dict[str, Any]] = []
        
        logger.info("🚀 TAP Contract Builder initialized")
        logger.info(f"   Contracts directory: {self.contracts_dir}")
        logger.info(f"   Build directory: {self.build_dir}")
    
    def discover_contracts(self) -> List[ContractInfo]:
        """Discover all .tap contract files in the directory"""
        
        logger.info("🔍 Discovering TAP Protocol contracts...")
        
        contract_files = list(self.contracts_dir.glob("*.tap"))
        discovered_contracts = []
        
        for contract_file in contract_files:
            try:
                contract_info = self._analyze_contract_file(contract_file)
                self.contracts[contract_info.name] = contract_info
                discovered_contracts.append(contract_info)
                
                logger.info(f"✅ Discovered contract: {contract_info.name}")
                logger.info(f"   File: {contract_file.name}")
                logger.info(f"   Functions: {len(contract_info.functions)}")
                logger.info(f"   Events: {len(contract_info.events)}")
                
            except Exception as e:
                logger.error(f"❌ Failed to analyze {contract_file}: {str(e)}")
        
        logger.info(f"📋 Total contracts discovered: {len(discovered_contracts)}")
        return discovered_contracts
    
    def _analyze_contract_file(self, file_path: Path) -> ContractInfo:
        """Analyze a TAP contract file and extract metadata"""
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract contract name
        contract_name = "Unknown"
        if "contract " in content:
            for line in content.split('\n'):
                if line.strip().startswith('contract '):
                    contract_name = line.split('contract ')[1].split(' ')[0].strip('{')
                    break
        
        # Extract functions
        functions = []
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('function '):
                func_name = stripped.split('function ')[1].split('(')[0]
                functions.append(func_name)
        
        # Extract events
        events = []
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('event '):
                event_name = stripped.split('event ')[1].split('(')[0]
                events.append(event_name)
        
        # Determine contract type
        contract_type = "utility"
        if "governor" in file_path.name.lower():
            contract_type = "governance"
        elif "tokenomics" in file_path.name.lower():
            contract_type = "economics"
        
        # Calculate file hash
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        return ContractInfo(
            name=contract_name,
            file_path=file_path,
            contract_type=contract_type,
            size_bytes=len(content.encode()),
            functions=functions,
            events=events,
            compiled_hash=content_hash
        )
    
    def compile_contract(self, contract_name: str) -> bool:
        """Compile a TAP Protocol contract"""
        
        if contract_name not in self.contracts:
            logger.error(f"❌ Contract {contract_name} not found")
            return False
        
        contract = self.contracts[contract_name]
        
        logger.info(f"🔨 Compiling contract: {contract_name}")
        
        try:
            # Read contract source
            with open(contract.file_path, 'r') as f:
                source_code = f.read()
            
            # Create compilation output
            compilation_output = {
                "contract_name": contract_name,
                "source_file": str(contract.file_path),
                "compiled_at": datetime.now().isoformat(),
                "source_hash": contract.compiled_hash,
                "functions": contract.functions,
                "events": contract.events,
                "bytecode": self._generate_mock_bytecode(source_code),
                "abi": self._generate_contract_abi(contract),
                "metadata": {
                    "compiler": "TAP-Builder-v1.0",
                    "language": "TAP Protocol",
                    "size_bytes": contract.size_bytes
                }
            }
            
            # Save compiled contract
            output_file = self.build_dir / f"{contract_name}_compiled.json"
            with open(output_file, 'w') as f:
                json.dump(compilation_output, f, indent=2)
            
            logger.info(f"✅ Contract {contract_name} compiled successfully")
            logger.info(f"   Output: {output_file}")
            logger.info(f"   Functions: {len(contract.functions)}")
            logger.info(f"   Events: {len(contract.events)}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to compile {contract_name}: {str(e)}")
            return False
    
    def _generate_mock_bytecode(self, source_code: str) -> str:
        """Generate mock bytecode for TAP contract"""
        # In a real implementation, this would use the TAP compiler
        # For now, generate a deterministic mock bytecode based on source
        source_hash = hashlib.sha256(source_code.encode()).hexdigest()
        return f"0x{source_hash[:64]}"
    
    def _generate_contract_abi(self, contract: ContractInfo) -> List[Dict[str, Any]]:
        """Generate ABI (Application Binary Interface) for contract"""
        abi = []
        
        # Add constructor
        abi.append({
            "type": "constructor",
            "inputs": [],
            "stateMutability": "nonpayable"
        })
        
        # Add functions
        for func_name in contract.functions:
            abi.append({
                "type": "function",
                "name": func_name,
                "inputs": [],  # Simplified - would parse from source
                "outputs": [],
                "stateMutability": "nonpayable" if func_name.startswith(('set', 'update', 'mint', 'complete')) else "view"
            })
        
        # Add events
        for event_name in contract.events:
            abi.append({
                "type": "event",
                "name": event_name,
                "inputs": [],  # Simplified - would parse from source
                "anonymous": False
            })
        
        return abi
    
    def prepare_deployment(self, contract_name: str, config: DeploymentConfig) -> Dict[str, Any]:
        """Prepare contract for deployment"""
        
        if contract_name not in self.contracts:
            logger.error(f"❌ Contract {contract_name} not found")
            return {}
        
        # Check if contract is compiled
        compiled_file = self.build_dir / f"{contract_name}_compiled.json"
        if not compiled_file.exists():
            logger.info(f"📦 Compiling {contract_name} for deployment...")
            if not self.compile_contract(contract_name):
                return {}
        
        # Load compiled contract
        with open(compiled_file, 'r') as f:
            compiled_contract = json.load(f)
        
        # Create deployment package
        deployment_package = {
            "contract_name": contract_name,
            "network": config.network,
            "compiled_contract": compiled_contract,
            "deployment_config": {
                "gas_limit": config.gas_limit,
                "gas_price": config.gas_price,
                "deployer_address": config.deployer_address,
                "constructor_args": config.constructor_args
            },
            "deployment_id": f"deploy_{contract_name}_{int(datetime.now().timestamp())}",
            "prepared_at": datetime.now().isoformat()
        }
        
        # Save deployment package
        package_file = self.build_dir / f"{contract_name}_deployment_package.json"
        with open(package_file, 'w') as f:
            json.dump(deployment_package, f, indent=2)
        
        logger.info(f"📦 Deployment package prepared: {contract_name}")
        logger.info(f"   Network: {config.network}")
        logger.info(f"   Package: {package_file}")
        
        return deployment_package
    
    def simulate_deployment(self, deployment_package: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate contract deployment (mock implementation)"""
        
        contract_name = deployment_package["contract_name"]
        
        logger.info(f"🎯 Simulating deployment: {contract_name}")
        
        # Generate mock deployment result
        mock_address = f"0x{hashlib.sha256(f'{contract_name}{datetime.now()}'.encode()).hexdigest()[:40]}"
        mock_tx_hash = f"0x{hashlib.sha256(f'tx{contract_name}{datetime.now()}'.encode()).hexdigest()}"
        
        deployment_result = {
            "contract_name": contract_name,
            "deployment_successful": True,
            "contract_address": mock_address,
            "transaction_hash": mock_tx_hash,
            "block_number": 12345678,
            "gas_used": deployment_package["deployment_config"]["gas_limit"] // 2,
            "deployment_timestamp": datetime.now().isoformat(),
            "network": deployment_package["network"]
        }
        
        # Update contract info
        if contract_name in self.contracts:
            self.contracts[contract_name].deployment_address = mock_address
            self.contracts[contract_name].deployment_timestamp = datetime.now()
        
        # Record deployment
        self.deployment_history.append(deployment_result)
        
        # Save deployment result
        result_file = self.build_dir / f"{contract_name}_deployment_result.json"
        with open(result_file, 'w') as f:
            json.dump(deployment_result, f, indent=2)
        
        logger.info(f"✅ Deployment simulation completed: {contract_name}")
        logger.info(f"   Address: {mock_address}")
        logger.info(f"   Transaction: {mock_tx_hash}")
        
        return deployment_result
    
    def build_all_contracts(self) -> Dict[str, bool]:
        """Build all discovered contracts"""
        
        logger.info("🏗️ Building all contracts...")
        
        # Discover contracts first
        self.discover_contracts()
        
        build_results = {}
        
        for contract_name in self.contracts:
            logger.info(f"🔨 Building {contract_name}...")
            build_results[contract_name] = self.compile_contract(contract_name)
        
        successful_builds = [name for name, success in build_results.items() if success]
        failed_builds = [name for name, success in build_results.items() if not success]
        
        logger.info(f"📊 Build Summary:")
        logger.info(f"   ✅ Successful: {len(successful_builds)} ({', '.join(successful_builds)})")
        if failed_builds:
            logger.info(f"   ❌ Failed: {len(failed_builds)} ({', '.join(failed_builds)})")
        
        return build_results
    
    def get_contract_info(self, contract_name: str) -> Optional[ContractInfo]:
        """Get information about a specific contract"""
        return self.contracts.get(contract_name)
    
    def list_contracts(self) -> List[ContractInfo]:
        """List all discovered contracts"""
        return list(self.contracts.values())
    
    def get_deployment_history(self) -> List[Dict[str, Any]]:
        """Get deployment history"""
        return self.deployment_history

# Convenience functions
def build_governor_contracts(contracts_dir: Path = Path(".")) -> bool:
    """Build all governor-related contracts"""
    
    builder = TAPContractBuilder(contracts_dir)
    
    # Build all contracts
    results = builder.build_all_contracts()
    
    # Check if all builds succeeded
    return all(results.values())

def deploy_contracts_to_testnet(contracts_dir: Path = Path(".")) -> Dict[str, str]:
    """Deploy all contracts to testnet and return addresses"""
    
    builder = TAPContractBuilder(contracts_dir)
    builder.discover_contracts()
    
    deployment_addresses = {}
    
    for contract_name in builder.contracts:
        # Prepare deployment
        config = DeploymentConfig(network="testnet")
        package = builder.prepare_deployment(contract_name, config)
        
        if package:
            # Simulate deployment
            result = builder.simulate_deployment(package)
            if result.get("deployment_successful"):
                deployment_addresses[contract_name] = result["contract_address"]
    
    return deployment_addresses

if __name__ == "__main__":
    # Example usage
    logger.info("🧪 Testing TAP Contract Builder")
    
    # Create builder
    builder = TAPContractBuilder()
    
    # Discover and build contracts
    contracts = builder.discover_contracts()
    logger.info(f"📋 Found {len(contracts)} contracts")
    
    # Build all contracts
    build_results = builder.build_all_contracts()
    
    # Prepare deployment for governor contract
    if "GovernorRegistry" in builder.contracts:
        config = DeploymentConfig(network="testnet")
        package = builder.prepare_deployment("GovernorRegistry", config)
        
        if package:
            result = builder.simulate_deployment(package)
            logger.info(f"🎯 Deployment result: {result['deployment_successful']}")
    
    logger.info("✅ TAP Contract Builder test complete") 