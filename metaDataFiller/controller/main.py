from metaDataFiller.fileHandlers.fileHandler import get_3d_files
from metaDataFiller.dbHandler.databaseHandler import close_connection
from metaDataFiller.metadataGathering.printables_metadata_gathering import get_printables_db_data
from metaDataFiller.metadataGathering.thingiverse_metadata_gathering import get_thingiverse_DB_data

import sys

get_3d_files()
get_printables_db_data()
get_thingiverse_DB_data()
close_connection()
print('Processing finished')
sys.exit()
