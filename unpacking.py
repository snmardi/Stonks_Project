import zipfile
import os
import shutil


def unpackData ():
    with zipfile.ZipFile('data.zip', 'r') as zipFile:
        zipFile.extractall()
    shutil.rmtree('__MACOSX')
    for mode in ['train', 'test']:
        dealsList = os.listdir(f'data/{mode}/{mode}_deals')
        for deals in dealsList:
            with zipfile.ZipFile(f'data/{mode}/{mode}_deals/{deals}', 'r') as zipFile:
                zipFile.extractall(f'data/{mode}/{mode}_deals')
            os.remove(f'data/{mode}/{mode}_deals/{deals}')