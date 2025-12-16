"""
Configuration Loader Utility

Provides functions for loading and validating configuration.
"""

import yaml
from pathlib import Path
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"Configuration loaded from {config_path}")
        return config
    
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file: {e}")
        raise


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration structure.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        True if valid, raises exception otherwise
    """
    required_sections = [
        'scraping',
        'data_storage',
        'embedding',
        'retrieval',
        'llm',
        'evaluation'
    ]
    
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required configuration section: {section}")
    
    logger.info("Configuration validation successful")
    return True


if __name__ == "__main__":
    # Test configuration loading
    try:
        config = load_config()
        validate_config(config)
        print("Configuration loaded and validated successfully!")
        print(f"\nConfiguration sections: {list(config.keys())}")
    except Exception as e:
        print(f"Error: {e}")
