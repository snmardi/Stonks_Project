import os
import pandas as pd
import numpy as np


def formatAccountCondition (id: int, mode: str) -> str or None:
    try:
        account_condition = pd.read_csv(f'data/{mode}/{mode}_additional_info/id_{id}/account_condition_{id}.csv', sep = ';', index_col = 0)
    except FileNotFoundError:
        return 'No Account Condition file for ID: {id}'
    account_condition['date'] = pd.to_datetime(account_condition['date'], format='%Y-%m-%d')
    for clmn in ['start_sum', 'warranty_provision', 'free_funds']:
        account_condition[clmn].loc[account_condition[clmn] == '-'] = np.nan
    if account_condition[clmn].isna().sum() != account_condition.shape[0]:
        account_condition[[clmn, f'{clmn}_delt']] = account_condition[clmn].str.split('(', expand = True)
        account_condition[f'{clmn}_delt'] = account_condition[f'{clmn}_delt'].str.replace(')', '')
        account_condition[f'{clmn}_delt'] = account_condition[f'{clmn}_delt'].str.replace('+', '')
        account_condition[f'{clmn}_delt'].loc[account_condition[f'{clmn}_delt'] == '-'] = np.nan
    else:
        account_condition[f'{clmn}_delt'] = np.nan
    account_condition = account_condition.astype({'start_sum': 'float', 'warranty_provision': 'float', 'free_funds': 'float', 'start_sum_delt': 'float', 'warranty_provision_delt': 'float', 'free_funds_delt': 'float'})
    os.remove(f'data/{mode}/{mode}_additional_info/id_{id}/account_condition_{id}.csv')
    account_condition.to_csv(f'data/{mode}/{mode}_additional_info/id_{id}/account_condition_{id}.csv')
    return account_condition
  
def formatReferencePoint (id: int, mode: str) -> str or None:
    try:
        reference_point = pd.read_csv(f'data/{mode}/{mode}_additional_info/id_{id}/reference_point_{id}.csv', sep = ';', index_col = 0)
    except FileNotFoundError:
        print('No such file for id', id)
        return 'No Reference Point file for ID: {id}'
    for clmn in ['market', 'ticker', 'open_positions', 'price', 'end_day_balance', 'estimated_cost']:
        reference_point[clmn].loc[reference_point[clmn] == '-'] = np.nan
    if reference_point['open_positions'].isna().sum() != reference_point.shape[0]:
        reference_point[['open_positions', 'open_positions_delt']] = reference_point['open_positions'].str.split('(', expand = True)
        reference_point['open_positions_delt'] = reference_point['open_positions_delt'].str.replace(')', '')
        reference_point['open_positions_delt'] = reference_point['open_positions_delt'].str.replace('+', '')
        reference_point['open_positions_delt'].loc[reference_point['open_positions_delt'] == '-'] = np.nan
    else:
        reference_point['open_positions_delt'] = np.nan
    reference_point = reference_point.astype({'open_positions': 'float', 'price': 'float', 'end_day_balance': 'float', 'estimated_cost': 'float'})
    os.remove(f'data/{mode}/{mode}_additional_info/id_{id}/reference_point_{id}.csv')
    reference_point.to_csv(f'data/{mode}/{mode}_additional_info/id_{id}/reference_point_{id}.csv')
    return reference_point

def addNamesToDeals (id: int, market: int, mode: str) -> str or None:
    try:
        deals = pd.read_csv(f'data/{mode}/{mode}_deals/{market}_{id}.csv', names = ["datetime", "ticker", "quantity", "summ"], sep = ';')
    except FileNotFoundError:
        print('No deals data file for ID: {market}_{id}')
        return None
    os.remove(f'data/{mode}/{mode}_deals/{market}_{id}.csv')
    deals.to_csv(f'data/{mode}/{mode}_deals/{market}_{id}.csv')
    return None

def preprocessData():
    for mode in ['train', 'test']:
        main = pd.read_csv(f'data/{mode}/{mode}.csv', sep = ',')
        for clmn in ['start_sum', 'income_rub', 'income_percent']:
            main[clmn] = str(main[clmn]).replace(',', '.')
            main[clmn] = str(main[clmn]).replace(' ', '')
        main['income_percent'].loc[main['income_percent'] == '-'] = np.nan
        main = main.astype({'start_sum': 'float', 'income_rub': 'float', 'income_percent': 'float'})
        os.remove(f'data/{mode}/{mode}.csv')
        main.to_csv(f'data/{mode}/{mode}.csv', index = False)

    for mode in ['train', 'test']:
        main = pd.read_csv(f'data/{mode}/{mode}.csv', sep = ',')
        ids = main['id']
        for id in ids:
            formatAccountCondition(id, mode)
            formatReferencePoint(id, mode)
            for i in range(1, 4):
                addNamesToDeals(id, i, mode)