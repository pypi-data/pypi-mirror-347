from fund_insight_engine.fund_data_retriever.fund_codes import get_fund_codes_class, get_fund_codes_generals
from fund_insight_engine import get_mapping_fund_names_class, get_mapping_fund_names_general
from mongodb_controller import client
from shining_pebbles import get_month_end_dates
from financial_dataset_preprocessor import load_currency
from universal_timeseries_transformer import extend_timeseries_by_all_dates
import pandas as pd
from tqdm import tqdm
 
def get_fund_codes_for_aum(date_ref, option_source='mongodb'):
    if option_source == 'mongodb':
        fund_codes_class = get_fund_codes_class(date_ref=date_ref)
        fund_codes_general = get_fund_codes_generals(date_ref=date_ref)
        fund_codes_for_aum = list(set(fund_codes_class + fund_codes_general))
    elif option_source == 's3':
        names_class = get_mapping_fund_names_class(date_ref=date_ref)
        names_general = get_mapping_fund_names_general(date_ref=date_ref)
        names_for_aum = {**names_class, **names_general}
        fund_codes_for_aum = list(names_for_aum.keys())
    return fund_codes_for_aum

def fetch_data_for_aum(date_ref):
    fund_codes_for_aum = get_fund_codes_for_aum(date_ref=date_ref)
    collection = client['database-rpa']['dataset-menu8186']
    pipeline = [
        {'$match': {'펀드코드': {'$in': fund_codes_for_aum}, '일자': '2025-04-30'}},
        {'$project': {'_id': 0, '펀드코드': 1, '순자산': 1}}
    ]
    cursor = collection.aggregate(pipeline)
    data = list(cursor)
    return data

def get_df_nav_for_aum(date_ref):
    data = fetch_data_for_aum(date_ref=date_ref)
    df = pd.DataFrame(data)
    return df

def get_aum_of_date(date_ref):
    df = get_df_nav_for_aum(date_ref=date_ref)
    aum_of_date = df['순자산'].sum()
    return aum_of_date

def get_timeseries_aum(end_date, start_date=None):
    start_date = start_date or '2020-05-31'
    start_year_month = start_date.replace('-', '')[:6]
    end_year_month = end_date.replace('-', '')[:6]
    month_end_dates = get_month_end_dates(start_year_month=start_year_month, end_year_month=end_year_month, date_format='%Y-%m-%d')
    aums = []
    for end_date in tqdm(month_end_dates):
        try:
            aum_of_date = get_aum_of_date(date_ref=end_date)
            aums.append({'date': end_date, 'aum': aum_of_date})
        except:
            pass
    aum = pd.DataFrame(aums).set_index('date')   
    return aum

def get_timeseries_aum_in_usd(end_date, start_date=None):
    timeseries_aum = get_timeseries_aum(end_date=end_date, start_date=start_date)
    df_currency = load_currency(ticker_bbg_currency='USDKRW Curncy').rename(columns={'PX_LAST': 'usdkrw'})
    df_currency = extend_timeseries_by_all_dates(df_currency, start_date=start_date, end_date=end_date)
    timeseries_aum_in_usd = timeseries_aum.join(df_currency, how='left')
    timeseries_aum_in_usd['aum_in_usd'] = timeseries_aum_in_usd['aum'] / timeseries_aum_in_usd['usdkrw']
    return timeseries_aum_in_usd

def get_firm_aum_since_inception(end_date, start_date=None, option_unit=True):
    timeseries_aum = get_timeseries_aum_in_usd(end_date=end_date, start_date=start_date)
    if option_unit:
        timeseries_aum['AUM (KRW, Billion)'] = round(timeseries_aum['aum']/ 1e9 ,4)
        timeseries_aum['AUM (USD, Million)'] = round(timeseries_aum['aum_in_usd']/ 1e6, 4)
        timeseries_aum = timeseries_aum[['AUM (KRW, Billion)', 'AUM (USD, Million)']]
    return timeseries_aum