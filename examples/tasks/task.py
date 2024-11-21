import datetime
import random

from hikari import GatewayBot, StartedEvent

from aurum import Client
from aurum.ext.tasks.task import Task, task

CHANNEL_ID = 1130594736944726106
MESSAGES: list[str] = [
    "Don't forget to complete your tasks today! 💪",
    "Set your goals for today and stick to them! 🎯",
    "Always strive for the best! ✨",
]

bot = GatewayBot("...")
client = Client(bot)


@task(datetime.timedelta(hours=2), name="daily_reminder")
async def daily_reminder_task(_: Task) -> None:
    await bot.rest.create_message(CHANNEL_ID, random.choice(MESSAGES))


@bot.listen()
async def on_started(_: StartedEvent) -> None:
    daily_reminder_task.start()


if __name__ == "__main__":
    bot.run()
