import sqlite3
import load_data

phoenix_db = load_data.SqlCommon()

def keyWordSugestion(keyword):
    pass

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



if __name__ == "__main__":
    print(get_overallScore(4))