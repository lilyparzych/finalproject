

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests
import json

def get_html_file(url): 
    r = requests.get(url)
    file = open("test.html" , "w")
    file.write(r.text)
    file.close()
    return r.text
    
def get_cat_info_from_web(html_text): 

    soup = BeautifulSoup(html_text, 'html.parser')

    breed_char = soup.find_all('p', class_="has-text-color", style = "color:#138e9b")

    dict_of_info = {}
    for char in breed_char: 
        fun_fact = char.find('a', class_="ek-link")
        url = fun_fact.get('href')
        # print(fun_fact.text)
        # print(url)
        dict_of_info[fun_fact.text] = url
   
    return dict_of_info

def get_rare_cat_breeds(dict_of_info):
    rare_cat_breeds = []
    url = dict_of_info['Rare Cat Breeds']
    soup = BeautifulSoup(get_html_file(url), 'html.parser')

    page_info = soup.find_all('h3')
    for info in page_info: 
        cat_breed = info.find('span')
        if cat_breed != None: 
            cat = cat_breed.text

            reg_ex = r"\b(?!Cat|Breed|\d|\.)\b\S+"
            cats = re.findall(reg_ex, cat)
            
            full_name = " ".join(cats)
            rare_cat_breeds.append(full_name)

    return rare_cat_breeds

def get_expensive_cat_breeds(dict_of_info):
    expensive_cat_breeds = []
    url = dict_of_info['9 Expensive Cat Breeds']
    soup = BeautifulSoup(get_html_file(url), 'html.parser')

    page_info = soup.find_all('h3')
    for info in page_info: 
        cat_breed = info.find('span')
        if cat_breed != None: 
            cat = cat_breed.text

            reg_ex = r"\b(?!Cat|Breed|\d|\.)\b\S+"
            cats = re.findall(reg_ex, cat)
            
            full_name = " ".join(cats)
            expensive_cat_breeds.append(full_name)

    return expensive_cat_breeds 

#PART 3: PROCESS THE DATA 

#SELECT the rare cats (from adopt a cat)
#SELECT the expensive cats (from adopt a cat)

#correlation between most expensive cat breeds and affection and energy level 
# why the expensive cats are expensive? 
# why the rare cats are rare?

def main(): 
    html = get_html_file("https://thediscerningcat.com/getting-a-cat/")
    #print(get_cat_info_from_web(html))
    # print("rare_cat_breeds")
    # print("------------------")
    print(get_rare_cat_breeds(get_cat_info_from_web(html)))
    # print("expensive_cat_breeds")
    # print("------------------")
    # print(get_expensive_cat_breeds(get_cat_info_from_web(html)))
    

main()
