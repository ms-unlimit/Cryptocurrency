import pandas as pd
import numpy as np
from numpy.linalg import norm

def vec(row):
    val_usd_max = 2889108351.13
    num_btc = 20000000

    # d7_val, d7_h2l, d7_o2c = row['d7_volume_usd']/val_usd_max , row['d7_h2l']*2 , row['d7_o2c']*2
    d7_val, d7_h2l, d7_o2c = (row['d7_volume_usd']/(row['d7_weighted_price']*num_btc))*100 , row['d7_h2l']*2 , row['d7_o2c']*2

    h24_val,h24_h2l ,h24_o2c  = (row['h24_volume_usd']/(row['h24_weighted_price']*num_btc))*1000  , row['h24_h2l']*20 , row['h24_o2c']*20

    h4_val,h4_h2l ,h4_o2c  = (row['h4_volume_usd']/(row['h4_weighted_price']*num_btc))*100000 , row['h4_h2l']*50 , row['h4_o2c']*50

    h1_val,h1_h2l ,h1_o2c  = (row['h1_volume_usd']/(row['h1_weighted_price']*num_btc))*1000000 , row['h1_h2l']*100 , row['h1_o2c']*100
    # h1_val,h1_h2l ,h1_o2c  = (row['h1_volume_usd']/row['d7_volume_usd'])*100 , df['h1_h2l']*100 , df['h1_o2c']*100

    # pred = 1 if row['h1f_o2c'] >=0 else 0

    if row['h1f_o2c'] > 0.002:
        pred = 1
    elif row['h1f_o2c'] < -0.002:
        pred = 2
    else:
        pred = 0
    # result = [[d7_val, d7_h2l, d7_o2c], [h24_val, h24_h2l ,h24_o2c], [h4_val, h4_h2l ,h4_o2c], [h1_val, h1_h2l ,h1_o2c]]
    result = [[d7_val, h24_val, h4_val, h1_val], [d7_h2l, h24_h2l, h4_h2l, h1_h2l], [d7_o2c, h24_o2c, h4_o2c, h1_o2c]]
    # result = [[h1_val, h24_o2c, h1_o2c]]
    return result

def sim(v, q):
     q = np.array(q)
     v = np.array(v)
     cosine = np.sum(q*v, axis=1)/(norm(q, axis=1)*norm(v, axis=1))
     return cosine.sum()


if __name__=="__main__":

    df = pd.read_pickle('embeddedCandle34.pkl')
    # df['vec'] = df.apply(lambda row: vec(row), axis=1)
    # df.to_pickle('embeddedCandle3.pkl')
    query = df.loc[13089]['vec']

    df['sim'] = df.apply(lambda row: sim(row['vec'], query), axis=1)

    real = df[df['sim'] ==1]['h1f_o2c']
    idx = real.index.to_list()[0]
    df = df.drop(idx)

    pred = df[df['sim'] > 0.99999]['h1f_o2c']


    p = [i for i in pred.tolist() if i>0]
    if len(p) > (len(pred)-len(p)):
        print('+')
    else:
        print('-')
    print('pred_num: ',len(pred))
    print('pred_mean: ',pred.mean())
    print('real: ',real.to_list()[0])


