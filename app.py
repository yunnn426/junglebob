
# Flask 
from flask import Flask, render_template, jsonify, request, redirect, make_response
app = Flask(__name__)

# Port 번호
from var import PORT

# IP
from var import IP

# MongoDB ID/PW
from var import ID
from var import PW
from var import DBPORT

# pymongo DB 연결 pip in
from pymongo import MongoClient 
client = MongoClient('mongodb://' + ID + ':' + PW + '@' + IP, DBPORT)
db = client.jungleBob

# Global 변수
global userData

# 인덱스화면에서 메인화면으로
@app.route("/", methods=['GET'])
def toLogin() : 
    return redirect('http://' + IP + ":" + str(PORT) + '/today')

# 메인 페이지
from datetime import datetime

import time

def getDate():
    date = ""
    date += str(datetime.today().year) + "-"
    month = datetime.today().month
    if (month < 10):
        date += "0" + str(month) + "-"
    else:
        date += str(month) + "-"
    intdate = datetime.today().day
    if intdate < 10:
        date += "0"
        date += str(intdate)
    else:
        date += str(datetime.today().day)

    return date

@app.route("/today", methods=['GET'])
def today() : 

    ######### 금일 메뉴 데이터

    # 시스템 날짜 가져와 년-월-일 출력
    # 이후 날짜 비교를 위해 date 변수 그대로 사용
    date = getDate()
    daydate = date
    day = datetime.today().weekday() ## 요일
    if day == 0: daydate += "(월)"
    elif day == 1: daydate += "(화)"
    elif day == 2: daydate += "(수)"
    elif day == 3: daydate += "(목)"
    elif day == 4: daydate += "(금)"
    elif day == 5: daydate += "(토)"
    elif day == 6: daydate += "(일)"
    print(date)
    
    ## 기숙사 식당 메뉴 가져오기
    ### 점심
    dt_l_record = db.menus.find_one({"date": date, "place": "경기드림타워", "lunch": True})
    try:
        dt_l_menu = dt_l_record['menu']
        dt_l_menu = dt_l_menu.replace('\r\n', ', ')
    except: 
        return render_template('error.html')
    ### 저녁
    dt_d_record = db.menus.find_one({"date": date, "place": "경기드림타워", "lunch": False})
    try:
        dt_d_menu = dt_d_record['menu']
        dt_d_menu = dt_d_menu.replace('\r\n', ', ')
    except: 
        return render_template('error.html')

    # 경슐랭 메뉴 
    kcl_menu = "돈가스, 김밥, 덮밥, 한식, 햄버거, 타코"

    # E-스퀘어 메뉴
    esq_menu = "라면, 김밥, 덮밥, 국수, 돈까스, 아이스크림"

    return render_template('today.html', 
                           template_date = daydate,
                           template_dt_lunch_menu = dt_l_menu, template_dt_dinner_menu = dt_d_menu,
                           template_kcl_menu = kcl_menu, template_esq_menu = esq_menu)


if __name__ == "__main__" :
    app.run("0.0.0.0", port=PORT, debug=True)

