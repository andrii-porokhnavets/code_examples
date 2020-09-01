# Basic APIs

```
POST   api/v1/auth/registration/ - signup user
POST   api/v1/auth/login/ - login user
POST   api/v1/posts/ - post creation
POST   api/v1/posts/<int:post_id>/like/ - post like
DELETE api/v1/posts/<int:post_id>/like/ - post unlike
GET    api/v1/likes/analytics/?[date_from=]&[date_to=] - analytics aggregated by day about how many likes were made
GET    api/vi/users/<int:user_id>/activity/ - resturns information when user was login the last time and when he made the last request
```

# Bot
There are two versions of the bot: `bot.py` and `async_bot.py`.
Config file is in `.json` format. All those files are stored in `bot` folder.