from flask import Flask, request, render_template
import pymysql

db = pymysql.connect("localhost", "root", "9907", "test")

from flask import Flask
app = Flask(__name__)

@app.route('/')
def someName():
    cursor = db.cursor()
    sql = "SELECT * FROM device_manager"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('index.html', title='크롤링데모', results=results)

if __name__ == '__main__':
    app.run(debug=True)