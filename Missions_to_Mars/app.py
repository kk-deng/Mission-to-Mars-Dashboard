from flask import Flask, render_template, redirect
import scrape_mars
import pymongo

app = Flask(__name__)

# Create a mongodb connection through pymongo with db and collection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
collection = db.mars

# Root route for homepage
@app.route("/")
def index():
    mars_data = collection.find_one(sort=[( '_id', pymongo.DESCENDING )])
    return render_template("index.html", mars_data = mars_data)

# Scrape route for web-scraping
@app.route("/scrape")
def scrape():
    scrape_data = scrape_mars.scrape()
    collection.insert_one(scrape_data)
    return redirect("/")

# Main function
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)