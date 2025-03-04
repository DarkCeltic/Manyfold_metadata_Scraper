from selenium.common import SessionNotCreatedException
from urllib3.exceptions import ReadTimeoutError

from metaDataFiller.GlobalVariables.Global import populate_models, add_to_creators_list
from metaDataFiller.customErrors.notAvailableError import notAvailableError
from metaDataFiller.fileHandlers.pdfHandler import get_pdf_data
from metaDataFiller.metadataProcessing.modelProcessor import process_data
from metaDataFiller.objects.file_lists import pdforreadme, nopdforreadme
from metaDataFiller.objects.model import Model

from metaDataFiller.objects.creator import Creator

import os.path


def get_printables_db_data():
    for file in pdforreadme.get("printables"):
        filename = os.path.basename(os.path.dirname(file))
        # Initialize the model object
        model = Model(filename)
        creator = Creator()
        if populate_models(filename, model, creator) == "Error":
            continue
        # if creator.existingCreatorUrls != 'None':
        #     return
        try:
            get_pdf_data(file, model, creator)
        except notAvailableError:
            root = os.path.dirname(file)
            pdforreadme.get("printables").remove(file)
            tmp_dict = {'url': root, 'files': os.listdir(root)}
            nopdforreadme.append(tmp_dict)
            pass
        except (SessionNotCreatedException, ReadTimeoutError):
            pass
        process_data(model, creator)
        add_to_creators_list(creator)
