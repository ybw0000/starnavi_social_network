from pydantic import AnyUrl

from automated_bot.clients.base_http_client import BaseHTTPClient
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
from automated_bot.settings import settings


class AutomatedBotAPIClient(BaseHTTPClient):
    BASE_URL: AnyUrl

    class ROUTES:
        # auth endpoints
        SIGN_UP = "api/v1/signup/"
        SIGN_IN = "api/v1/token/"
        SIGN_REFRESH = "api/v1/token/refresh/"

        # posts endpoints
        POSTS = "api/v1/posts/"
        LIKE_POST = "api/v1/posts/{id}/like/"

    def __init__(self, credentials: UserDataSchema) -> None:
        self.BASE_URL = settings.SERVICE_URL
        self.credentials = credentials

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.credentials.access}"}

    async def sign_up(self, data: SignUpSchema) -> TokenResponseSchema:
        response = await self.post(self.ROUTES.SIGN_UP, json=data.model_dump())
        return TokenResponseSchema(**response.json())

    async def sign_in(self, data: SignInSchema) -> TokenResponseSchema:
        response = await self.post(self.ROUTES.SIGN_IN, json=data.model_dump())
        return TokenResponseSchema(**response.json())

    async def refresh_token(self, data: RefreshSchema) -> TokenResponseSchema:
        response = await self.post(self.ROUTES.SIGN_REFRESH, json=data.model_dump())
        return TokenResponseSchema(**response.json())

    async def create_post(self, data: CreatePostSchema) -> CreatePostResponseSchema:
        response = await self.post(self.ROUTES.POSTS, data=data.model_dump(), headers=self.headers)
        return CreatePostResponseSchema(**response.json())

    async def get_posts(self):
        response = await self.get(self.ROUTES.POSTS)
        return [GetPostResponseSchema(**post) for post in response.json()]

    async def like_post(self, params: LikePostRequestSchema) -> LikePostResponseSchema:
        response = await self.patch(self.ROUTES.LIKE_POST.format(**params.model_dump()), headers=self.headers)
        return LikePostResponseSchema(**response.json())
