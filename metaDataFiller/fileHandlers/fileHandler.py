import glob
import json
import os.path

from metaDataFiller.dbHandler.databaseHandler import config
from metaDataFiller.objects import file_lists

creator_list = {}
with open(os.getcwd() + '/license_info') as f:
    data = f.read()
license_dict: dict = json.loads(data)


# TODO scrape the stl filenames on google to get all pages

def get_3d_files():
    config.read('config.ini')
    # Access values from the configuration file
    path = config.get('3dFilesLocation', 'path')
    find_files_to_proces(path)

    # TODO this is starter code to query google for missing files, will work on later
    # for f in nopdforreadme:
    #     filename = os.path.basename(f['url'])
    #     search_params = '"' + filename.split('#')[0].replace(' ','+') + '"'
    #     for file in f['files']:
    #         search_params += '+"' + file.replace(' ', '+') + '"'
    # googleScraper.scrape_google_for_file_info(search_params)


def find_files_to_proces(path):
    printables = []
    thingiverse = []

    for file in sorted(glob.glob(path + '**/*#*', recursive=True)):
        if any(fi.endswith('.pdf') for fi in os.listdir(file)):
            printables.append(glob.glob(file + '/' + "*.pdf")[0])
        elif any(fi.endswith('README.txt') for fi in os.listdir(file)):
            thingiverse.append(glob.glob(file + '/' + "README.txt")[0])
        else:
            stlFiles = glob.glob(file + '/**/*.stl', recursive=True)
            stlFiles2 = glob.glob(file + '/**/*.STL', recursive=True)
            stlFilesCombined = stlFiles + stlFiles2
            stleFilenames = [os.path.basename(path) for path in stlFilesCombined]
            tmp_dict = {'url': file, 'files': stleFilenames}
            file_lists.nopdforreadme.append(tmp_dict)
            del tmp_dict
    file_lists.pdforreadme.get('printables').extend(printables)
    file_lists.pdforreadme.get('thingiverse').extend(thingiverse)
