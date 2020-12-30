# Web-Scraping-Challenge
This project builds a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page

<img src="https://github.com/kk-deng/Web-Scraping-Challenge/blob/main/Missions_to_Mars/static/header.jpg?raw=true">

## Web-Scraping

Four websites were used to scraped for Mars information.

1. <a href="https://mars.nasa.gov/news/">NASA Mars News</a>: latest News Title and Paragraph Text

2. <a href="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars">JPL Mars Space Images - Featured Image</a>: the url for JPL Featured Space Image

3. <a href="https://space-facts.com/mars/">Mars Facts</a>: use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

4. <a href="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars">Mars Hemispheres</a>: high resolution images for each of Mar's hemispheres

## Flask Web App with MongoDB

* A mars collection was created in mars_db MongoDB database with pymongo:

```python
# Create a mongodb connection through pymongo with db and collection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
collection = db.mars
```

* Two routes (`"/"` and `"/scrape"`) were set up:

```python
@app.route("/")
def index():
# This route was used to display a rendered html webpage with Jinja2, getting the lastest document from mars_db

@app.route("/scrape")
def scrape():
# This route runs the scrape python scripte to get data through splinter.browser and then insert to MongoDB
```

* In `scrape_mars.py` file, four feature functions were defined and called in the main function **scrape()** :
PS: For the last function, it might take up to 30s to fetch content depending on the Internet. **Do not refresh the webpage**.

```python
news_title, news_p = mars_news(browser, 
    "https://mars.nasa.gov/news/")

featured_image_url = featured_image(browser, 
    "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")

mars_fact_table = get_mars_fact(
    "https://space-facts.com/mars/")

list_hemispheres = get_hemispheres(
    "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
```

* All mars informations were stored in a dictionary which will be inserted into MongoDB later:
```python
mars_data = {
    "news_title"    :   news_title,
    "news_p"        :   news_p,
    "featured_img"  :   featured_image_url,
    "mars_fact"     :   mars_fact_table,
    "hemisphere_img":   list_hemispheres
}
```

* A Jinja2 if statement was used in `index.html` to display the div based on the availability of MongoDB collections:
```html

<!-- Notify user db has no record  -->
{% if mars_data == None %}
<div class="row">
...
</div>

<!-- If db has record, render page -->
{% else %}
<div class="row">
...
</div>

<!-- Enf of Jinja2 if statement -->
{% endif %}
```

## File Index

Following files are attached:

1. <a href="https://github.com/kk-deng/Web-Scraping-Challenge/blob/main/Missions_to_Mars/app.py">appy.py</a>: Main web-app script

2. <a href="https://github.com/kk-deng/Web-Scraping-Challenge/blob/main/Missions_to_Mars/mission_to_mars.ipynb">mission_to_mars.ipynb</a>: A Jupyter Notebook for the initial scraping

3. <a href="https://github.com/kk-deng/Web-Scraping-Challenge/blob/main/Missions_to_Mars/scrape_mars.py">scrape_mars.py</a>: Python script for `/scrape` route

4. <a href="https://github.com/kk-deng/Web-Scraping-Challenge/blob/main/Missions_to_Mars/templates/index.html">/templates/index.html</a>: A Jinja2 html for rendering

5. <a href="https://github.com/kk-deng/Web-Scraping-Challenge/tree/main/Missions_to_Mars/static">static</a>: CSS, Favicon and header image

6. <a href="https://github.com/kk-deng/Web-Scraping-Challenge/tree/main/Missions_to_Mars/Resources">Resources/chromedriver</a>: A chromdriver.exe (v87.0) for scraping engine

## View Screenshots
<img src="https://github.com/kk-deng/Web-Scraping-Challenge/blob/main/Screenshot/mars.png">
