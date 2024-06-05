import os
import glob
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def delete_files(directory, pattern):
    """
    Delete files matching the pattern in the specified directory.

    :param directory: The directory to search for files.
    :param pattern: The pattern of files to delete.
    """
    try:
        if os.path.exists(directory):
            os.chdir(directory)
            for file in glob.glob(pattern):
                try:
                    os.remove(file)
                    logging.info(f'Deleted: {file}')
                except OSError as e:
                    logging.error(f'Error deleting {file}: {e}')
        else:
            logging.error(f'The directory {directory} does not exist')
    except OSError as e:
        logging.error(f'Error changing directory to {directory}: {e}')

if __name__ == "__main__":
    temp_directory = '/storage/emulated/0/temp'
    delete_files(temp_directory, '*.tmp')
    delete_files(temp_directory, '*.mp3')
