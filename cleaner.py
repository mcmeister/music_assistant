import os
import glob
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_downloaded_files(directory='/tmp/'):
    """
    Delete temporary and mp3 files from the specified directory.
    
    :param directory: The directory to clean. Defaults to '/tmp/'.
    """
    os.chdir(directory)
    file_patterns = ['*.tmp', '*.mp3']
    
    for pattern in file_patterns:
        for file_path in glob.glob(pattern):
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logging.info(f'Deleted: {file_path}')
                else:
                    logging.warning(f'The file does not exist: {file_path}')
            except Exception as e:
                logging.error(f'Error deleting file {file_path}: {e}')

# Execute the cleaning function
clean_downloaded_files()
