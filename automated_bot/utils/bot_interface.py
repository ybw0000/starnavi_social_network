import asyncio
import datetime
import logging
import random

from automated_bot.clients.automated_bot_client import AutomatedBotClient
from automated_bot.schemas import GetPostResponseSchema
from automated_bot.schemas import SignUpSchema
from automated_bot.schemas import UserDataSchema
from automated_bot.settings import settings
from automated_bot.utils.exceptions import HTTPClientException
from automated_bot.utils.pickle_Interface import PickleInterface

logger = logging.getLogger(__name__)


class BotInterface:
    USERS: list[AutomatedBotClient]

    def __init__(self) -> None:
        self.pickle_interface = PickleInterface()
        self.__init_users()

    def __init_users(self) -> None:
        """Init users"""
        self.USERS = []
        for credentials in self.pickle_interface.data:
            self.USERS.append(AutomatedBotClient(credentials))

    async def refresh_interface(self) -> None:
        """Refresh bot interface after bulks"""
        self.pickle_interface = PickleInterface()
        self.__init_users()

    async def clear_file(self) -> None:
        """Clear users data file"""
        self.pickle_interface.clear_file()
        await self.refresh_interface()

    async def _sign_up(self) -> None:
        """Sign up new user"""
        credentials = UserDataSchema()
        sign_up_data = SignUpSchema()
        client = AutomatedBotClient(credentials)

        try:
            response = await client.sign_up(sign_up_data)
        except HTTPClientException as exc:
            logger.info(msg={"message": "Failed to create user.", "error": str(exc)})
        else:
            self.pickle_interface.sign_up(credentials, sign_up_data, response)

    async def __update_access_tokens(self, user: AutomatedBotClient) -> None:
        """Verify and update access tokens if needed"""
        if user.credentials.access_to < datetime.datetime.now():
            if user.credentials.refresh_to < datetime.datetime.now():
                response = await user.sign_in()
            else:
                response = await user.refresh_token()
            self.pickle_interface.refresh_tokens(user, response)

    async def _create_post(self, user: AutomatedBotClient) -> None:
        """Create post"""
        try:
            response = await user.create_post()
        except HTTPClientException as exc:
            logger.info(msg={"message": "Failed to create post.", "error": str(exc), "user": str(user)})
        else:
            self.pickle_interface.create_post(user, response)

    async def _like_post(self, user: AutomatedBotClient, post: GetPostResponseSchema) -> None:
        try:
            response = await user.like_post(post.id)
        except HTTPClientException as exc:
            logger.info(msg={'message': 'Failed post like.', 'post_id': post.id, 'error': str(exc), 'user': str(user)})
        else:
            self.pickle_interface.like_post(user, response, post.id)

    async def create_users(self, difference: int = 0, clear_file: bool = False) -> None:
        """Bulk create users"""
        if clear_file:
            await self.clear_file()
            await asyncio.gather(*[self._sign_up() for _ in range(settings.MAX_USERS)])
            await self.refresh_interface()
        elif difference:
            await asyncio.gather(*[self._sign_up() for _ in range(difference)])
            await self.refresh_interface()

    async def create_posts(self) -> None:
        """Bulk create posts"""
        for user in self.USERS:
            await self.__update_access_tokens(user)
            count_of_posts = random.randint(0, settings.MAX_POSTS_PER_USERS)
            await asyncio.gather(*[self._create_post(user) for _ in range(count_of_posts)])

    async def like_posts(self) -> None:
        """Bulk like posts"""
        list_of_posts = await AutomatedBotClient(UserDataSchema()).get_posts()
        for user in self.USERS:
            await self.__update_access_tokens(user)
            count_of_likes = random.randint(0, settings.MAX_LIKES_PER_USER)
            await asyncio.gather(*[self._like_post(user, random.choice(list_of_posts)) for _ in range(count_of_likes)])
