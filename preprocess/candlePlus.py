import pandas as pd

def streeming(conf, data):

    data = data[data['Timestamp'] >= conf['start']]
    data = data[data['Timestamp'] < conf['end']]

    start, end, now = conf['start'], conf['end'], (conf['start']+604800)

    while(now < end):
        d7 = data[data['Timestamp'] >= (now-604800)]
        d7 = d7[d7['Timestamp'] < now]
        h24 = d7[d7['Timestamp'] >= (now-86400)]
        h4 = h24[h24['Timestamp'] >= (now-14400)]
        h1 = h4[h4['Timestamp'] >= (now-3600)]

        h1f = data[data['Timestamp'] >= now]
        h1f = h1f[h1f['Timestamp'] < (now+3600)]

        now += conf['step']

        yield {'d7':d7, 'h24':h24, 'h4':h4, 'h1':h1, 'h1f':h1f}

def dataToCandle(data):

    candle_plus = {}

    opens, closes = data['Open'].to_list(), data['Close'].to_list()
    candle_plus['open'], candle_plus['close'] = opens[0], closes[-1]
    candle_plus['timestamp'] = data['Timestamp'].to_list()[0]
    candle_plus['high'], candle_plus['low'] = data['High'].max(), data['Low'].min()
    candle_plus['volume_btc'] = data['Volume_(BTC)'].sum()
    candle_plus['volume_usd'] = data['Volume_(Currency)'].sum()

    data['Weighted_BTC_Price'] = data.apply(lambda row: row['Volume_(BTC)']*row['Weighted_Price'], axis=1)
    candle_plus['weighted_price'] = data['Weighted_BTC_Price'].sum() /data['Volume_(BTC)'].sum()

    candle_plus['h2l'] = (candle_plus['high'] / candle_plus['low']) -1
    if candle_plus['open'] >= candle_plus['close'] :
        candle_plus['o2c'] = (candle_plus['open'] / candle_plus['close']) -1
    else:
        candle_plus['o2c'] = ((candle_plus['close'] / candle_plus['open']) -1) * -1

    return candle_plus

if __name__=="__main__":

    dataset = pd.DataFrame(columns=['d7_timestamp', 'd7_high', 'd7_low', 'd7_open', 'd7_close', 'd7_volume_btc', 'd7_volume_usd', 'd7_weighted_price', 'd7_h2l', 'd7_o2c', 'h24_timestamp', 'h24_high', 'h24_low', 'h24_open', 'h24_close', 'h24_volume_btc', 'h24_volume_usd', 'h24_weighted_price', 'h24_h2l', 'h24_o2c', 'h4_timestamp', 'h4_high', 'h4_low', 'h4_open', 'h4_close', 'h4_volume_btc', 'h4_volume_usd', 'h4_weighted_price', 'h4_h2l', 'h4_o2c', 'h1_timestamp', 'h1_high', 'h1_low', 'h1_open', 'h1_close', 'h1_volume_btc', 'h1_volume_usd', 'h1_weighted_price', 'h1_h2l', 'h1_o2c', 'h1f_timestamp', 'h1f_high', 'h1f_low', 'h1f_open', 'h1f_close', 'h1f_volume_btc', 'h1f_volume_usd', 'h1f_weighted_price', 'h1f_h2l', 'h1f_o2c'])

    df = pd.read_csv('b.csv').dropna().reset_index(drop=True)
    # window_config = {'start':1499249760, 'end':1617148800, 'step':3600}
    window_config = {'start':1586247360, 'end':1617148800, 'step':3600}
    stream_data = streeming(window_config, df)
    while(True):
        try:
            time_frames_candle = {}
            time_frames = next(stream_data)
            for time_frame in time_frames.keys():
                if len(time_frames[time_frame]) == 0:
                    time_frames_candle[time_frame] = {'open':None, 'close':None, 'high':None, 'low':None, 'timestamp':None, 'volume_btc':None, 'volume_usd':None, 'weighted_price':None, 'h2l':None, 'o2c':None }
                    print('None')
                else:
                    candle_plus = dataToCandle(time_frames[time_frame].copy())
                    time_frames_candle[time_frame] = candle_plus

            row = {'d7_timestamp':time_frames_candle['d7']['timestamp'], 'd7_high':time_frames_candle['d7']['high'], 'd7_low':time_frames_candle['d7']['low'],'d7_open':time_frames_candle['d7']['open'], 'd7_close':time_frames_candle['d7']['close'], 'd7_volume_btc':time_frames_candle['d7']['volume_btc'], 'd7_volume_usd':time_frames_candle['d7']['volume_usd'], 'd7_weighted_price':time_frames_candle['d7']['weighted_price'], 'd7_h2l':time_frames_candle['d7']['h2l'], 'd7_o2c':time_frames_candle['d7']['o2c'],
                   'h24_timestamp':time_frames_candle['h24']['timestamp'], 'h24_high':time_frames_candle['h24']['high'], 'h24_low':time_frames_candle['h24']['low'],'h24_open':time_frames_candle['h24']['open'], 'h24_close':time_frames_candle['h24']['close'], 'h24_volume_btc':time_frames_candle['h24']['volume_btc'], 'h24_volume_usd':time_frames_candle['h24']['volume_usd'], 'h24_weighted_price':time_frames_candle['h24']['weighted_price'], 'h24_h2l':time_frames_candle['h24']['h2l'], 'h24_o2c':time_frames_candle['h24']['o2c'],
                    'h4_timestamp':time_frames_candle['h4']['timestamp'], 'h4_high':time_frames_candle['h4']['high'], 'h4_low':time_frames_candle['h4']['low'],'h4_open':time_frames_candle['h4']['open'], 'h4_close':time_frames_candle['h4']['close'], 'h4_volume_btc':time_frames_candle['h4']['volume_btc'], 'h4_volume_usd':time_frames_candle['h4']['volume_usd'], 'h4_weighted_price':time_frames_candle['h4']['weighted_price'], 'h4_h2l':time_frames_candle['h4']['h2l'], 'h4_o2c':time_frames_candle['h4']['o2c'],
                    'h1_timestamp':time_frames_candle['h1']['timestamp'], 'h1_high':time_frames_candle['h1']['high'], 'h1_low':time_frames_candle['h1']['low'],'h1_open':time_frames_candle['h1']['open'], 'h1_close':time_frames_candle['h1']['close'], 'h1_volume_btc':time_frames_candle['h1']['volume_btc'], 'h1_volume_usd':time_frames_candle['h1']['volume_usd'], 'h1_weighted_price':time_frames_candle['h1']['weighted_price'], 'h1_h2l':time_frames_candle['h1']['h2l'], 'h1_o2c':time_frames_candle['h1']['o2c'],
                    'h1f_timestamp':time_frames_candle['h1f']['timestamp'], 'h1f_high':time_frames_candle['h1f']['high'], 'h1f_low':time_frames_candle['h1f']['low'],'h1f_open':time_frames_candle['h1f']['open'], 'h1f_close':time_frames_candle['h1f']['close'], 'h1f_volume_btc':time_frames_candle['h1f']['volume_btc'], 'h1f_volume_usd':time_frames_candle['h1f']['volume_usd'], 'h1f_weighted_price':time_frames_candle['h1f']['weighted_price'], 'h1f_h2l':time_frames_candle['h1f']['h2l'], 'h1f_o2c':time_frames_candle['h1f']['o2c']
                   }
            dataset = dataset.append(row, ignore_index = True)
            if len(dataset) % 1000 == 0:
                print('len',len(dataset))
                dataset.to_pickle('candlePlus2.pkl')
        except:
            print("Done")
            break
