from flask import Flask, render_template, redirect
# from flask_pymongo import PyMongo
import scrape_mars
import pymongo

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
collection = db.mars

# app.config["MONGO URI"] = "mongodb://localhost:27017/mars_db"
# mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = collection.find_one()
    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scrape():
    scrape_data = scrape_mars.scrape()
    collection.insert_one(scrape_data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)