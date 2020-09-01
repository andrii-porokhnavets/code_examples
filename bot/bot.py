import json
import requests
import random
import time


BASE_API = "http://127.0.0.1:8000/api/v1/"

users = []
posts = []
likes = []


def read_config():
    with open("config.json") as f:
        config = json.load(f)

    return config


def request(url, data=None, headers=None):
    response = requests.post(url, data=data, headers=headers)
    status = response.status_code

    return {
        'data': response.json() if status == 200 or status == 201 else response.text,
        'status': status
    }


def signup_user():
    data = {
        'username': f'random_user_{str(random.randint(1, 9999999))}',
        'password1': 'rnd_user_pwd',
        'password2': 'rnd_user_pwd',
    }

    return request(BASE_API + 'auth/registration/', data)


def create_post(user):
    headers = {'Authorization': 'Bearer ' + user['access_token']}
    data = {
        'title': 'Random title',
        'body': 'Random body',
        'image': 'random_img.png',
    }

    return request(BASE_API + 'posts/', data=data, headers=headers)


def like_post(post, user):
    headers = {'Authorization': 'Bearer ' + user['access_token']}

    return request(BASE_API + f'posts/{post["id"]}/like/', headers=headers)


def main():
    config = read_config()

    for _ in range(config['number_of_users']):
        users.append(signup_user())

    registered_users = [user['data'] for user in users if user['status'] == 201]

    for user in registered_users:
        number_of_post = random.randint(1, config['max_posts_per_user'])

        for _ in range(number_of_post):
            posts.append(create_post(user))

    created_posts = [post['data'] for post in posts if post['status'] == 201]

    for user in registered_users:
        for _ in range(config['max_likes_per_user']):
            post = random.choice(created_posts)
            likes.append(like_post(post, user))

    print_report(config)


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


if __name__ == '__main__':
    t0 = time.time()
    print('Script is running...')

    main()

    elapsed = time.time() - t0
    print(f'Elapsed time: {elapsed:.2f}s')
