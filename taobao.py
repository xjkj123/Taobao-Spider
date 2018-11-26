import requests, json, pandas, sqlite3, tqdm


def GetCommodity(Commodity):
    li = []
    for x in tqdm.tqdm(range(0, 100)):
        data = 'event_submit_do_new_search_auction=1&' \
               '_input_charset=utf-8&' \
               'topSearch=1&' \
               'atype=b&' \
               'searchfrom=1&' \
               'action=home%3Aredirect_app_action&' \
               'from=1&' \
               'q=' + Commodity + '&' \
                                  'sst=1&' \
                                  'n=20&' \
                                  'buying=buyitnow&' \
                                  'm=api4h5&' \
                                  'token4h5=&' \
                                  'abtest=18&' \
                                  'wlsort=18&' \
                                  'page=%d' % x
        url = '''https://s.m.taobao.com/search?''' + data
        ret = requests.get(url)
        x = json.loads(ret.text)['listItem']
        for sp in x:
            li.append(sp)
    df = pandas.DataFrame(li)
    return df


if __name__ == '__main__':
    Commodity = '五年高考三年模拟'
    df = GetCommodity(Commodity)
    con = sqlite3.connect('taobao.db')
    df = df[['name', 'nick', 'location', 'originalPrice', 'price', 'sold', 'zkType']]
    df.to_sql(con=con, name=Commodity, if_exists='append')
