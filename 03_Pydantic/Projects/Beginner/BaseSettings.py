from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "My App"
    database_url: str
    debug_mode: bool = False
    api_key: str = Field(alias="APP_API_KEY")

# Example .env file content:
# DATABASE_URL=postgresql://user:password@host:port/dbname
# APP_API_KEY=your_secret_api_key

settings = AppSettings()

print(f"App Name: {settings.app_name}")
print(f"Database URL: {settings.database_url}")
print(f"Debug Mode: {settings.debug_mode}")
print(f"API Key: {settings.api_key}")