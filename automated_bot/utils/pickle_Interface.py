import datetime
import logging
import pickle

from automated_bot.clients.automated_bot_client import AutomatedBotClient
from automated_bot.schemas import CreatePostResponseSchema
from automated_bot.schemas import LikePostMessages
from automated_bot.schemas import LikePostResponseSchema
from automated_bot.schemas import SignUpSchema
from automated_bot.schemas import TokenResponseSchema
from automated_bot.schemas import UserDataSchema

logger = logging.getLogger()


class PickleInterface:
    FILE_NAME: str = "users_data.pkl"

    def __init__(self):
        self.data = self.__read_pickle_file()

    def __read_pickle_file(self) -> list[UserDataSchema | None]:
        try:
            with open(self.FILE_NAME, "rb") as pickle_file:
                data = pickle.load(pickle_file)
                return data or []
        except FileNotFoundError:
            logger.error(msg={'message': f'File {self.FILE_NAME} not found!'})
            return []
        except pickle.UnpicklingError:
            logger.error(msg={'message': f'File {self.FILE_NAME} unpickling error.'})
            return []

    def __write_pickle_file(self, data: UserDataSchema) -> None:
        self.data.append(data)
        try:
            with open(self.FILE_NAME, "wb") as pickle_file:
                pickle.dump(self.data, pickle_file)
        except Exception as exc:
            logger.error(msg={'message': f'Error writing to file {self.FILE_NAME}', 'error': str(exc)})

    def __update_pickle_file(self) -> None:
        try:
            with open(self.FILE_NAME, "wb") as pickle_file:
                pickle.dump(self.data, pickle_file)
        except Exception as exc:
            logger.error(msg={'message': f'Error writing to file {self.FILE_NAME}', 'error': str(exc)})

    def clear_file(self) -> None:
        try:
            with open(self.FILE_NAME, "wb") as pickle_file:
                pickle.dump([], pickle_file)
        except Exception as exc:
            logger.error(msg={'message': f'Error writing to file {self.FILE_NAME}', 'error': str(exc)})

    def sign_up(self, credentials: UserDataSchema, sign_up_data: SignUpSchema, response: TokenResponseSchema) -> None:
        credentials.username = sign_up_data.username
        credentials.password = sign_up_data.password
        credentials.access = response.access
        credentials.refresh = response.refresh
        self.__write_pickle_file(credentials)

    def update_credentials(self, credentials: UserDataSchema) -> None:
        for i in range(len(self.data)):
            if self.data[i].username == credentials.username:
                self.data[i] = credentials
        self.__update_pickle_file()

    def refresh_tokens(self, user: AutomatedBotClient, response: TokenResponseSchema) -> None:
        user.credentials.access = response.access
        user.credentials.refresh = response.refresh
        user.credentials.access_to = datetime.datetime.now() + datetime.timedelta(minutes=5)
        user.credentials.refresh_to = datetime.datetime.now() + datetime.timedelta(days=15)
        self.update_credentials(user.credentials)

    def create_post(self, user: AutomatedBotClient, response: CreatePostResponseSchema) -> None:
        user.credentials.posts.append(response)
        self.update_credentials(user.credentials)

    def like_post(self, user: AutomatedBotClient, response: LikePostResponseSchema, post_id: int) -> None:
        if response.message == LikePostMessages.LIKED:
            user.credentials.likes.append(post_id)
        elif response.message == LikePostMessages.UNLIKED:
            for i in range(len(user.credentials.likes)):
                try:
                    if user.credentials.likes[i] == post_id:
                        user.credentials.likes.pop(i)
                except IndexError as exc:
                    logger.error(
                        msg={
                            'message': 'Fail to delete user like from user credentials',
                            'error': str(exc),
                            'post_id': post_id,
                            'user': str(user),
                        }
                    )
        self.update_credentials(user.credentials)
