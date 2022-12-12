
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import json 
import unittest
import os
import requests
import random

def read_data(url): 
    r = requests.get(url)
    file = open("test-adopt.html" , "w")
    file.write(r.text)
    file.close()
    return r.json()

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def count_origin(json_data): 
    dict_of_origins = {}
    for cat in json_data:
        origin = cat['origin']
        if origin not in dict_of_origins.keys(): 
            dict_of_origins[origin] = 1
        else: 
            dict_of_origins[origin] += 1
    
    return dict_of_origins

def pie_chart(dict_of_origins):
    #this shows us the origin of all the cats 
    labels = dict_of_origins.keys()
    sizes = []
    num_of_countries = len(labels)

    for label in labels: 
        sizes.append(dict_of_origins[label])

    explode = (0,0,0.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    print(len(explode))

    startangle = 360/num_of_countries
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode = explode, labels = labels, 
    autopct = '%1.1f%%', shadow = False, startangle= startangle)

    ax1.axis('equal')

    plt.show()

def main(): 
    json_data = read_data('https://api.thecatapi.com/v1/breeds')
    cur,conn = open_database('cat_database.db')
    num_of_countries = count_origin(json_data)
    pie_chart(num_of_countries)

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)