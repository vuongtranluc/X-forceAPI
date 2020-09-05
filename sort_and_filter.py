import pandas as pd
import numpy as np
import handle_input, load_data
import load_data


def handle_filter(filters):
    filters = list(set(map(int, filters.split('_'))))
    filters.sort()
    sql = "select hm.id from hotel_mapping hm join hotel_quality hq on hm.id = hq.hotel_id join hotel_facility hf on hm.id = hf.hotel_id join hotel_info hi on hm.id = hi.hotel_id join hotel_service hs on hm.id = hs.hotel_id"
    sql_where = ""
    array_filter = ["", "currency_exchange = 1", "room_service_24_hour = 1", "elevator = 1", 
                    "safely_deposit_boxed = 1", "luggage_storage = 1", "airport_transfer = 1",
                    "restaurants = 1", "concierge = 1", "front_desk_24_hour = 1", "bar = 1",
                    "laundry_service = 1", "(is_free_car_park = 1 or is_internet_free_wifi_in_area = 1 or is_internet_free_wifi_in_room = 1)",
                    "tours = 13", "relax_outdoor_pool = 1"]
    for f in filters:
        if (sql_where == ""):
            sql_where = " where " + array_filter[f]
        else:
            sql_where += " and " + array_filter[f]
    sql += sql_where
    phoenix_db = load_data.SqlCommon()  
    df_filter = pd.DataFrame(phoenix_db.execute(sql))
    return df_filter[0].values
   

""" 
    filter-code:
    --------------------------------------
    currency_exchange       = 1
    room_service_24_hour    = 2
    elevator                = 3
    safely_deposit_boxed    = 4
    luggage_storage         = 5
    airport_transfer        = 6
    restaurants             = 7
    concierge               = 8
    front_desk_24_hour      = 9
    bar                     = 10
    laundry_service         = 11
    wifi                    = 12
    tours                   = 13
    relax_outdoor_pool      = 14
    --------------------------------------
    star_number (-1: none, !=: 1-2-3-4-5)
"""