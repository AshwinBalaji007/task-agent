import os
import yaml
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# --- Helper function to find the project root ---
def get_project_root() -> Path:
    """Returns the project root folder."""
    return Path(__file__).parent.parent.parent

# --- Main Settings Class ---
class LLMSettings(BaseSettings):
    """Configuration for the Large Language Model."""
    model_name: str = "gemini-1.0-pro"
    temperature: float = 0.7

class Settings(BaseSettings):
    """
    Main settings class to hold all configuration.
    It reads from environment variables and a YAML file.
    """
    model_config = SettingsConfigDict(env_file=get_project_root() / '.env', env_file_encoding='utf-8', extra='ignore')

    google_api_key: str = Field(..., validation_alias="GOOGLE_API_KEY")
    app_env: str = Field("development", validation_alias="APP_ENV")
    
    app_name: str = "AI Task Manager Agent"
    log_level: str = "INFO"
    llm: LLMSettings = LLMSettings()


def load_yaml_config(settings: Settings) -> dict:
    """Loads settings from the YAML file based on the app environment."""
    config_path = get_project_root() / 'configs' / 'settings.yaml'
    
    if not config_path.exists():
        return {}

    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)

    yaml_config = config_data.get('default', {})
    env_config = config_data.get(settings.app_env, {})
    yaml_config.update(env_config)
    
    return yaml_config

def create_settings() -> Settings:
    """Factory function to create and load settings."""
    # First, load settings from environment variables (.env file)
    # The linter gives a false positive here, so we ignore it.
    settings = Settings()  # type: ignore 
    
    # Then, load settings from the YAML file
    yaml_config = load_yaml_config(settings)
    
    settings_data = settings.model_dump()
    
    def update_dict(d, u):
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = update_dict(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    final_data = update_dict(settings_data, yaml_config)
    
    return Settings.model_validate(final_data)


# --- Singleton instance ---
settings = create_settings()