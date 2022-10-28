from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import json
import requests

FORM = "https://forms.gle/gtpW28dduBADmyAB7"
ZILLOW = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.43927955627441%2C%22east%22%3A-121.89957618713379%2C%22south%22%3A37.56791597927116%2C%22north%22%3A37.87641164462166%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"
CHROME_DRIVER_PATH = "C:/ChromeDriver/chromedriver.exe"

#  Scrape all the listings from the Zillow web address
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
           'Accept-Language': 't-IT,it;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate'}

response = requests.get(url=ZILLOW, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

data = soup.find_all(name="script", attrs={"type": "application/json"})[1].text.replace("<!--", "").replace("-->", "")
data = json.loads(data)["cat1"]["searchResults"]["listResults"]

links = [item['detailUrl'] if '/b/' not in item['detailUrl'] else "https://www.zillow.com"+item['detailUrl'] for item in data]
prices = [item["units"][0]["price"][:6] if item.get("price") is None else item["price"][:6] for item in data]
addresses = [item['address'] for item in data]

# Fill the forms
driver = webdriver.Chrome(CHROME_DRIVER_PATH)
for i in range(len(links)):
    driver.get(FORM)
    sleep(3)
    address = driver.find_elements(By.CSS_SELECTOR, "div.AgroKb input")[0]
    address.send_keys(addresses[i])
    price = driver.find_elements(By.CSS_SELECTOR, "div.AgroKb input")[1]
    price.send_keys(prices[i])
    link = driver.find_elements(By.CSS_SELECTOR, "div.AgroKb input")[2]
    link.send_keys(links[i])
    driver.find_element(By.CSS_SELECTOR, "div.lRwqcd div").click()

