from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union

#--------------------
# Author: NotOfficial
# Data: 13.05.2025
#--------------------
@dataclass
class Field:
    name: str
    value: str
    inline: bool = False

@dataclass
class DiscordEmbed:
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    color: int = 0x000000
    fields: List[Field] = field(default_factory=list)
    author: Optional[Dict] = None
    footer: Optional[Dict] = None
    image: Optional[str] = None
    thumbnail: Optional[str] = None

    def setTitle(self, title: str) -> "DiscordEmbed":
        """Устанавливает заголовок эмбеда."""
        self.title = title
        return self

    def setDescription(self, description: str) -> "DiscordEmbed":
        """Устанавливает описание эмбеда."""
        self.description = description
        return self

    def setUrl(self, url: str) -> "DiscordEmbed":
        """Устанавливает URL эмбеда."""
        self.url = url
        return self

    def setColor(self, color: Union[int, str]) -> "DiscordEmbed":
        """Устанавливает цвет эмбеда (HEX-строка или int)."""
        if isinstance(color, str) and color.startswith("#"):
            self.color = int(color[1:], 16)
        else:
            self.color = color
        return self

    def addField(self, name: str, value: str, inline: bool = False) -> "DiscordEmbed":
        """Добавляет поле в эмбед."""
        self.fields.append(Field(name, value, inline))
        return self

    def setAuthor(self, name: str, icon_url: Optional[str] = None, url: Optional[str] = None) -> "DiscordEmbed":
        """Устанавливает автора эмбеда."""
        self.author = {"name": name}
        if icon_url:
            self.author["icon_url"] = icon_url
        if url:
            self.author["url"] = url
        return self

    def setFooter(self, text: str, icon_url: Optional[str] = None) -> "DiscordEmbed":
        """Устанавливает футер эмбеда."""
        self.footer = {"text": text}
        if icon_url:
            self.footer["icon_url"] = icon_url
        return self

    def setImage(self, url: str) -> "DiscordEmbed":
        """Устанавливает изображение эмбеда."""
        self.image = url
        return self

    def setThumbnail(self, url: str) -> "DiscordEmbed":
        """Устанавливает миниатюру эмбеда."""
        self.thumbnail = url
        return self

    def to_dict(self) -> Dict:
        """Преобразует эмбед в словарь для отправки."""
        result = {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "color": self.color,
            "fields": [field.__dict__ for field in self.fields]
        }
        if self.author:
            result["author"] = self.author
        if self.footer:
            result["footer"] = self.footer
        if self.image:
            result["image"] = {"url": self.image}
        if self.thumbnail:
            result["thumbnail"] = {"url": self.thumbnail}
        return {k: v for k, v in result.items() if v is not None}