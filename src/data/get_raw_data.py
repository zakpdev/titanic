# -*- coding: utf-8 -*-
import os
from dotenv import find_dotenv, load_dotenv
from requests import session
import logging

# payload for login to kaggle
payload = {
    'action' : 'login',
    'username' : os.environ.get("KAGGLE_USERNAME"),
    'password' : os.environ.get("KAGGLE_PASSWORD")
}

def extract_data(url, file_path):
    """
    extract data from kaggle
    """
    # setup sessions
    with session() as c:
        c.post('https://www.kaggle.com/account/login', data = payload)
        # open file to write
        with open(file_path, 'wb') as handle:
            response = c.get(url, stream = True)
            for block in response.iter_content(1024):
                handle.write(block)

def main(project_dir):
    """
    main method
    """
    # get logger
    logger = logging.getLogger(__name__)
    logger.info('getting raw data')

    # urls
    train_url = 'https://storage.googleapis.com/kagglesdsdata/competitions/3136/26502/train.csv?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1694987304&Signature=ZhG5tZFPUBQFLhDer45fG%2B5gUMaRYfZ7%2F33UY7cB89%2FhhwvY0Kt%2F%2BKMw1o9KhX90h7ZvTLcvYS5F6OKuGG4Aqp3TdJiqBlenA4h0RoLryGoQqJpZE9k%2Frso2PjiVKbr%2FJz4KaoIAMoZYlDNaBS2DcIzh5biWqeDeulJ16jEVHdxxgKOsC30aZkGPKNa68jn3dwqlmSVB9fZGFIWYRAjytDz5tCnG6nbmwcoa6PDw2YT4raCdl0WhHcjdl1TbB3jesv5lmJ%2Fd7JJQXybJprg9xAYK41xJeK0oaMnP1YwN0tL6rwYJmjZQROsJ40XABnSCMpO0Slx9cJKIZPPboV0z6w%3D%3D&response-content-disposition=attachment%3B+filename%3Dtrain.csv'
    test_url = 'https://storage.googleapis.com/kagglesdsdata/competitions/3136/26502/test.csv?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1694987268&Signature=DLAn2SxiCgruuN6eifRUMAE0GNrbYKzjzxKV2tbCwYoZOc45wFqIEEpzSxH50XfG3fL6Hp41Ls%2FYz2Y2fGGzUJkiZrchTx9J0q%2BMUE4KRYIfYZcPrKrVcNVtk3eYCVQZn6UzSRSqWAry%2B0FSRtZLBhsQ2Apfaf2G%2F5%2FPTrYCR3MYLBJPk1hd70%2FzM3vgrrkbcKl6hAP1m%2Fd%2Feec0pwhZYTOBmx%2BT%2FXTgtHDBhLDBItZV%2FJf9smA00ti%2FniyLeAhR1TAS4pcZhCOZx9Yuav%2F%2BqoNf9JFkWq5zrGwqqZ7PXzqZ8ed4AKl%2F6ZiDa2yKzJTBIP%2BeTp2kadbATGD30EHPFA%3D%3D&response-content-disposition=attachment%3B+filename%3Dtest.csv'

    # file paths
    raw_data_path = os.path.join(os.path.pardir, 'data', 'raw')
    train_data_path = os.path.join(raw_data_path, 'train.csv')
    test_data_path = os.path.join(raw_data_path, 'test.csv')

    # extract data
    extract_data(train_url, train_data_path)
    extract_data(test_url, test_data_path)
    logger.info('downloading raw training and test data')
    
if __name__ == '__main__':
    # getting root directory
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # setup logger
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level = logging.INFO, format = log_fmt)

    # find .env automatically by walking up directories until it is found
    dotenv_path = find_dotenv()
    # load up the entries as environment variables
    load_dotenv(dotenv_path)

    # call the main
    main(project_dir)
