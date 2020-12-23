# Dependencies
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup as bs
import splinter

# Setting Chrome Driver exe file path
executable_path = {"executable_path" : "Resources/chromedriver.exe"}
browser = splinter.Browser("chrome", **executable_path)

# -------- NASA Mars News --------
# Use chromedriver to open NASA webpage and parse html to soup
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
html_page = browser.html
soup = bs(html_page, "html.parser")

# Filter content by looking for content div
content = soup.find("div", class_='content_page')

# Get a list of all article titles
titles = content.find_all("div", class_="content_title")
print(titles[0].text.strip())

# Get a list of all article teasers
article_teasers = content.find_all("div", class_="article_teaser_body")
print(article_teasers[0].text)

# -------- JPL Mars Space Images - Featured Image --------
# Use chromedriver to open JPL webpage and parse html to soup
jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(jpl_url)
jpl_html = browser.html
jpl_soup = bs(jpl_html, "html.parser")

# Get the front page image url
image_rel_url = jpl_soup.find("article", class_="carousel_item")["style"]
url_1 = jpl_url.split("?")[0]
url_2 = image_rel_url.split("/spaceimages/")[1].split("'")[0]
featured_image = url_1 + url_2


# Get the large size of the featured image
# Click the full_image button
browser.find_by_id("full_image").click()

# Click more info button to get to the information page
browser.find_by_text("more info     ").click()

# Get the large size of this image
image_html = browser.html
image_soup = bs(image_html, "html.parser")
featured_image_large = image_soup.find("img", class_="main_image")["src"]

# Combine the relative link with the website url
featured_image_url = jpl_url.split("/spaceimages")[0] + featured_image_large


# -------- Mars Facts --------
# Get all tables from the webpage with pandas
mars_url = "https://space-facts.com/mars/"
mars_fact_tables = pd.read_html(mars_url)

# Get the first table and print it out.
df_mars_fact = mars_fact_tables[0]
df_mars_fact

# Rename columns
df_mars_fact.columns = ["Description", "Mars"]
df_mars_fact

# Export the Mars fact table
df_mars_fact.to_html("mars_fact.html", index=False)


# -------- Mars Hemispheres --------
# Get the soup from the main page of Mars Hemispheres
usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
usgs_response = requests.get(usgs_url)
usgs_soup = bs(usgs_response.text, "html.parser")

# From the soup above, collect all Mars Hemisphere url into a list
article_urls = usgs_soup.find_all("a", class_="itemLink product-item")
url_domain = usgs_url.split("/search/")[0]
hemisphere_image_urls = []

for article in article_urls:
    # Collect each article title text, and make a url for each article
    article_title = article.text
    article_url = url_domain + article["href"]
    print(article_url)
    
    # Get into each article url to get image url
    article_response = requests.get(article_url)
    article_soup = bs(article_response.text, "html.parser")
    
    # Find the <a> tag with text 'Sample" in the page, then get its img url
    img_full_url = article_soup.find("a", string="Sample")["href"]
    print(img_full_url)

    # Append the new dict to the img list
    hemisphere_image_urls.append({"title": article_title, "img_url": img_full_url})
    