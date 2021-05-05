from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless = False)
def scrape():
    browser = init_browser()
    mars = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars['news_title'] = soup.find_all("div", class_ = "content_title")[1].text
    mars['news_paragraph'] = soup.find("div", class_ = "article_teaser_body").text

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url) 

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image=soup.find('a', class_='showimg')['href']

    mars['featured_image_url']= 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'+ image

    url ='https://space-facts.com/mars/'
    mars_tables = pd.read_html(url)

    df = mars_tables[0]

    mars['mars_facts'] = df.to_html(index = False, header = False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mh_names = []

    results = soup.find_all('div', class_='item')

    for result in results:
        hemisphere = result.find('h3')
        mh_names.append(hemisphere.text)

    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')

    title = []

    for result in results:
        title_result = result.find('a')['href']
        title_url = 'https://astrogeology.usgs.gov/' + title_result
        title.append(title_url)

    mh_img_url = []

    for link in title:
        browser.visit(link)
    
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        images = soup.find('img', class_='wide-image')['src']
        img_link = 'https://astrogeology.usgs.gov/' + images
    
        mh_img_url.append(img_link)

    hemi_dict = zip(mh_names, mh_img_url)
    mars['hemisphere_dictionary'] = []

    for title, img in hemi_dict:
        mars_dict = {}
        mars_dict['title'] = title
        mars_dict['img_url'] = img
        mars['hemisphere_dictionary'].append(mars_dict)

    return mars