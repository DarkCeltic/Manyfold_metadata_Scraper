from metaDataFiller.dbHandler.databaseHandler import get_creator_links_from_db, get_model_info_from_db, \
    get_model_links_from_db, \
    get_creator
from metaDataFiller.fileHandlers.fileHandler import creator_list, license_dict
from urllib.parse import *

from metaDataFiller.objects.file_lists import pdforreadme


def add_to_creators_list(creator):
    if len(creator_list) == 0 and creator.creatorId != 'None':
        creator_list[creator.creatorId] = creator
    else:
        # for c in creator_list:
        # if creator.creatorId not in creator_list:
        if creator.creatorId == 'None':
            pass
        elif creator.creatorId not in creator_list.keys():
            creator_list[creator.creatorId] = creator
        elif creator.creatorId in creator_list.keys():
            if creator_list[creator.creatorId] != creator:
                creator_list[creator.creatorId] = creator
        else:
            pass


def populate_models(filename, model, creator):
    model_creator_ids = get_model_info_from_db(filename)[0]
    if len(model_creator_ids) == 0:  # TODO Check if model not in manyfold, shouldn't be needed, used this when I broke my db
        print(filename + ' not available in DB')
        return 'Model not in DB'
    populate_objects_with_db_data(model_creator_ids, model, creator)


def populate_objects_with_db_data(model_creator_ids, model, creator):
    model.modelId = str(model_creator_ids.get('id'))
    model.license = model_creator_ids.get('license')
    if model_creator_ids.get('creator_id') is not None:
        model.creatorAssigned = True
        creator.creatorId = str(model_creator_ids.get('creator_id'))
        if ',' in creator.creatorId:
            print("Fail")
        add_existing_creator_urls(model_creator_ids.get('creator_urls'), creator)
        creator.creatorName = model_creator_ids.get('name')
    add_existing_model_urls(model_creator_ids.get('model_urls'), model)


def get_existing_creator_data(model, creator):
    check_for_existing_creator(model, creator)


def check_for_existing_creator(model, creator):
    # if creator ID is not in List then create it
    if creator.creatorId in creator_list.keys():
        model.creatorAssigned = True
        creator.existing_creator(creator_list.get(creator.creatorId))
    else:
        add_creator_name(get_creator_name(creator.creatorId), creator)
        add_existing_creator_urls(get_creator_links_from_db(creator.creatorId), creator)


def add_existing_model_urls(model_links, model):
    for url in model_links:
        if url not in model.existingModelUrls:
            model.existingModelUrls.append(url)


def add_existing_creator_urls(creator_urls, creator):
    if len(creator_urls) > 1:
        pass
    for url in creator_urls:
        if url not in creator.existingCreatorUrls:
            creator.existingCreatorUrls.append(url)


def add_creator_name(creator_name, creator):
    creator.creatorName = creator_name


# TODO  change the new and existing urls to use the followingtype(apple).__name__
#   1. change creator and model to have the same names
#   2. merge the two functions
def add_new_model_urls(model_url, model):
    parse_url = urlparse(model_url)
    if len(model.existingModelUrls) == 0:
        model.newModelUrls.append(model_url)
        return
    else:
        is_not_existing_url = True
        for url in model.existingModelUrls:
            if parse_url.path in url:
                is_not_existing_url = False
        if is_not_existing_url:
            model.newModelUrls.append(model_url)


def add_new_creator_urls(creator_url, creator):
    parse_url = urlparse(creator_url)
    if len(creator.existingCreatorUrls) == 0:
        creator.newCreatorUrls.append(creator_url)
        # return NOT NEEDED?
    else:
        is_not_existing_url = True
        for url in creator.existingCreatorUrls:
            if parse_url.path in url:
                is_not_existing_url = False
        if is_not_existing_url:
            creator.newCreatorUrls.append(creator_url)


def convert_license(license_url_name):
    if not license_dict.get(license_url_name):
        print(license_url_name + ' not in dict')
    return license_dict.get(license_url_name)


def get_creator_name(creator_id):
    return get_creator(creator_id)
