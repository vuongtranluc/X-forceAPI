import sqlite3
import load_data
import handle_input
import sort_and_filter
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# phoenix_db = load_data.SqlCommon()

def searchProvince(string):
    string = "%%" + string + "%%"
    string = handle_input.string_no_accent(string)
    phoenix_db = load_data.SqlCommon()  
    df = pd.DataFrame(phoenix_db.execute("select id, name from province where name_no_accent like \'" + string + "\'"))
    return df

# print(searchProvince('ha noi'))

def searchDistrict(string):
    string = "%%" + string + "%%"
    string = handle_input.string_no_accent(string)
    phoenix_db = load_data.SqlCommon()  
    df = pd.DataFrame(phoenix_db.execute("select id, name from district where name_no_accent like \'" + string + "\'"))
    return df

def searchHotelName(string):
    string = "%%" + string + "%%"
    phoenix_db = load_data.SqlCommon()  
    df = pd.DataFrame(phoenix_db.execute("select id, name from roothotel_info where name like \'" + string + "\'"))
    FinalMapping = pd.read_csv('FinalMapping.csv')
    hotel_ids = FinalMapping['hotel_id'].values
    df = pd.DataFrame(df[df[0].isin(hotel_ids)])
    return df

def getHotelsInProvince(province_id, filters, star_number):
    sql = "select id, name, address, logo, star_number from roothotel_info where province_id = " + str(province_id)
    if star_number != "6":
        star_number = list(set(map(int, star_number.split('_'))))
        star_number.sort()
        sql_where = ""
        for s in star_number:
            if sql_where == "":
                sql_where = " and (star_number=" + str(s)
            else:
                sql_where += " or star_number=" + str(s)
        sql += sql_where + ")"
    # print(sql)
    phoenix_db = load_data.SqlCommon()  
    df = pd.DataFrame(phoenix_db.execute(sql))
    FinalMapping = pd.read_csv('FinalMapping.csv')
    if filters != "15":
        # print("hghj")
        domain_hotel_mapping_ids = sort_and_filter.handle_filter(filters)
        
        df_result = pd.DataFrame(FinalMapping[FinalMapping['domain_hotel_mapping_id'].isin(domain_hotel_mapping_ids)])
        hotel_ids = df_result['hotel_id'].values
        df = pd.DataFrame(df[df[0].isin(hotel_ids)])
    else:
        hotel_ids = FinalMapping['hotel_id'].values
        df = pd.DataFrame(df[df[0].isin(hotel_ids)])
    return df
# getHotelsInProvince(11, "1_2", "6")
def getHotelsInDistrict(district_id, filters, star_number):
    sql = "select id, name, address, logo, star_number from roothotel_info where district_id = " + str(district_id)
    if star_number != "6":
        star_number = list(set(map(int, star_number.split('_'))))
        star_number.sort()
        sql_where = ""
        for s in star_number:
            if sql_where == "":
                sql_where = " and (star_number=" + str(s)
            else:
                sql_where += " or star_number=" + str(s)
        sql += sql_where + ")"
    phoenix_db = load_data.SqlCommon()  
    df = pd.DataFrame(phoenix_db.execute(sql))
    # print(df)
    # return df
    FinalMapping = pd.read_csv('FinalMapping.csv')
    if filters != "15":
        # print("hghj")
        domain_hotel_mapping_ids = sort_and_filter.handle_filter(filters)
        
        df_result = pd.DataFrame(FinalMapping[FinalMapping['domain_hotel_mapping_id'].isin(domain_hotel_mapping_ids)])
        hotel_ids = df_result['hotel_id'].values
        df = pd.DataFrame(df[df[0].isin(hotel_ids)])
    else:
        hotel_ids = FinalMapping['hotel_id'].values
        df = pd.DataFrame(df[df[0].isin(hotel_ids)])
        print(df)
        # print("//////////////////////////////////////////////////////////")
    return df
# print(getHotelsInDistrict(483, "15", "6"))

def getHotelsWithName(hotel_id):
    sql = "select id, name, address, logo, star_number from roothotel_info where id = " + str(hotel_id)
    phoenix_db = load_data.SqlCommon()  
    df = pd.DataFrame(phoenix_db.execute(sql))
    return df


def get_overallScore(hotel_id):
    conn = sqlite3.connect('database1.db')
    sql = "SELECT * FROM finalScore WHERE hotel_id = ?" 
    score = conn.execute(sql, (hotel_id,)).fetchall()
    conn.close()
    return list(score[0])

# print(get_overallScore(15))

def getInformation(hotel_id):
    sql = "select id, name, address, logo, latitude, longitude from roothotel_info where id = " + str(hotel_id)
    phoenix_db = load_data.SqlCommon()  
    df = pd.DataFrame(phoenix_db.execute(sql), 
                      columns=['hotel_id', 'name', 'address', 'logo', 'latitude', 'longitude'])
    return df
    
