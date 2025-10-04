"""
Configuration Manager
- Use BaseSettings to manage environment variables.
- Example: database credentials, API keys, feature flags.
"""

# More on BaseSettings
"""
BaseSettings in Pydantic is a class designed for managing application configuration, particularly by allowing settings to be easily loaded from environment variables and .env files. It extends Pydantic's BaseModel and adds functionality specifically tailored for settings management.

See BaseSettings.py for (in the same directory) for more.
"""

# Example .env file content:
# DATABASE_URL=postgresql://user:password@host:port/dbname
# APP_API_KEY=your_secret_api_key

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field

class AppSettings(BaseSettings, case_sensitive=True):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "My App"
    app_url: str = Field(..., alias='NEXT_PUBLIC_APP_URL')

    clerk_public_key: str = Field(..., alias='NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY')
    clerk_secret_key: str = Field(..., alias='CLERK_SECRET_KEY')

    imagekit_public_key: str = Field(..., alias='NEXT_PUBLIC_IMAGEKIT_PUBLIC_KEY')
    imagekit_private_key: str = Field(..., alias='IMAGEKIT_PRIVATE_KEY')
    imagekit_public_url_endpoint: str = Field(..., alias='NEXT_PUBLIC_IMAGEKIT_URL_ENDPOINT')

    sign_in_url: str = "/sign-in"
    sign_up_url: str = "/sign-up"

    sign_in_fallback_url: str = "/"
    sign_up_fallback_url: str = "/"

    database_url: str = Field(..., alias='DATABASE_URL')
    debug_mode: bool = False

settings = AppSettings()
print(f"App Name: {settings.app_name}")
print(f"App URL: {settings.app_url}")

print(f"Clerk Publishable Key: {settings.clerk_public_key}")
print(f"Clerk Secret Key: {settings.clerk_secret_key}")

print(f"ImageKit Public Key: {settings.imagekit_public_key}")
print(f"ImageKit Private Key: {settings.imagekit_private_key}")
print(f"ImageKit Public URL Endpoint: {settings.imagekit_public_url_endpoint}")

print(f"Sign-in fallback URL: {settings.sign_in_fallback_url}")
print(f"Sign-up fallback URL: {settings.sign_up_fallback_url}")

print(f"Database URL: {settings.database_url}")
print(f"Debug Mode: {settings.debug_mode}")