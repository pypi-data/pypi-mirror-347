# Webhook Helper 📨

**Webhook Helper** — это простая и мощная Python-библиотека для отправки сообщений и эмбедов через вебхуки на платформы **Discord** и **Telegram**. Поддерживает как синхронные, так и асинхронные методы, а также отправку одного или нескольких эмбедов за раз. Идеально подходит для автоматизации уведомлений, ботов и интеграций.

## Основные возможности ✨

- 📬 Отправка текстовых сообщений и эмбедов через вебхуки.
- 🔄 Поддержка синхронных и асинхронных методов.
- 📋 Создание и настройка Discord-эмбедов с помощью удобного API.
- 🌐 Совместимость с **Discord** и **Telegram**.
- 🚫 Отключение логов HTTP-запросов для чистоты вывода.
- 🛠️ Простая интеграция в ваши проекты.

## Установка 🛠️

1. Убедитесь, что у вас установлен Python 3.8 или выше.
2. Установите зависимость:

```bash
pip install webhookhelper
```
## Использование 🚀

Библиотека предоставляет класс `WebHookHelper` для работы с вебхуками и класс `DiscordEmbed` для создания эмбедов. Вы можете отправлять сообщения и эмбеды синхронно или асинхронно.

### Пример: Отправка сообщения и эмбедов в Discord

```python
import asyncio
from webhook_helper import WebHookHelper, DiscordEmbed

# Синхронный пример
def sync_example():
    discord_hook = WebHookHelper(
        type="discord",
        webhook="YOUR_DISCORD_WEBHOOK_URL"
    )

    # Создаем два эмбеда
    embed1 = DiscordEmbed()
    embed1.setTitle("Первый эмбед").setDescription("Тест 1").setColor("#FF0000")
    embed1.addField("Поле 1", "Значение 1", inline=True)

    embed2 = DiscordEmbed()
    embed2.setTitle("Второй эмбед").setDescription("Тест 2").setColor("#00FF00")
    embed2.addField("Поле 2", "Значение 2", inline=True)

    # Отправляем сообщение и эмбеды
    discord_hook.send("Простое сообщение")
    discord_hook.send_embed([embed1, embed2])

# Асинхронный пример
async def async_example():
    discord_hook = WebHookHelper(
        type="discord",
        webhook="YOUR_DISCORD_WEBHOOK_URL"
    )

    embed1 = DiscordEmbed()
    embed1.setTitle("Первый эмбед").setDescription("Тест 1").setColor("#FF0000")
    embed1.addField("Поле 1", "Значение 1", inline=True)

    embed2 = DiscordEmbed()
    embed2.setTitle("Второй эмбед").setDescription("Тест 2").setColor("#00FF00")
    embed2.addField("Поле 2", "Значение 2", inline=True)

    # Отправляем асинхронно
    await discord_hook.async_send("Простое сообщение")
    await discord_hook.async_send_embed([embed1, embed2])

# Запуск
sync_example()
asyncio.run(async_example())
```

### Пример: Отправка в Telegram

```python
import asyncio
from webhook_helper import WebHookHelper, DiscordEmbed

async def telegram_example():
    telegram_hook = WebHookHelper(
        type="telegram",
        token="YOUR_TELEGRAM_BOT_TOKEN",
        chat_id="YOUR_CHAT_ID"
    )

    embed = DiscordEmbed()
    embed.setTitle("Тестовый эмбед").setDescription("Это тестовое сообщение")
    embed.addField("Поле", "Значение")

    # Отправляем асинхронно
    await telegram_hook.async_send_embed(embed)

asyncio.run(telegram_example())
```

## API 📖

### Класс `WebHookHelper`

| Метод | Описание | Тип |
| --- | --- | --- |
| `send(content: str)` | Синхронно отправляет текстовое сообщение | Синхронный |
| `async_send(content: str)` | Асинхронно отправляет текстовое сообщение | Асинхронный |
| `send_embed(embeds: Union[DiscordEmbed, List[DiscordEmbed]])` | Синхронно отправляет один или несколько эмбедов | Синхронный |
| `async_send_embed(embeds: Union[DiscordEmbed, List[DiscordEmbed]])` | Асинхронно отправляет один или несколько эмбедов | Асинхронный |

### Класс `DiscordEmbed`

| Метод | Описание |
| --- | --- |
| `setTitle(title: str)` | Устанавливает заголовок эмбеда |
| `setDescription(description: str)` | Устанавливает описание |
| `setUrl(url: str)` | Устанавливает URL |
| `setColor(color: Union[int, str])` | Устанавливает цвет (HEX или int) |
| `addField(name: str, value: str, inline: bool)` | Добавляет поле |
| `setAuthor(name: str, icon_url: str, url: str)` | Устанавливает автора |
| `setFooter(text: str, icon_url: str)` | Устанавливает футер |
| `setImage(url: str)` | Устанавливает изображение |
| `setThumbnail(url: str)` | Устанавливает миниатюру |
| `to_dict()` | Преобразует эмбед в словарь |

## Лицензия 📜

Эта библиотека распространяется под MIT License. Вы можете свободно использовать, модифицировать и распространять код при условии сохранения текста лицензии и указания авторства.

## Контакты 📧

Автор: NotOfficial\
Дата: 13.05.2025\
GitHub: NotOfficial\
Issues: Создать issue

---

⭐ **Поддержите проект, поставив звезду на GitHub!**
