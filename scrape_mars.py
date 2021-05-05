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
