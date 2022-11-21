from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
from marvel_inventory.forms import SearchCharactersForm
from marvel_inventory.helpers import token_required
from marvel import Marvel
from dotenv import load_dotenv
import os
import json

def configure():
    load_dotenv()

pub_key = os.getenv('PUBLIC_KEY')
priv_key = os.getenv('PRIVATE_KEY')

search = Blueprint('search', __name__, url_prefix = '/search', template_folder='search_templates')
# os.getenv('PUBLIC_KEY') will get the public key
@search.route('/searchcharacters', methods = ['POST', 'GET'])
def searchCharacters():
    """
    Search the Marvel API. Returns the results for the user to copy/paste into Insomnia to add
    to their personal api.
    """
    form = SearchCharactersForm()
    # api call
    try:
        if form.validate_on_submit():
            charname = form.charName.data
            comictitle = form.comicTitle.data
            # The marvel api has this handy class that makes api calls for you
            # In the 'test.py' file, you can see how I went about figuring out the api calls if you want
            m = Marvel(PUBLIC_KEY=pub_key, PRIVATE_KEY=priv_key)
            characters = m.characters
            if charname:
                data = characters.all(nameStartsWith=charname)['data']['results']
                # gather info
                id = data[0]['id']
                name = data[0]['name']
                desc = data[0]['description']
                num_comics = data[0]['comics']['available']
                num_series = data[0]['series']['available']
                num_stories = data[0]['stories']['available']
                # add info to dict
                results = {
                    "id": id,
                    "name": name,
                    "desc": desc,
                    "num_comics": num_comics,
                    "num_series": num_series,
                    "num_stories": num_stories
                }
            elif comictitle:
                # We want the character id as well as the name
                # First we have to get the comic id
                comics = m.comics
                comicid = comics.all(titleStartsWith=comictitle)['data']['results'][0]['id']
                # Then we get the list of characters using that id
                data = characters.all(comics=comicid)['data']['results']
                charDict = {}
                if len(data) == 0:
                    charDict['no'] = 'results'
                for i in range(len(data)):
                    name = data[i]['name']
                    id = data[i]['id']
                    charDict[name] = id
                results = charDict
                # Unfortunately, it looks like the api has an empty list of characters for a lot of comics
                # for testing, 'amazing' will give you spider-man


            # converts dictionary to a string with "" which is what insomnia needs
            results = json.dumps(results)
            # Display results on the page
            return render_template('characters_search.html', form=form, char_searched=results)
            # db.session.add(character)
            # db.session.commit()
            # I actually can't do this because I need the user token
            # So the user has to take the data they get from the search and add the character manually
    except:
        raise Exception('Invalid Form Data: Please check your form')
    return render_template('characters_search.html', form=form, char_searched = 'no results')
