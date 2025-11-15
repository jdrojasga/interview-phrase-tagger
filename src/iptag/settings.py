"""Settings module for iptag package."""

from pydantic_settings import BaseSettings


class IptagSettings(BaseSettings):
    """Application settings for Interview Phrase Tagger (iptag)."""

    debug: bool = False

    class Config:
        """Configuration for IptagSettings."""

        env_file = ".env"
        env_file_encoding = "utf-8"
