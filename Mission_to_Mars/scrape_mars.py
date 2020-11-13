from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd


def scrape():

    mars = {}

    #NASA Mars News
    #Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. 

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    browser.is_element_visible_by_css('.item_list',wait_time=10)
    html = browser.html
    soup = bs(html, 'html.parser')


    news_title_div = soup.find_all('div', class_='bottom_gradient')[0]
    news_p_div = soup.find_all('div', class_='article_teaser_body')[0]

    ##############################
    #NEWS VARIABLES
    ##############################

    mars["news_title"] = news_title_div.h3.text
    mars["news_p"] = news_p_div.text

    #JPL Mars Space Images - Featured Image

    url =  'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    #Click through to full-image and more info to get url
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()
    browser.find_by_css('.main_image').click()

    ###############################
    #FEATURED IMAGE
    ##############################
    mars["featured_img"] = browser.url


    #Mars Facts
    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    table_df = pd.DataFrame(tables[0])
    table_html = table_df.to_html(header=False, index=False)

    ###############################
    #DATA TABLE
    ###############################
    mars['data_table'] = table_html


    #Mars Hemispheres

    #Get a list of all h3s on the page and then loop through them
    #use splinter to navigate to their respective image links

    url =  'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)

    html = browser.html

    soup = bs(html, 'html.parser')

    image_links = soup.find_all('h3')

    #########################
    #HEMISPHERE IMAGES
    #########################

    hemisphere_image_urls = []

    for link in image_links:
        
        browser.links.find_by_partial_text(link.text).click()
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        img_url_loc = soup.find('div', class_='downloads')
        
        img_url = img_url_loc.li.a['href']
        
        image_dict = {
            "title":link.text,
            "img_url":img_url
        }
        
        hemisphere_image_urls.append(image_dict)
        
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        
    mars['hemisphere_images'] = hemisphere_image_urls

    browser.quit()

    return mars
