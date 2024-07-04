from hikari import GatewayBot, StartedEvent

from aurum import Client
from aurum.ext.tasks.cron import CronTask, cron_task

bot = GatewayBot("...")
client = Client(bot)


@cron_task("0 8 * * *", name="morning_greeting")
async def good_morning(_: CronTask) -> None:
    await bot.rest.create_message(1130594736944726106, "☀️ Good morning! Have a good day!")


@cron_task("0 22 * * *", name="night_greeting")
async def good_night(_: CronTask) -> None:
    await bot.rest.create_message(1130594736944726106, "🌙 Good night! Have a good sleep!")


@bot.listen()
async def on_started(_: StartedEvent) -> None:
    good_morning.start()
    good_night.start()


if __name__ == "__main__":
    bot.run()
