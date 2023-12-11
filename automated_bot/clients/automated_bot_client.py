import json

from automated_bot.clients.automated_bot_api_client import AutomatedBotAPIClient
from automated_bot.schemas import CreatePostResponseSchema
from automated_bot.schemas import CreatePostSchema
from automated_bot.schemas import GetPostResponseSchema
from automated_bot.schemas import LikePostRequestSchema
from automated_bot.schemas import LikePostResponseSchema
from automated_bot.schemas import RefreshSchema
from automated_bot.schemas import SignInSchema
from automated_bot.schemas import SignUpSchema
from automated_bot.schemas import TokenResponseSchema
from automated_bot.schemas import UserDataSchema
from automated_bot.utils.exceptions import HTTPClientException


class AutomatedBotClient:
    def __init__(self, credentials: UserDataSchema):
        self.credentials = credentials
        self.api_client = AutomatedBotAPIClient(credentials)

    async def sign_up(self, sign_up_data: SignUpSchema) -> TokenResponseSchema:
        try:
            response = await self.api_client.sign_up(sign_up_data)
        except HTTPClientException as exc:
            raise exc
        else:
            return response

    async def sign_in(self) -> TokenResponseSchema:
        data = SignInSchema(username=self.credentials.username, password=self.credentials.password)
        try:
            response = await self.api_client.sign_in(data)
        except HTTPClientException as exc:
            raise exc
        else:
            return response

    async def refresh_token(self) -> TokenResponseSchema:
        data = RefreshSchema(refresh=self.credentials.refresh)
        try:
            response = await self.api_client.refresh_token(data)
        except HTTPClientException as exc:
            raise exc
        else:
            return response

    async def create_post(self) -> CreatePostResponseSchema:
        data = CreatePostSchema()
        try:
            response = await self.api_client.create_post(data)
        except HTTPClientException as exc:
            raise exc
        else:
            return response

    async def get_posts(self) -> list[GetPostResponseSchema]:
        try:
            response = await self.api_client.get_posts()
        except HTTPClientException as exc:
            raise exc
        else:
            return response

    async def like_post(self, post_id: int) -> LikePostResponseSchema:
        params = LikePostRequestSchema(id=post_id)
        try:
            response = await self.api_client.like_post(params)
        except HTTPClientException as exc:
            raise exc
        else:
            return response

    def __repr__(self) -> str:
        return json.dumps(
            {
                'username': self.credentials.username,
                'password': self.credentials.password,
                'posts': [post.id for post in self.credentials.posts],
                'likes': self.credentials.likes,
            }
        )
