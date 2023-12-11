import datetime
import enum
import random
import string

from pydantic import BaseModel
from pydantic import Field


class LikePostMessages(str, enum.Enum):
    LIKED = "Liked."
    UNLIKED = "Unliked."


class SignUpSchema(BaseModel):
    """Sign up request schema"""

    username: str = Field(default_factory=lambda: "".join(random.choices(string.ascii_letters, k=8)))
    password: str = Field(
        default_factory=lambda: "".join(
            random.choices(
                string.ascii_letters + string.digits + "!@#$%^&*()_+=-{}[]|\\;:'\",.<>?/",
                k=12,
            )
        )
    )


class SignInSchema(BaseModel):
    """Sign in request schema"""

    username: str
    password: str


class RefreshSchema(BaseModel):
    """Refresh token request schema"""

    refresh: str


class TokenResponseSchema(BaseModel):
    """Token response schema"""

    access: str
    refresh: str


class CreatePostSchema(BaseModel):
    """Creates post request schema"""

    text: str = Field(default_factory=lambda: "".join(random.choices(string.ascii_letters, k=100)))


class CreatePostResponseSchema(BaseModel):
    """Creates post response schema"""

    id: int
    text: str
    author: int


class GetPostResponseSchema(BaseModel):
    """Gets post response schema"""

    id: int


class LikePostRequestSchema(BaseModel):
    """Like post request schema"""

    id: int


class LikePostResponseSchema(BaseModel):
    """Like post response schema"""

    message: LikePostMessages


class UserDataSchema(BaseModel):
    """User json data"""

    username: str = ''
    password: str = ''
    access: str = ''
    refresh: str = ''
    access_to: datetime.datetime = Field(default=(datetime.datetime.now() + datetime.timedelta(minutes=5)))
    refresh_to: datetime.datetime = Field(default=(datetime.datetime.now() + datetime.timedelta(days=15)))
    posts: list[CreatePostResponseSchema] = []
    likes: list[int] = []
