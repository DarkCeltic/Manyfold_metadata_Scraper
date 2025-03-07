import sys

from metaDataFiller.dbHandler.databaseHandler import close_connection
from metaDataFiller.fileHandlers import googleHandler
from metaDataFiller.fileHandlers.fileHandler import get_3d_files
from metaDataFiller.metadataGathering.printables_metadata_gathering import get_printables_db_data
from metaDataFiller.metadataGathering.thingiverse_metadata_gathering import get_thingiverse_DB_data

get_3d_files()
get_printables_db_data()
get_thingiverse_DB_data()
# googleHandler.google_handler()
close_connection()
print('Processing finished')
sys.exit()
