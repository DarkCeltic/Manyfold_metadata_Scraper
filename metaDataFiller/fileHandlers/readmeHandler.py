import configparser
from pathlib import Path
from metaDataFiller.APIs.apiHandler import thingiverse_api_get_thing
from metaDataFiller.GlobalVariables.Global import add_new_creator_urls, add_new_model_urls, convert_license
from metaDataFiller.customErrors.notAvailableError import notAvailableError
from metaDataFiller.objects.creator import Creator
from metaDataFiller.objects.model import Model
from metaDataFiller.webScrapers import thingiverseScraper

config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Access values from the configuration file
api_key = config.get('Thingiverse_API_Key', 'key')

def process_thingiverse_readme(f, model: Model, creator: Creator):
    thing_url = get_thing_id_from_file(f)
    if api_key == '':
        thingiverseScraper.scrape_thingiverse(thing_url, creator, model)
    else:
        thingiverse_info = thingiverse_api_get_thing(Path(thing_url).name.split(':')[1])  # TODO this shouldn't process data just return it
        if thingiverse_info == 'no longer available':
            raise notAvailableError("Url not available")
        if creator.creatorName is not thingiverse_info.get('creator'):
            creator.creatorName = thingiverse_info.get('creator')
        add_new_creator_urls(thingiverse_info.get('creator_urls')[0], creator)
        add_new_model_urls(thingiverse_info.get('model_urls')[0], model)
        if model.license is not thingiverse_info.get('license'):
            model.license = convert_license(thingiverse_info.get('license'))



def get_thing_id_from_file(thing_file):
    read_me = open(thing_file, "r")
    split_read_me = read_me.read().split()
    read_me.close()
    url = split_read_me[len(split_read_me) - 1]
    return url