def getAllId(hotel_id):
    FinalMapping = pd.read_csv('FinalMapping.csv')
    df = pd.DataFrame(FinalMapping[FinalMapping['hotel_id'] == hotel_id][['hotel_id', 'domain_id', 'domain_hotel_mapping_id']])
    df['domain_hotel_id'] = 0
    for index, row in df.iterrows():
        df.loc[df['domain_hotel_mapping_id'] == row['domain_hotel_mapping_id'], 'domain_hotel_id'] = getDomainHotelId(row['domain_hotel_mapping_id'])
    df = df.drop_duplicates(subset='domain_hotel_id', keep="first")
    return df
    
def getDomainHotelId(domain_hotel_mapping_id):
    sql = "select domain_hotel_id from hotel_mapping where id = \'" + domain_hotel_mapping_id + "\'"
    phoenix_db = load_data.SqlCommon()  
    df = pd.DataFrame(phoenix_db.execute(sql))
    return df[0][0]
    
# print(getDomainHotelId("95a50186-3167-4000-9f74-ce716fbb973f"))
# print(sum(get_overallScore(2), 3))
# print(get_overallScore(2))

def getDescription(hotel_id):
    df = getAllId(hotel_id)
    # print(df)
    domain_hotel_mapping_id = df['domain_hotel_mapping_id'].tolist()[-1]
    print(domain_hotel_mapping_id)
    sql = "select description from hotel_info where hotel_id = \'" + domain_hotel_mapping_id + "\'"
    phoenix_db = load_data.SqlCommon()  
    df = pd.DataFrame(phoenix_db.execute(sql))
    return (df[0][0])

# getDescription(54)
# print("ghj")

def keywordSugesstion(keyword):
    df = pd.read_csv("Search.csv")
    df["score"] = df["name_no_accent"].apply(lambda x: fuzz.token_set_ratio(x, keyword))
    df = df.sort_values(by=["score", "type_code"], ascending=[False, True])
    return df.head(3)


###
### Luc's update 10/9/2020
###

def getDomainHotelMappingID(hotelID):
    conn = sqlite3.connect('FinalMapping.db')
    sql = "SELECT domain_hotel_mapping_id FROM FinalMapping WHERE hotel_id = ?" 
    # mappingID is a list of tuple, each tuple has a form (domainHotelMappingId,)
    mappingID = conn.execute(sql, (hotelID,)).fetchall()
    conn.close()

    finalMappingID = []
    for i in range(len(mappingID)):
        rawID = mappingID[i][0]
        finalMappingID.append(rawID[:(len(rawID)-1)])

    return finalMappingID
# print(getDomainHotelMappingID(5))

def getMinPrice(domain_hotel_id):
    try:
        sql = "Select final_amount_min from hotel_price_daily where domain_hotel_id = {0} order by final_amount_min limit 1".format(domain_hotel_id)
        phoenix_db = load_data.SqlCommon()
        df = pd.DataFrame(phoenix_db.execute(sql))
        return df[0][0]
    except:
        return -1
    
# print()

def collectMinPrice(hotel_id):
    try:
        domainHotelMappingID = getDomainHotelMappingID(hotel_id)
        # print("DomainHotelMapping: ", domainHotelMappingID)
        domainHotelID = []
        print(domainHotelMappingID)
        for i in domainHotelMappingID:
            domainHotelID.append(getDomainHotelId(i))
        # print("domainHotelID: ", domainHotelID)
        minPrice = []
        for y in domainHotelID:
            # print("domainHotelID: ", y)
            minPrice.append((y, getMinPrice(y)))
            
        return findMinPrice(minPrice)
    except:
        return [(-1,-1)]

def findMinPrice(ListPrice):
    try: 
        minPrice = ListPrice[0]
        for i in ListPrice:
            if i[1] < minPrice[1]:
                minPrice = i
        return minPrice
    except:
        return (-1, -1)


def getMinPrice(hotel_id):
    df = pd.read_csv("minPrice.csv")
    try:
        return df[df['hotel_id'] == hotel_id]['min_price'].tolist()[0]
    except:
        return -1

def getURL(domain_hotel_id):
    phoenix_db = load_data.SqlCommon()
    sql = "Select url from hotel_info where domain_hotel_id = {0}".format(domain_hotel_id)
    df = pd.DataFrame(phoenix_db.execute(sql))

    try:
        return df[0][0]

    except:
        return -1


def addHotel(data, row):
    data.append({
        "hotel_id": row[0],
        "name": row[1], 
        "address": row[2],
        "logo": row[3],
        "star_number": row[4],
        "overall_score": round(get_overallScore(row[0])[3], 1),
        "point_hidden": round(sum(get_overallScore(row[0])[3:]), 2)            
    })