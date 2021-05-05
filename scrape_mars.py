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
