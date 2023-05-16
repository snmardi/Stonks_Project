from unpacking import unpackData
from preprocessing import preprocessData
import pandas as pd

unpackData()
preprocessData()

MODE = ''

main_test = pd.read_csv(f'data/{MODE}/{MODE}.csv')
