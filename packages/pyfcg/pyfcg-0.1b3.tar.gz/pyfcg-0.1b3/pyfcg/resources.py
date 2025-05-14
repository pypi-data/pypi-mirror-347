import appdirs
import os
import wget

from urllib.error import HTTPError

def load_resource(file_name, target_directory=None):
    """
    Loads the resource named `file_name` by returning its local path.
    If resource is not yet locally available, it will first be downloaded from the file server.
    By default, the file will be stored in the user data directory, although an alternative `target_directory` can be specfied.
    """
    # By default, resources are stored locally in the user data directory
    if target_directory is None:
        user_data_dir = appdirs.user_data_dir(appname="FCG Go")
        target_directory = os.path.join(user_data_dir, "resources")
        os.makedirs(target_directory, exist_ok=True)
    
    file_path = os.path.join(target_directory, file_name)

    # If resource is not yet locally available, download it from file server
    if not os.path.isfile(file_path):
        try:
            url = 'https://emergent-languages.org/fcg-go/resources/' + file_name
            wget.download(url, out=target_directory)
        except HTTPError as exception:
            print(f"Failed to load resource with name '{file_name}'.")
            return None
    
    return file_path
