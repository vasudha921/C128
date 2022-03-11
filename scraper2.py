import enum
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import csv

START_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("/Users/krishnamoorthypatlashankaranarayana/Desktop/Pythonclass/C127WebScraping/chromedriver")
browser.get(START_url)
time.sleep(10)

headers = ["name", "light_years_from_Earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink","planet_type","planet_radius","orbital_radius","orbital_period","eccentricity"]
planet_data = []  
new_planet_data = []

def scrape():
    
    for i in range(0,2):
        
       # while True:
    
        time.sleep(2)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        currentPageNo = int(soup.find_all("input", attrs = {"class", "page_num"})[0].get("value"))
        if currentPageNo < i:
            browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        elif currentPageNo > i:
            browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
        else:
             break



        for ul_tag in soup.find_all("ul", attrs= {"class", "exoplanet"}):
             print("you are inside scrape")
             li_tags = ul_tag.find_all("li")
             temp_list = []
             for index, li_tag in enumerate(li_tags):
                 if index == 0:
                     temp_list.append(li_tag.find_all("a")[0].contents[0])
                 else : 
                     try: 
                         temp_list.append(li_tag.contents[0])
                     except: 
                         temp_list.append("")
             hyper_link_li_tag = li_tags[0]
             temp_list.append("https://exoplanets.nasa.gov"+hyper_link_li_tag.find_all("a", href=True)[0]["href"])

             planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i}page done 1")


def scrape_more_data(hyper_link):
    print("you are inside scrape_more_data")
    try: 
        page = requests.get(hyper_link)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        temp_list = []  
        for tr_tag in soup.find_all("tr", attrs={"class", "factrow"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("div", attrs = {"class", "value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_planet_data.append(temp_list)

    except: 
        time.sleep(1)
        scrape_more_data(hyper_link)
            
scrape()
for index, data in enumerate(planet_data):
    scrape_more_data([5])
    print(f"{index + 1}page done 2")

final_planet_data = []

for index, data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data + new_planet_data_element)

with open("scrapper2.csv", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(headers)
        csv_writer.writerows(planet_data)



