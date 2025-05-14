import requests
import aiohttp
import logging
from typing import List, Dict, Optional, Union
from .discord_embed import DiscordEmbed

#--------------------
# Author: NotOfficial
# Data: 13.05.2025
#--------------------
class WebHookHelper:
    def __init__(self, type: str, **kwargs):
        """Инициализирует WebHookHelper для указанного типа вебхука."""
        self.type = type.lower()
        self.logger = logging.getLogger("WebHookHelper")
        logging.getLogger("urllib3").setLevel(logging.CRITICAL)
        logging.getLogger("aiohttp").setLevel(logging.CRITICAL)

        if self.type == "discord":
            self.webhook_url = kwargs.get("webhook")
        elif self.type == "telegram":
            token = kwargs.get("token")
            chat_id = kwargs.get("chat_id")
            self.webhook_url = f"https://api.telegram.org/bot{token}/sendMessage"
            self.chat_id = chat_id
        else:
            raise ValueError("Unsupported type")

    def send(self, content: str) -> None:
        """Синхронно отправляет текстовое сообщение."""
        if self.type == "discord":
            data = {"content": content}
            self._post(data)
        elif self.type == "telegram":
            data = {
                "chat_id": self.chat_id,
                "text": content,
                "parse_mode": "Markdown"
            }
            self._post(data)

    async def async_send(self, content: str) -> None:
        """Асинхронно отправляет текстовое сообщение."""
        if self.type == "discord":
            data = {"content": content}
            await self._async_post(data)
        elif self.type == "telegram":
            data = {
                "chat_id": self.chat_id,
                "text": content,
                "parse_mode": "Markdown"
            }
            await self._async_post(data)

    def send_embed(self, embeds: Union[DiscordEmbed, List[DiscordEmbed]]) -> None:
        """Синхронно отправляет один или несколько эмбедов."""
        if not isinstance(embeds, list):
            embeds = [embeds]

        if self.type == "discord":
            data = {"embeds": [embed.to_dict() for embed in embeds]}
            self._post(data)
        elif self.type == "telegram":
            for embed in embeds:
                lines = [f"*{embed.title}*"] if embed.title else []
                if embed.description:
                    lines.append(embed.description)
                for field in embed.fields:
                    lines.append(f"*{field.name}*: {field.value}")
                if embed.image:
                    lines.append(f"[Image]({embed.image})")
                text = "\n".join(lines)
                self.send(text)

    async def async_send_embed(self, embeds: Union[DiscordEmbed, List[DiscordEmbed]]) -> None:
        """Асинхронно отправляет один или несколько эмбедов."""
        if not isinstance(embeds, list):
            embeds = [embeds]

        if self.type == "discord":
            data = {"embeds": [embed.to_dict() for embed in embeds]}
            await self._async_post(data)
        elif self.type == "telegram":
            for embed in embeds:
                lines = [f"*{embed.title}*"] if embed.title else []
                if embed.description:
                    lines.append(embed.description)
                for field in embed.fields:
                    lines.append(f"*{field.name}*: {field.value}")
                if embed.image:
                    lines.append(f"[Image]({embed.image})")
                text = "\n".join(lines)
                await self.async_send(text)

    def _post(self, data: Dict) -> None:
        """Внутренний метод для синхронной отправки HTTP-запроса."""
        try:
            headers = {"Content-Type": "application/json"}
            r = requests.post(self.webhook_url, json=data, headers=headers)
            if not r.ok:
                self.logger.warning(f"Webhook response: {r.status_code}, {r.text}")
        except Exception as e:
            self.logger.error(f"Error: {e}")

    async def _async_post(self, data: Dict) -> None:
        """Внутренний метод для асинхронной отправки HTTP-запроса."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=data) as response:
                    if not response.ok:
                        self.logger.warning(f"Webhook response: {response.status}, {await response.text()}")
        except Exception as e:
            self.logger.error(f"Error: {e}")