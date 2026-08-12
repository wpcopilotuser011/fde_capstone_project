"""
Configuration Management Module
Handles loading of configuration from YAML files and environment variables
"""
import os
import yaml
from typing import Any, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ConfigManager:
    """Manages application configuration from multiple sources"""
    
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from YAML files"""
        base_dir = Path(__file__).parent.parent
        
        # Load base config
        config_path = base_dir / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        
        # Override with local config if exists
        local_config_path = base_dir / "config.local.yaml"
        if local_config_path.exists():
            with open(local_config_path, 'r') as f:
                local_config = yaml.safe_load(f)
                self._deep_merge(self.config, local_config)
        
        # Override with environment variables
        self._load_env_overrides()
    
    def _deep_merge(self, base: Dict, override: Dict):
        """Deep merge override dict into base dict"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def _load_env_overrides(self):
        """Load configuration overrides from environment variables"""
        # AI Configuration
        if os.getenv('OPENAI_API_KEY'):
            self.config.setdefault('ai', {})['api_key'] = os.getenv('OPENAI_API_KEY')
        
        if os.getenv('ANTHROPIC_API_KEY'):
            self.config.setdefault('ai', {})['anthropic_api_key'] = os.getenv('ANTHROPIC_API_KEY')
        
        if os.getenv('LLM_MODEL_NAME'):
            self.config.setdefault('ai', {})['llm_model'] = os.getenv('LLM_MODEL_NAME')
        
        # Database
        if os.getenv('DATABASE_URL'):
            self.config.setdefault('database', {})['url'] = os.getenv('DATABASE_URL')
        
        if os.getenv('DB_TYPE'):
            self.config.setdefault('database', {})['type'] = os.getenv('DB_TYPE')
        
        # MySQL connection details (password intentionally not mirrored into
        # self.config - DatabaseManager reads MYSQL_PASSWORD directly from
        # the environment so it never ends up in a config dict/dump/log).
        mysql_overrides = {
            'host': os.getenv('MYSQL_HOST'),
            'port': os.getenv('MYSQL_PORT'),
            'user': os.getenv('MYSQL_USER'),
            'name': os.getenv('MYSQL_DATABASE'),
        }
        if any(mysql_overrides.values()):
            self.config.setdefault('database', {}).setdefault('mysql', {}).update(
                {k: v for k, v in mysql_overrides.items() if v}
            )
        
        # Application
        if os.getenv('APP_ENV'):
            self.config.setdefault('app', {})['environment'] = os.getenv('APP_ENV')
        
        if os.getenv('LOG_LEVEL'):
            self.config.setdefault('logging', {})['level'] = os.getenv('LOG_LEVEL')
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        Example: config.get('ai.llm_model')
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI configuration"""
        return self.config.get('ai', {})
    
    def get_mcp_config(self) -> Dict[str, Any]:
        """Get MCP configuration"""
        return self.config.get('mcp', {})
    
    def get_db_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        return self.config.get('database', {})
    
    def get_external_systems_config(self) -> Dict[str, Any]:
        """Get external systems configuration"""
        return self.config.get('external_systems', {})
    
    def is_mock_mode(self) -> bool:
        """Check if running in mock mode"""
        return self.config.get('external_systems', {}).get('mock_mode', True)


# Global configuration instance
config = ConfigManager()
