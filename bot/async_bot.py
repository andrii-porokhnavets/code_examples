import aiohttp
import asyncio
import json
import random
import time


BASE_URL = 'http://127.0.0.1:8000/api/v1/'

users = []
posts = []
likes = []


def read_config():
    with open('config.json') as f:
        config = json.load(f)

    return config


async def request(session, url, data=None, headers=None):
    async with session.post(url, data=data, headers=headers) as response:
        status = response.status

        return {
            'data': await (response.json() if status == 200 or status == 201 else response.text()),
            'status': status
        }


async def signup_user(session):
    data = {
        'username': f'random_user_{str(random.randint(1, 9999999))}',
        'password1': 'rnd_user_pwd',
        'password2': 'rnd_user_pwd',
    }

    res = await request(session, BASE_URL + 'auth/registration/', data)
    users.append(res)

    return res


async def create_post(session, user):
    url = BASE_URL + 'posts/'
    headers = {'Authorization': 'Bearer ' + user['access_token']}
    data = {
        'title': 'Random title',
        'body': 'Random body',
        'image': 'random_img.png',
    }

    posts.append(await request(session, url, data, headers))


async def signup_and_create_post(session, max_posts_per_user):
    number_of_posts = random.randint(1, max_posts_per_user)

    signup_response = await signup_user(session)

    if signup_response['status'] == 201:
        await asyncio.gather(
            *[create_post(session, signup_response['data']) for _ in range(number_of_posts)]
        )


async def like_post(session, user, post):
    url = BASE_URL + f'posts/{post["id"]}/like/'
    headers = {'Authorization': 'Bearer ' + user['access_token']}

    likes.append(await request(session, url, headers=headers))


async def randomly_like_posts(session, user, posts_to_like, number_of_likes):
    await asyncio.gather(
        *[like_post(session, user, random.choice(posts_to_like)) for _ in range(number_of_likes)]
    )


async def loop(config):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            *[signup_and_create_post(session, config['max_posts_per_user'])
                for _ in range(config['number_of_users'])]
        )

        registered_users = [user['data'] for user in users if user['status'] == 201]
        created_posts = [post['data'] for post in posts if post['status'] == 201]

        if len(created_posts) > 0:
            await asyncio.gather(
                *[randomly_like_posts(session, user, created_posts,
                                      config['max_likes_per_user']) for user in registered_users]
            )


def print_report(config):
    registered_users = [user['data'] for user in users if user['status'] == 201]
    created_posts = [post['data'] for post in posts if post['status'] == 201]
    created_likes = [like['data'] for like in likes if like['status'] == 201]
    multiply_likes = [like['data'] for like in likes if like['status'] == 200]

    print(f'Config: {config}')
    print(f'{"Created":10}{"Success":^10}{"Fail":^10}')
    print(f'{"Users":10}{len(registered_users):^10}{len(users) - len(registered_users):^10}')
    print(f'{"Posts":10}{len(created_posts):^10}{len(posts) - len(created_posts):^10}')
    print(f'{"Likes":10}{len(created_likes):^10}{len(likes) - len(created_likes) - len(multiply_likes):^10}')
    print(f'Likes which were liked multiple times: {len(multiply_likes)}')


def main():
    t0 = time.time()

    print('Script is running...')

    config = read_config()
    asyncio.run(loop(config))

    print_report(config)
    elapsed = time.time() - t0
    print(f'Elapsed time: {elapsed:.2f}s')


if __name__ == '__main__':
    main()


