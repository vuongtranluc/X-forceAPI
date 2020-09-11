from flask import Flask, request, jsonify, render_template
import os
import query, load_data, sort_and_filter, handle_input
import pandas as pd
import numpy as np
import json

#init app
app = Flask(__name__)

#recomment base on keywords
@app.route("/hotels/keywordsuggestion/<keyword>", methods=["GET"])
def keywordSugesstion(keyword):
    # type_code
    # 0: default
    # 1: province
    # 2: district
    # 3: hotel name
    keyword = " ".join(keyword.split())
    keyword = handle_input.string_no_accent(keyword)
    data = []
    df = query.keywordSugesstion(keyword)
    for index, row in df.iterrows(): 
        data.append({
            "search_id": row['search_id'],
            "name": row['name'],
            "type_code":row['type_code'],
            "score": row['score']
        })

    return app.response_class(json.dumps(data),mimetype='application/json')

#release hotel(when click search)
@app.route("/hotels/gethotels/<search_id>/<int:type_code>/<filters>/<star_number>", methods=["GET"])
def finalSearch(search_id, type_code, filters, star_number):
    filters = filters.strip()
    search_id = search_id.strip()
    star_number = star_number.strip()
    data = []
    if type_code == 0:
        search_id = " ".join(search_id.split())
        search_id = handle_input.string_no_accent(search_id)
        df = query.keywordSugesstion(search_id)
        search_id = df.head(1)['search_id'].tolist()[0]
        type_code = df.head(1)['type_code'].tolist()[0]
    if type_code == 1:
        search_id = int(search_id)
        df = query.getHotelsInProvince(search_id, filters, star_number)
    if type_code == 2:
        search_id = int(search_id)
        df = query.getHotelsInDistrict(search_id, filters, star_number)
    if type_code == 3:
        search_id = int(search_id)
        df = query.getHotelsWithName(search_id)
    
    for index, row in df.iterrows(): 
        ##
        ## Luc update find min price 
        ##
        # print(row[0])
        # minPrice = query.collectMinPrice(int(row[0]))
        # print(minPrice[0], minPrice[1])
        # # minPrice = (0, 0)

        data.append({
            "min_price": query.getMinPrice(row[0]),
            "address": row[2],
            "logo": row[3],
            "star_number": row[4],
            "overall_score": round(query.get_overallScore(row[0])[3], 1),
            "point_hidden": round(sum(query.get_overallScore(row[0])[3:]), 2)

        })
    if data != []:
        data.sort(reverse=True, key=lambda row: row["point_hidden"])
    if len(data) > 30:
        data = data[:30]

    return app.response_class(json.dumps(data),mimetype='application/json')
    # print(data)
    # return jsonify(data)
    
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
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/hotels/getAllId/<int:hotel_id>", methods=["GET"])
def getAllId(hotel_id):
    data = []
    df = query.getAllId(hotel_id)
    for index, row in df.iterrows(): 
        data.append({
            "hotel_url": query.getURL(row['domain_hotel_id']),
            "hotel_id": row['hotel_id'],
            "domain_id": row['domain_id'],
            "domain_hotel_mapping_id":row['domain_hotel_mapping_id'],
            "domain_hotel_id": row['domain_hotel_id']
        })
    # print("??????")
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/", methods=["GET"])
def home():
    return render_template('instruction.html')

#Run server
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
