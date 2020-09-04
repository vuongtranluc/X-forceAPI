from flask import Flask, request, jsonify
import os
import query

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
@app.route("/hotels/keywordSugestion/<keyword>", methods=["GET"])
def keywordSugesstion(keyword):
    pass

#release hotel(when click search)
@app.route("/hotels/gethotels/<keyword>", methods=["GET"])
def releaseHotel(keyword):
    # test
    return 1


#get hotels by hotel id(when click on specific hotel)
@app.route("/hotels/getByID/<int:hotel_id>", methods=["GET"])
def getByID(hotel_id):
    pass


#Run server
if __name__ == "__main__":
    app.run(debug=True)