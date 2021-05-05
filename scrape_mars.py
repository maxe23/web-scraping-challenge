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