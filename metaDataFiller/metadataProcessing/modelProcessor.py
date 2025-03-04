from metaDataFiller.dbHandler import databaseHandler
from metaDataFiller.dbHandler.databaseHandler import get_creator_links_from_db, create_creator, \
    add_creator_to_links_table, add_creator_to_model, add_model_to_links_table, add_license_to_model
from metaDataFiller.objects.creator import Creator
from metaDataFiller.objects.model import Model
from nanoid import generate

ALPHABET = "bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ0123456789"


def process_data(model: Model, creator: Creator):
    __process_creator(model.creatorAssigned,creator)
    __process_model(model, creator)


def __process_creator(existing_creator, creator: Creator):
    # if creator.creatorName == 'None':
    #     return
    # existing_creator = False
    # if len(creator.newCreatorUrls) > 0:
    # existing_creator2 = databaseHandler.check_if_creator_exist(creator.creatorName, creator.existingCreatorUrls[0])
    # if existing_creator:
    # #     # creator.creatorId = existing_creator[0].get('id')
    # #     #TODO I already get existing links earlier
    # #     # existing_urls = get_creator_links_from_db(existing_creator[0].get('id'))
    #     different_urls = list(set(creator.newCreatorUrls).difference(creator.existingCreatorUrls))
    #     same_urls = list(set(creator.newCreatorUrls).intersection(creator.existingCreatorUrls))
    # #TODO this needs to only be done when both different and same have a value
    #     creator.newCreatorUrls[:] = same_urls
    #     creator.existingCreatorUrls[:] = different_urls
    #     print()
    if creator.creatorId == 'None':
        result = create_creator(creator.creatorName, generate_public_id())
        test = str(create_creator(creator.creatorName, generate_public_id())[0])
        creator.creatorId = test
        if ',' in creator.creatorId:
            print('Error')
    if len(creator.newCreatorUrls) > 0:
        for url in creator.newCreatorUrls:
            add_creator_to_links_table(creator.creatorId, url)
            creator.existingCreatorUrls.append(url)
            creator.newCreatorUrls.remove(url)


def generate_public_id():
    return generate(ALPHABET, 8)


def __process_model(model: Model, creator: Creator):
    if not model.creatorAssigned:
        if creator.creatorId != 'None':
            add_creator_to_model(creator.creatorId, model.modelId)
            model.creatorAssigned = True
    if len(model.newModelUrls) > 0:
        for url in model.newModelUrls:
            add_model_to_links_table(url, model.modelId)
            model.existingModelUrls.append(url)
            model.newModelUrls.remove(url)
    if model.license != 'None':
        add_license_to_model(model.modelId, model.license)

# if 'None' in fileHandler.Creator.creatorId:  # this means the model doesn't have a db_creator added
#     db_creator = get_creator(fileHandler.Creator.creatorName) # getting the creator id if it exists
#     if len(db_creator) == 0:  # this means there is no db_creator in DB
#         fileHandler.Creator.creatorId = str(create_creator(fileHandler.Creator.creatorName)[0].get('id'))
#         add_creator_to_model(fileHandler.Creator.creatorId,fileHandler.Model.modelId)
#         for url in fileHandler.Creator.existingCreatorUrls: # This is added the creator urls to the links table
#             add_creator_to_links_table(fileHandler.Creator.creatorId, url)
#         # TODO need to check if the model urls are in the table already
#         for url in fileHandler.Model.existingModelUrls:
#             add_model_to_links_table(url, fileHandler.Model.modelId)
#         # TODO need to convert incoming license to code for Manyfold
#         add_license_to_model(fileHandler.Model.modelId, fileHandler.Model.license)
#     else:  # this means a db_creator exists but not assigned to model
#         # All ready have creator_id in model_info
#         # existing_creator_id = get_creator(model_info.get('creator'))[0].get('id')
#         #########################STOPPED HERE ######################################################################
#         fileHandler.Creator.creatorId = db_creator[0].get('id')
#         existing_creator_links = get_creator_links_from_db(fileHandler.Creator.creatorId)
#         for creator_url in fileHandler.Creator.existingCreatorUrls:
#             if not any(d['url'] == creator_url for d in existing_creator_links):
#                 add_creator_to_links_table(fileHandler.Creator.creatorId, creator_url)
#                 add_creator_to_model(fileHandler.Creator.creatorId, fileHandler.Model.modelId)
#         for url in model_info.get('model_urls'):
#             add_model_to_links_table(url, model_info.get('model_db_id'))
#         add_license_to_model(model_info.get('model_db_id'), model_info.get('license'))
# else:  # This means a db_creator is already attached to the model
#     # existing_creator_id = get_creator(model_info.get('creator'))[0].get('id')
#     existing_creator_id = get_creator(model_info.get('creator'))[0].get('id')
#     existing_creator_links = get_creator_links_from_db(existing_creator_id)
#     for new_creator_link in model_info.get('creator_urls'):
#         if not any(d['url'] == new_creator_link for d in existing_creator_links):
#             add_creator_to_links_table(existing_creator_id, new_creator_link)
#     for url in model_info.get('model_urls'):
#         add_model_to_links_table(url, model_info.get('model_db_id'))
#     add_license_to_model(model_info.get('model_db_id'), model_info.get('license'))


