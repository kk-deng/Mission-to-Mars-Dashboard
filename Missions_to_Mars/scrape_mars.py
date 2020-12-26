# Dependencies
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup as bs
import splinter

def mars_news(browser, url):
    # -------- NASA Mars News --------
    # Use chromedriver to open NASA webpage and parse html to soup
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    html_page = browser.html
    soup = bs(html_page, "html.parser")

    # Filter content by looking for content div
    content = soup.find("div", class_='content_page')

    try:
        # Get a list of all article titles
        news_title = content.find_all("div", class_="content_title")[0].text.strip()

        # Get a list of all article teasers
        news_p = content.find_all("div", class_="article_teaser_body")[0].text.strip()
    except:
        news_title = news_p = "Unable to load news. Please Retry"

    return (news_title, news_p)

def featured_image(browser, url):
    # -------- JPL Mars Space Images - Featured Image --------
    # Use chromedriver to open JPL webpage and parse html to soup
    browser.visit(url)
    browser.is_element_present_by_css("a.button", wait_time=1)

    try:
        # Get the large size of the featured image
        # Click the full_image button
        browser.find_by_id("full_image").click()

        # Click more info button to get to the information page
        browser.find_by_text("more info     ").click()

        # Get the large size of this image
        # browser.is_element_present_by_css("img.main_image", wait_time=1)
        image_html = browser.html
        image_soup = bs(image_html, "html.parser")

    
        # Get the relative link from img tag with class 'main_image'
        featured_image_rel = image_soup.find("img", class_="main_image")["src"]

        # Combine the relative link with the website url
        featured_image_url = "https://www.jpl.nasa.gov" + featured_image_rel
    except:
        featured_image_url = "Unable to load featured image. Please Retry"
    
    return featured_image_url

def get_mars_fact(browser, url):
    # -------- Mars Facts --------
    # Get first table from the webpage with pandas
    df_mars_fact = pd.read_html(url, encoding="UTF-8")[0]

    # Rename columns and reset index
    df_mars_fact.columns = ["Description", "Mars"]
    df_mars_fact.set_index("Description", inplace=True)

    # Export the Mars fact table
    return df_mars_fact.to_html(index=False, 
                                justify="left", 
                                classes="table table-striped table-hover table-sm", 
                                border=3)

def get_hemispheres(browser, url):
    # -------- Mars Hemispheres --------
    # Get the soup from the main page of Mars Hemispheres
    usgs_response = requests.get(url)
    usgs_soup = bs(usgs_response.text, "html.parser")

    # From the soup above, collect all Mars Hemisphere url into a url list
    article_urls = usgs_soup.find_all("a", class_="itemLink product-item")
    url_domain = url.split("/search/")[0]
    hemisphere_image_urls = []

    # Create a session to keep the connection open and configured
    session = requests.Session()

    for article in article_urls:
        # Collect each article title text, and make a url for each article
        article_title = article.text
        article_url = url_domain + article["href"]
        print("Loading: " + article_url)

        # Get into each article url to get image url
        article_response = session.get(article_url)
        # browser.visit(article_url)
        # article_response = browser.html
        article_soup = bs(article_response.text, "html.parser")
        
        # Find the <a> tag with text 'Sample" in the page, then get its img url
        img_full_url = article_soup.find("a", string="Sample")["href"]

        # Append the new dict to the img list
        hemisphere_image_urls.append({"title": article_title, "img_url": img_full_url})
    
    return hemisphere_image_urls

def scrape():
    # Setting Chrome Driver exe file path
    executable_path = {"executable_path" : "Resources/chromedriver.exe"}
    browser = splinter.Browser("chrome", **executable_path)

    news_title, news_p = mars_news(browser, 
        "https://mars.nasa.gov/news/")

    featured_image_url = featured_image(browser, 
        "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    
    #Close browser
    browser.quit()
 
    mars_fact_table = get_mars_fact(browser, 
        "https://space-facts.com/mars/")

    list_hemispheres = get_hemispheres(browser, 
        "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")


    # Gather all scraped data into a python dictionary
    mars_data = {
        "news_title"    :   news_title,
        "news_p"        :   news_p,
        "featured_img"  :   featured_image_url,
        "mars_fact"     :   mars_fact_table,
        "hemisphere_img":   list_hemispheres
    }

    return mars_data
