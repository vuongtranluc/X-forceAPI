import requests
import json
import pandas as pd
import numpy as np
import query



def getPrice(hotel_id):
    df = query.getAllId(hotel_id)
    temp = ""
    for index, row in df.iterrows():
        temp += str(row['domain_id']) + "_" + str(row['domain_hotel_id']) + "_20200930,"
    temp = temp[:-1]
    url = "https://tripgle.data.tripi.vn/get_price"   
    data = {"hotel_ids": temp}
    headers = {"Authorization": "Basic UGhvZW5pWDpOTzEyRWs5Z1dLcEgxY3pnM1Z2dA=="}
    x = requests.post(url, data = json.dumps(data), headers = headers)
    return json.loads(x.text)

def getMinPrice(hotel_id):
    try:
        result = getPrice(hotel_id)
        if result == [] or len(result) == 0 or result is None:
            return -1
        minprice = 20000000000
        for domain_rs in result:
            for rs in domain_rs:
                if minprice > rs['final_amount']:
                    minprice = rs['final_amount'] 
        return minprice
    except:
        return -1