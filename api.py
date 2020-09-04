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
    if type_code == 0:
        print()
    if type_code == 1:
        df = query.getHotelsInProvince(search_id, filters, star_number)
    if type_code == 2:
        df = query.getHotelsInDistrict(search_id, filters, star_number)
    if type_code == 3:
        df = query.getHotelsWithName(search_id)

    for index, row in df.iterrows(): 
        data.append({
            "hotel_id": row[0],
            "name": row[1],
            "address": row[2],
            "logo": row[3],
            "star_number": row[4]
        })
    return jsonify(data)
    
#get hotels by hotel id(when click on specific hotel)
@app.route("/hotels/getByID/<int:hotel_id>", methods=["GET"])
def getByID(hotel_id):
    pass


#Run server
if __name__ == "__main__":
    app.run(debug=True)