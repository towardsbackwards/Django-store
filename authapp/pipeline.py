from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from social_core.exceptions import AuthForbidden

from env.Lib.collections import OrderedDict


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              '/method/account.getInfo',
                              urlencode(OrderedDict(
                                  fields=','.join(
                                      ('bdate', 'sex', 'about', 'photo_max', 'user_ids', 'lang', 'interests')),
                                  access_token=response['access_token'],
                                  v='5.92')), None
                              ))
        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]  # Берем первый элемент JSON по ключу response (список)

        print('*' * 100)
        print('VK response: ', resp)
        print('*' * 100)

        if data['sex'] and not user.shopuserprofile.gender:
            if data['sex'] == 2:
                user.shopuserprofile.gender = 'M'
            else:
                user.shopuserprofile.gender = 'F'
        if data['bdate']:
            user.shopuserprofile.bdate = resp['bdate']
            #bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        user.save()


    print('*' * 100)
    print('response', response)
    print('*' * 100)
    if backend.name == "google-oauth2":
        if 'gender' in response.keys():
            if response['gender'] == 'male':
                user.shopuserprofile.gender = 'M'
            else:
                user.shopuserprofile.gender = 'F'

        if 'tagline' in response.keys():
            user.shopuserprofile.tagline = response['tagline']

        if 'aboutMe' in response.keys():
            user.shopuserprofile.aboutMe = response['aboutMe']

        if 'ageRange' in response.keys():
            minAge = response['ageRange']['min']
            # print(f'{user} minAge: {minAge}')
            if int(minAge) < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')

        user.save()

    return
