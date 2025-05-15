import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Default configuration values
DEFAULT_CONFIG = {
    # API Configuration
    'model_base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
    'model_name': 'qwen-max',
    'api_token': '',
    'max_workers': 10
}

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        """Initialize configuration manager"""
        self.config_file = Path(config_file)
        self.config = DEFAULT_CONFIG.copy()
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
                logger.debug(f"Configuration loaded from {self.config_file}")
        except Exception as e:
            logger.warning(f"Error loading configuration: {str(e)}")
    
    def _save_config(self) -> None:
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            logger.debug(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """Update configuration with new values"""
        try:
            self.config.update(new_config)
            self._save_config()
            logger.debug("Configuration updated successfully")
        except Exception as e:
            logger.error(f"Error updating configuration: {str(e)}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)

# Create a global configuration instance
config = ConfigManager()