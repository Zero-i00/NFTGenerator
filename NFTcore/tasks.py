from NFTGenerator.celery import app
from .services import test
from scripts.nft_generator import make_art, check_paths
import os


@app.task
def start_generate_nft():

    check_paths()
    export_path_for_meta_data_global = os.path.join(os.getcwd(), 'Output', '_metadata', '_metadata.json')

    with open(export_path_for_meta_data_global, 'a') as f:
        f.write('[\n')
    make_art()
    with open(export_path_for_meta_data_global, 'a') as f:
        f.write(']')

@app.task
def hello():
    print('hello world')