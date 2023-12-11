# StarNavi social network

### installation to local

1. poetry install && poetry shell
2. Set .env vars (Example in .env.sample)
3. run by `python manage.py runserver` or `sh entrypoint.sh`

### OR docker-compose

1. `docker compose build`
2. `docker compose up -d`

Swagger endpoint `/swagger/` \
Redoc endpoint `/redoc/`

Current test coverage

| Name                                                     | Stmts  | Miss   | Cover |
|----------------------------------------------------------|--------|--------|-------|
| core/__init__.py                                         | 0      | 0      | 100%  |
| core/logging.py                                          | 10     | 0      | 100%  |
| core/middlewares.py                                      | 33     | 0      | 100%  |
| core/settings.py                                         | 30     | 0      | 100%  |
| core/urls.py                                             | 10     | 0      | 100%  |
| manage.py                                                | 12     | 2      | 83%   |
| posts/__init__.py                                        | 0      | 0      | 100%  |
| posts/admin.py                                           | 9      | 0      | 100%  |
| posts/apps.py                                            | 4      | 0      | 100%  |
| posts/migrations/0001_initial.py                         | 7      | 0      | 100%  |
| posts/migrations/0002_alter_like_unique_together.py      | 5      | 0      | 100%  |
| posts/migrations/__init__.py                             | 0      | 0      | 100%  |
| posts/models.py                                          | 29     | 2      | 93%   |
| posts/serializers.py                                     | 21     | 0      | 100%  |
| posts/swagger_schemas.py                                 | 6      | 0      | 100%  |
| posts/tests.py                                           | 179    | 0      | 100%  |
| posts/urls.py                                            | 6      | 0      | 100%  |
| posts/views.py                                           | 60     | 0      | 100%  |
| user/__init__.py                                         | 0      | 0      | 100%  |
| user/admin.py                                            | 5      | 0      | 100%  |
| user/apps.py                                             | 4      | 0      | 100%  |
| user/migrations/0001_initial.py                          | 9      | 0      | 100%  |
| user/migrations/0002_alter_user_last_request.py          | 5      | 0      | 100%  |
| user/migrations/__init__.py                              | 0      | 0      | 100%  |
| user/models.py                                           | 5      | 0      | 100%  |
| user/serializers.py                                      | 26     | 4      | 85%   |
| user/tests.py                                            | 68     | 0      | 100%  |
| user/urls.py                                             | 6      | 0      | 100%  |
| user/views.py                                            | 56     | 2      | 96%   |
| -------------------------------------------------------- | ------ | ------ | ----- |
| TOTAL                                                    | 605    | 10     | 98%   |

# AUTOMATED BOT

1. accessible only from local machine
2. before start u need to place .env file in directory 'automated_bot'
3. .env.sample is the example of your .env
4. to run bot u need to switch to automated_bot dir `cd automated_bot`
5. after all upper points u can run by `python run.py` or if u use Mac with Apple Silicone CPU u can run
   by `arch --arm64 python run.py`

## ATTENTION

### Docker web server was tested on config with 8CPUS and 4GB memory

#### stable .env setup for this Docker config is

```dotenv
MAX_USERS=50
MAX_POSTS_PER_USERS=25
MAX_LIKES_PER_USER=50
```