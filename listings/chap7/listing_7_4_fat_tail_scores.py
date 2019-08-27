import pandas as pd
import numpy as np
from listing_5_2_dataset_stats import dataset_stats

def fat_tail_scores(data_set_path='',skew_thresh=4.0,save=True,**kwargs):

    churn_data = pd.read_csv(data_set_path)
    churn_data.set_index(['account_id','observation_date'],inplace=True)
    data_scores = churn_data.copy()
    data_scores.drop('is_churn',axis=1)

    stats = dataset_stats(data_set_path,save=False)
    stats=stats.drop('is_churn')
    skewed_columns=(stats['skew']>skew_thresh) & (stats['min'] >= 0)
    skewed_columns=skewed_columns[skewed_columns] # keep only the True values
    fattail_columns=(stats['skew']>skew_thresh) & (stats['min'] < 0)
    fattail_columns=fattail_columns[fattail_columns] # keep only the True values

    for col in skewed_columns.keys():
        data_scores[col]=np.log(1.0+data_scores[col])

    for col in fattail_columns.keys():
        data_scores[col]=np.log(data_scores[col] + np.sqrt(np.power(data_scores[col],2) + 1.0) )

    data_scores=(data_scores-data_scores.mean())/data_scores.std()
    data_scores['is_churn']=churn_data['is_churn']

    if save:
        score_save_path=data_set_path.replace('.csv','_scores.csv')

        data_scores.to_csv(score_save_path,header=True)

    return data_scores
