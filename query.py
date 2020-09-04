import sqlite3
import load_data
import handle_input
import sort_and_filter
import pandas as pd
import numpy as np

phoenix_db = load_data.SqlCommon()

def searchProvince(string):
    string = handle_input.string_no_accent(string)
    phoenix_db = load_data.SqlCommon()  
    df = pd.DataFrame(phoenix_db.execute("select id, name from province where name_no_accent = \'" + string + "\'"))
    return df

def searchDistrict(string):
    string = handle_input.string_no_accent(string)
    phoenix_db = load_data.SqlCommon()  
    df = pd.DataFrame(phoenix_db.execute("select id, name from district where name_no_accent = \'" + string + "\'"))
    return df

def searchHotelName(string):
    phoenix_db = load_data.SqlCommon()  
    df = pd.DataFrame(phoenix_db.execute("select id, name from roothotel_info where name = \'" + string + "\'"))
    return df

def getHotelsInProvince(province_id, filters, star_number):
    sql = "select id, name, address, logo, star_number from roothotel_info where province_id = " + str(province_id)
    if star_number != "":
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
    domain_hotel_mapping_ids = sort_and_filter.handle_filter(filters)
    FinalMapping = pd.read_csv('FinalMapping.csv')
    df_result = pd.DataFrame(FinalMapping[FinalMapping['domain_hotel_mapping_id'].isin(domain_hotel_mapping_ids)])
    hotel_ids = df_result['hotel_id'].values
    df = pd.DataFrame(df[df[0].isin(hotel_ids)])
    return df

def getHotelsInDistrict(district_id, filters, star_number):
    sql = "select id, name, address, logo, star_number from roothotel_info where district_id = " + str(district_id)
    if star_number != "":
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
    domain_hotel_mapping_ids = sort_and_filter.handle_filter(filters)
    FinalMapping = pd.read_csv('FinalMapping.csv')
    df_result = pd.DataFrame(FinalMapping[FinalMapping['domain_hotel_mapping_id'].isin(domain_hotel_mapping_ids)])
    hotel_ids = df_result['hotel_id'].values
    df = pd.DataFrame(df[df[0].isin(hotel_ids)])
    return df

def getHotelsWithName(hotel_id):
    sql = "select id, name, address, logo, star_number from roothotel_info where id = " + str(hotel_id)
    phoenix_db = load_data.SqlCommon()  
    df = pd.DataFrame(phoenix_db.execute(sql))
    return df

def keywordSugesstion(keyword):
    pass

def releaseHotel(keyword):
    pass

def getByID(hotelID):
    pass

def get_overallScore(hotel_id):
    conn = sqlite3.connect('database1.db')
    sql = "SELECT * FROM finalScore WHERE hotel_id = ?" 
    score = conn.execute(sql, (hotel_id,)).fetchall()
    conn.close()

    return score

