# Your name: Caitlin Liz Yeung
# Your student id: 13965134
# Your email: clyeung@umich.edu
# List who you have worked with on this project:

from PetFinder import * 
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

    conn.commit()

def make_characteristics_table(data, cur, conn): 
    cur.execute('DROP TABLE IF EXISTS Characteristics')
    cur.execute('CREATE TABLE IF NOT EXISTS Characteristics (name TEXT PRIMARY KEY, affection_level INTEGER, energy_level INTEGER, intelligence INTEGER, suppressed_tail INTEGER, temperament TEXT)')

    for cat in data: 
        cur.execute('INSERT INTO Characteristics (name, affection_level, energy_level, intelligence, suppressed_tail, temperament) VALUES (?,?,?,?,?,?)', (cat['name'], cat['affection_level'], cat['energy_level'], cat['intelligence'], cat['suppressed_tail'], cat['temperament']))
    
    conn.commit()

#PART 3: PROCESS THE DATA 
def rare_breed_search(data, cur, conn):
    #JOIN tables --> name, hypoallergenic, lifespan, origin, energy_level, intelligence, 
    # cur.execute('DROP TABLE IF EXISTS RareChar')
    # cur.execute('CREATE TABLE IF NOT EXISTS RareChar (name TEXT PRIMARY KEY, hypoallergenic INTEGER, lifespan INTEGER, energy_level INTEGER, intelligence INTEGER')
    html = get_html_file("https://thediscerningcat.com/getting-a-cat/")
    dict_of_info = get_cat_info_from_web(html)
    rare_breeds_list = get_rare_cat_breeds(dict_of_info)
    print(rare_breeds_list)

    for cat in rare_breeds_list:
        cur.execute('SELECT Cats.name, Cats.hypoallergenic, Cats.lifespan, Cats.origin, Characteristics.energy_level, Characteristics.intelligence FROM Cats JOIN Characteristics ON Cats.name = Characteristics.name WHERE Cats.name = ?', (cat,))
 
    # for cat in data:
    #     cur.execute('SELECT Cats.name, Cats.hypoallergenic, Cats.lifespan, Cats.origin, Characteristics.energy_level, Characteristics.intelligence FROM Cats JOIN Characteristics ON Cats.name = Characteristics.name WHERE Cats.name = ?', (cat['name'],))
        result = cur.fetchall()
        print(result)
        # if cat['name'] in rare_breeds_list: 
        #     # cur.execute('SELECT Cats.name, Cats.hypoallergenic, Cats.lifespan, Cats.origin, Characteristics.energy_level, Characteristics.intelligence FROM Cats JOIN Characteristics ON Cats.name = Characteristics.name WHERE Cats.name = ?', (cat['name']))
        #     cur.execute('SELECT Cats.name, Cats.hypoallergenic, Cats.lifespan, Cats.origin, Characteristics.energy_level, Characteristics.intelligence FROM Cats JOIN Characteristics ON Cats.name = Characteristics.name')
        #     result = cur.fetchall()
        #     print(result)
    conn.commit()

    return 

def main(): 
    #print(read_data("https://api.thecatapi.com/v1/breeds"))
    #grabbing data from cat breeds website
    json_data = read_data('https://api.thecatapi.com/v1/breeds')
    cur,conn = open_database('cat_database.db')
    make_cat_table(json_data, cur, conn)
    make_characteristics_table(json_data, cur, conn)

    rare_breed_search(json_data,cur, conn)

    conn.close()

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)