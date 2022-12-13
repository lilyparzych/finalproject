#this creates the database, create cat table, create characteristics table
# Your name: Lily and Caitlin
# Your student id: 13965134
# Your email: clyeung@umich.edu
# List who you have worked with on this project: 

from catfacts import * 
import unittest
import sqlite3
import json
import os
import requests

def read_data(url): 
    r = requests.get(url)
    file = open("test-adopt.html" , "w")
    file.write(r.text)
    file.close()
    return r.json()

# def add_file(filename):
#     full_path = os.path.join(os.path.dirname(__file__), filename)
#     f = open(full_path)
#     file_data = f.read()
#     f.close()
#     json_data = json.loads(file_data)
#     return json_data

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# def get_cat_data(): 
#     api_key = "api_key=live_98hpkuYsR5QlXnvlnzJu8mEgHrFaBsw5dE7m8kwgAaqlboOKaGyfiK7fczjjjJQI"
#     response = requests.get(f"api.thecatapi.com/v1/images/search?limit=100&api_key={api_key}")

# def get_breed_data(dog_type):
#     breed = dog_type.lower()
#     #from the table get the id
#     response = requests.get(f"https://api.thecatapi.com/v1/images/search?breed_ids={breed.id}")

def make_cat_table(data, cur,conn):
    cur.execute('DROP TABLE IF EXISTS Cats')
    cur.execute('CREATE TABLE IF NOT EXISTS Cats (name TEXT PRIMARY KEY, breed_id TEXT, weight INTEGER, lifespan INTEGER, hypoallergenic INTEGER, country_code TEXT, origin TEXT)')

    #inserting into the table 
    for cat in data: 
        cur.execute('INSERT INTO Cats (name, breed_id, weight, lifespan, hypoallergenic, country_code, origin) VALUES (?,?,?,?,?,?,?)', (cat['name'], cat['id'], cat['weight']['metric'], cat['life_span'], cat['hypoallergenic'], cat['country_code'], cat['origin']))

    # Correct Typos on the Website

    conn.commit()

def make_characteristics_table(data, cur, conn): 
    cur.execute('DROP TABLE IF EXISTS Characteristics')
    cur.execute('CREATE TABLE IF NOT EXISTS Characteristics (name TEXT PRIMARY KEY, affection_level INTEGER, energy_level INTEGER, intelligence INTEGER, suppressed_tail INTEGER, temperament TEXT)')

    for cat in data: 
        cur.execute('INSERT INTO Characteristics (name, affection_level, energy_level, intelligence, suppressed_tail, temperament) VALUES (?,?,?,?,?,?)', (cat['name'], cat['affection_level'], cat['energy_level'], cat['intelligence'], cat['suppressed_tail'], cat['temperament']))
   
    conn.commit()

def rare_breed_search(cur, conn):
    #gets the affection level, energy level, intelligence, hypo-allergenic to compare for the bar graph
    html = get_html_file("https://thediscerningcat.com/getting-a-cat/")
    dict_of_info = get_cat_info_from_web(html)
    rare_breeds_list = get_rare_cat_breeds(dict_of_info)
    #['Scottish Fold', 'Norwegian Forest', 'Turkish Angora', 'American Bobtail', 
    # 'Burmilla', 'Devon Rex', 'Eyptian Mau', 'Tonkinese', 'Chartreux', 'Peterbald', 'Sokoke', 'Bombay', 'Selkirk Rex', 'American Wirehair', 'Sphynx', 'Korat', 'Ashera', 'Ocicat', 'Cornish Rex', 'Singapura', 'Havana Brown', 'Minskin']
    affection_level = []
    energy_level = []
    intelligence = []
    hypoallergenic = []

    cats_not_in_db = []
    
    for cat in rare_breeds_list:
        cur.execute('SELECT Characteristics.affection_level, Characteristics.energy_level, Characteristics.intelligence, Cats.hypoallergenic FROM Cats JOIN Characteristics ON Cats.name = Characteristics.name WHERE Cats.name = ?', (cat,))
        info = cur.fetchall()

        if len(info) == 0:
            cats_not_in_db.append(cat)
        else:
            description = info[0]
            affection_level.append(description[0])
            energy_level.append(description[1])
            intelligence.append(description[2])
            hypoallergenic.append(description[3])
    
    for cat in cats_not_in_db:
        rare_breeds_list.remove(cat)
   
    conn.commit()

    list_of_characteristics = []
    list_of_characteristics.append(affection_level)
    list_of_characteristics.append(energy_level)
    list_of_characteristics.append(intelligence)
    list_of_characteristics.append(hypoallergenic)

    return rare_breeds_list, list_of_characteristics

# Function to clean cat data for db
def clean_json_data(json_data):
    for cat in json_data:
        # Remove the word "Cat" from cat's name
        cat['name'] = cat['name'].replace(" Cat", "")

def main(): 
    #print(read_data("https://api.thecatapi.com/v1/breeds"))
    #grabbing data from cat breeds website
    json_data = read_data('https://api.thecatapi.com/v1/breeds')
    clean_json_data(json_data)
    cur,conn = open_database('cat_database.db')
    make_cat_table(json_data, cur, conn)
    make_characteristics_table(json_data, cur, conn)

    rare_breed_search(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)