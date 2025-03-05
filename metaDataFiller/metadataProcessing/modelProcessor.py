from nanoid import generate

from metaDataFiller.dbHandler.databaseHandler import create_creator, \
    add_creator_to_links_table, add_creator_to_model, add_model_to_links_table, add_license_to_model
from metaDataFiller.objects.creator import Creator
from metaDataFiller.objects.model import Model

ALPHABET = "bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ0123456789"


def process_data(model: Model, creator: Creator):
    __process_creator(model.creatorAssigned, creator)
    __process_model(model, creator)


def __process_creator(existing_creator, creator: Creator):
    if creator.creatorId == 'None':
        create_creator(creator.creatorName, generate_public_id())
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
