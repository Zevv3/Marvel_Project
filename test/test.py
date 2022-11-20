from hashlib import md5
from datetime import datetime
from marvel import Marvel
import requests
# I deleted the keys file to hide my keys but I figured I'd keep this file to show my process of figuring this out
from keys import PUBLIC_KEY, PRIVATE_KEY
from flask import jsonify
# https://developer.marvel.com/docs#!/public/getCreatorCollection_get_0

# There is a way of storing the keys more safely using environment variables or something. I want to look into that
m = Marvel(PUBLIC_KEY=PUBLIC_KEY, PRIVATE_KEY=PRIVATE_KEY)
characters = m.characters
# commenting all of this out so I don't accidentally call the api a bunch 
# character_name = characters.all()['data']['results'][0]['name']
# comics = m.comics.all()['data']['results']
# print(jsonify(comics))
# NOTE that when searching comics, you need the character id to search by character


# characters = m.characters
# data = characters.all(nameStartsWith = 'black')['data']['results']
# print(data)

# my_char = characters.all(name = 'Black Cat')['data']['results'][0]['series']

# print(my_char)

# I did all the stuff below before I knew about the Marvel class but I'll just use the class instead

# ts = datetime.now()
# to_hash = f"{ts}{private_key}{public_key}"
# hash = md5(to_hash.encode())
# hash = hash.hexdigest()
# url = f"http://gateway.marvel.com/v1/public/comics?ts=1&apikey={public_key}&hash={hash}"

# def marvel_api_call(characterId):

#     ts = datetime.now()
#     to_hash = f"{ts}{PRIVATE_KEY}{PUBLIC_KEY}"
#     hash = md5(to_hash.encode())
#     hash = hash.hexdigest()
#     url = f"http://gateway.marvel.com/v1/public/characters/{characterId}?ts=1&apikey={PUBLIC_KEY}&hash={hash}"
#     req = requests.get(url)
#     if req.status_code == 200:
#         return req.json()
#     return 'oops'
        

# print(marvel_api_call())