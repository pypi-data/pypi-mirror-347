from elabapi_python.rest import ApiException

from .elabftw import API_KEY_NAME

def connect(verify_ssl: bool = False):
    from .elabftw import connect_to_database
    connect_to_database(verify_ssl)
    
    
def download_experiment_tree(ID):
    """
    Get the experiment with the given ID from the eLabFTW database and save it to the rawdata folder.
    
    Parameters
    ----------
    ID : str
        The ID of the experiment to retrieve.
    
    Returns
    -------
    None
    """
    
    
    from .elabftw import create_structure_and_download_experiments
    try:
        create_structure_and_download_experiments(ID)
    except ApiException as e:
        if e.status == 404:
            print(f"Experiment with ID {ID} not found. error 404")
        elif( e.status == 401):
            print(f"The API key is not correct. Check your .env file for '{API_KEY_NAME}'-key . error 401")
        else:
            print(f"An error occurred: {e}")