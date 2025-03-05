import os.path

from metaDataFiller.GlobalVariables.Global import populate_models, add_to_creators_list
from metaDataFiller.customErrors.notAvailableError import notAvailableError
from metaDataFiller.fileHandlers import readmeHandler
from metaDataFiller.metadataProcessing.modelProcessor import process_data
from metaDataFiller.objects.creator import Creator
from metaDataFiller.objects.file_lists import pdforreadme, nopdforreadme
from metaDataFiller.objects.model import Model


def get_thingiverse_DB_data():
    for file in pdforreadme.get("thingiverse"):
        filename = os.path.basename(os.path.dirname(file))
        # Initialize the model object
        model = Model(filename)
        creator = Creator()
        if populate_models(filename, model, creator) == "Error":
            continue
        try:
            readmeHandler.process_thingiverse_readme(file, model, creator)
        except notAvailableError:
            root = os.path.dirname(file)
            pdforreadme.get("thingiverse").remove(file)
            tmp_dict = {'url': root, 'files': os.listdir(root + '/files')}
            nopdforreadme.append(tmp_dict)
            pass
        process_data(model, creator)
        add_to_creators_list(creator)
        print(model.fileName + ' finished')