# def process_model():
#     if 'None' in fileHandler.Creator.creatorId:  # this means the model doesn't have a db_creator added
#         # db_creator = get_creator(thing.get("creatorName"))
#         db_creator = get_creator(fileHandler.Creator.creatorName) # getting the creator id if it exists
#         if len(db_creator) == 0:  # this means there is no db_creator in DB
#             fileHandler.Creator.creatorId = str(create_creator(fileHandler.Creator.creatorName)[0].get('id'))
#             for url in fileHandler.Creator.creatorUrls: # This is added the creator urls to the links table
#                 add_creator_to_links_table(fileHandler.Creator.creatorId, url)
#             # TODO need to test to make sure working after moving
#             add_creator_to_model(fileHandler.Creator.creatorId, fileHandler.Model.modelId) # moved this out of the for loop, should only be run once 11/1/2024;
#             # TODO need to check if the model urls are in the table already
#             for url in fileHandler.Model.modelUrls:
#                 add_model_to_links_table(url, fileHandler.Model.modelId)
#             # TODO need to convert incoming license to code for Manyfold
#             add_license_to_model(fileHandler.Model.modelId, fileHandler.Model.license)
#         else:  # this means a db_creator exists but not assigned to model
#             # All ready have creator_id in model_info
#             # existing_creator_id = get_creator(model_info.get('creator'))[0].get('id')
#             #########################STOPPED HERE ######################################################################
#             fileHandler.Creator.creatorId = db_creator[0].get('id')
#             existing_creator_links = get_creator_links_from_db(fileHandler.Creator.creatorId)
#             for creator_url in fileHandler.Creator.creatorUrls:
#                 if not any(d['url'] == creator_url for d in existing_creator_links):
#                     add_creator_to_links_table(fileHandler.Creator.creatorId, creator_url)
#                     add_creator_to_model(fileHandler.Creator.creatorId, fileHandler.Model.modelId)
#             for url in model_info.get('model_urls'):
#                 add_model_to_links_table(url, model_info.get('model_db_id'))
#             add_license_to_model(model_info.get('model_db_id'), model_info.get('license'))
#     else:  # This means a db_creator is already attached to the model
#         # existing_creator_id = get_creator(model_info.get('creator'))[0].get('id')
#         existing_creator_id = get_creator(model_info.get('creator'))[0].get('id')
#         existing_creator_links = get_creator_links_from_db(existing_creator_id)
#         for new_creator_link in model_info.get('creator_urls'):
#             if not any(d['url'] == new_creator_link for d in existing_creator_links):
#                 add_creator_to_links_table(existing_creator_id, new_creator_link)
#         for url in model_info.get('model_urls'):
#             add_model_to_links_table(url, model_info.get('model_db_id'))
#         add_license_to_model(model_info.get('model_db_id'), model_info.get('license'))
