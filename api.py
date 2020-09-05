from flask import Flask, request, jsonify
import os
import query, load_data, sort_and_filter
import pandas as pd
import numpy as np

#init app
app = Flask(__name__)

#url to get overscore by hotel_id
@app.route("/hotels/overallScore/<int:hotel_id>",methods=["GET"])
def get_overalScore(hotel_id):
    rows = query.get_overallScore(hotel_id)
    data = []
    
    for r in rows: 
        data.append({
            "overall_score": r[3],
            "location_score": r[4],
            "sleep_quality_score":r[5],
            "meal_score": r[6],
            "service_score": r[7],
            "cleanliness_score": r[8]
        })

    return jsonify(data)

#recomment base on keywords
@app.route("/hotels/keywordsuggestion/<keyword>", methods=["GET"])
def keywordSugesstion(keyword):
    # type_code
    # 0: default
    # 1: province
    # 2: district
    # 3: hotel name
    data = []
    df = query.searchProvince(keyword)
    for index, row in df.iterrows(): 
        data.append({
            "search_id": row[0],
            "name": row[1],
            "type_code": 1
        })
    if len(data) != 0:
        return jsonify(data)
    df = query.searchDistrict(keyword)
    for index, row in df.iterrows(): 
        data.append({
            "search_id": row[0],
            "name": row[1],
            "type_code": 2
        })
    if len(data) != 0:
        return jsonify(data)
    df = query.searchHotelName(keyword)
    for index, row in df.iterrows(): 
        data.append({
            "search_id": row[0],
            "name": row[1],
            "type_code": 3
        })
    return jsonify(data)

#release hotel(when click search)
@app.route("/hotels/gethotels/<int:search_id>/<int:type_code>/<int:page_number>/<filters>/<star_number>", methods=["GET"])
def finalSearch(search_id, type_code, page_number, filters, star_number):
    data = []
    if type_code == 1:
        df = query.getHotelsInProvince(search_id, filters, star_number)
    if type_code == 2:
        df = query.getHotelsInDistrict(search_id, filters, star_number)
    if type_code == 3:
        df = query.getHotelsWithName(search_id)

    df[5] = 8
    
    for index, row in df.iterrows(): 
        data.append({
            "hotel_id": row[0],
            "name": row[1],
            "address": row[2],
            "logo": row[3],
            "star_number": row[4],
            "overall_score": round(query.get_overallScore(row[0])[3], 1),
            "point_hidden": round(sum(query.get_overallScore(row[0])[3:]), 2)
        })
    data.sort(reverse=True, key=lambda row: row["point_hidden"])
    return jsonify(data)
    
#get hotels by hotel id(when click on specific hotel)
@app.route("/hotels/getByID/<int:hotel_id>", methods=["GET"])
def getByID(hotel_id):
    data = []
    df = query.getInformation(hotel_id)
    for index, row in df.iterrows(): 
        arr = query.get_overallScore(row['hotel_id'])
        data.append({
            "hotel_id": row['hotel_id'],
            "name": row['name'],
            "address": row['address'],
            "logo": row['logo'],
            "star_number": arr[1],
            "overall_score": round(arr[3], 1),
            "location_score": round(arr[4], 1),
            "sleep_quality_score": round(arr[5], 1),
            "meal_score": round(arr[6], 1),
            "service_score": round(arr[7], 1),
            "cleanliness_score": round(arr[8], 1),
            "description": query.getDescription(row['hotel_id'])
        })
    return jsonify(data)

@app.route("/hotels/getAllId/<int:hotel_id>")
def getAllId(hotel_id):
    data = []
    df = query.getAllId(hotel_id)
    for index, row in df.iterrows(): 
        data.append({
            "hotel_id": row['hotel_id'],
            "domain_id": row['domain_id'],
            "domain_hotel_mapping_id":row['domain_hotel_mapping_id'],
            "domain_hotel_id": row['domain_hotel_id']
        })

    return jsonify(data)

#Run server
if __name__ == "__main__":
    app.run(debug=True)