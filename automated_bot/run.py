import asyncio
import logging.config

from automated_bot.settings import settings
from automated_bot.utils.bot_interface import BotInterface
from automated_bot.utils.logging import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger()


async def sign_up_users_scenario(interface: BotInterface):
    if interface.USERS:
        difference = settings.MAX_USERS - len(interface.USERS)
        if difference < 0:
            difference = 0

        print(
            f"You have already {len(interface.USERS)} users. ",
            f"In settings provided max count of users is {settings.MAX_USERS}",
            sep="\n",
        )

        while True:
            print(
                "Select scenario:",
                f"1. Forget all existing users and create {settings.MAX_USERS} new.",
                f"2. Signup {difference} new users for reaching max count of users.",
                f"0. Leave signup menu",
                sep="\n",
            )
            choice = input("Enter scenario number: ")

            match choice:
                case "1":
                    await interface.create_users(clear_file=True)
                case "2":
                    await interface.create_users(difference=difference)
                case "0":
                    return
                case _:
                    print("Invalid choice")

    await interface.create_users(clear_file=True)
    await interface.refresh_interface()


async def run():
    interface = BotInterface()
    while True:
        print(
            "MENU:",
            "1. Signup users",
            "2. Create posts",
            "3. Like posts",
            "4. Show users data",
            "0. Shutdown",
            sep="\n",
        )
        choice = input("Enter menu number: ")

        match choice:
            case "1":
                await sign_up_users_scenario(interface)
            case "2":
                await interface.create_posts()
            case "3":
                await interface.like_posts()
            case "4":
                print(*interface.USERS, sep="\n")
            case "0":
                print("See ya!")
                break
            case _:
                print("Invalid choice")


if __name__ == "__main__":
    asyncio.run(run())
