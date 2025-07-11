"""
Base test cases for mystical systems
"""

import pytest
from typing import Any, Dict, Type
from .base import BitcoinMysticalSystem
from .schemas import MysticalSystemConfig, BitcoinIntegrationConfig
from .bitcoin_integration import BitcoinIntegration

class TestMysticalSystemBase:
    """Base test class for mystical systems"""
    
    @pytest.fixture
    def system_class(self) -> Type[BitcoinMysticalSystem]:
        """Override this to return your system class"""
        raise NotImplementedError("Must provide system class")
        
    @pytest.fixture
    def system_config(self) -> Dict[str, Any]:
        """Override this to provide system-specific config"""
        return {
            "system_id": "test_system",
            "name": "Test System",
            "description": "Test mystical system",
            "version": "1.0.0",
            "capabilities": ["test"]
        }
        
    @pytest.fixture
    def bitcoin_config(self) -> BitcoinIntegrationConfig:
        """Bitcoin integration config for testing"""
        return BitcoinIntegrationConfig(
            use_ordinals=True,
            use_inscriptions=True,
            network="testnet",
            min_confirmations=1
        )
        
    @pytest.fixture
    def system(self, system_class, system_config, bitcoin_config):
        """System instance for testing"""
        config = MysticalSystemConfig(
            **system_config,
            bitcoin_integration=bitcoin_config.dict()
        )
        return system_class(config.dict())
        
    def test_system_initialization(self, system):
        """Test system initialization"""
        assert system.id == "test_system"
        assert system.config is not None
        
    def test_bitcoin_integration(self, system):
        """Test Bitcoin integration"""
        # Test with valid txid
        test_txid = "a" * 64
        attributes = system.derive_mystical_attributes(test_txid)
        assert isinstance(attributes, list)
        
        # Test with valid ordinal
        system.bind_to_ordinal("test_ordinal")
        assert system.ordinal_data is not None
        
        # Test with valid inscription
        system.bind_to_inscription("test_inscription")
        assert system.inscription_data is not None
        
    def test_validation(self, system):
        """Test input validation"""
        # Test with valid input
        valid_input = {"name": "test", "txid": "a" * 64}
        result = system.validate_input(valid_input)
        assert result.is_valid
        assert not result.errors
        
        # Test with invalid input
        invalid_input = {"invalid": "data"}
        result = system.validate_input(invalid_input)
        assert not result.is_valid
        assert result.errors
        
    def test_correspondence_calculation(self, system):
        """Test mystical correspondence calculation"""
        test_data = {
            "source": "test_source",
            "target": "test_target"
        }
        result = system.calculate_correspondences(test_data)
        assert isinstance(result, dict)
        
    def test_system_info(self, system):
        """Test system info retrieval"""
        info = system.get_system_info()
        assert isinstance(info, dict)
        assert "name" in info
        assert "version" in info
        assert "description" in info
        assert "capabilities" in info 