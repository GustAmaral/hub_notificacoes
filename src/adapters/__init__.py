"""Pacote de adaptadores de canal (Strategy)."""

from src.adapters.base import CanalAdapter
from src.adapters.discord_adapter import DiscordAdapter
from src.adapters.email_adapter import EmailAdapter

__all__ = ["CanalAdapter", "DiscordAdapter", "EmailAdapter"]
