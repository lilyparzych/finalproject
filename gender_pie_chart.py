import matplotlib.pyplot as plt
import os
import sqlite3

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

cur, conn = open_database("cat_database.db")
rows = (cur.execute("SELECT gender, COUNT(*) FROM Animals GROUP BY gender").fetchall())
num_male = rows[1][1]
num_female = rows[0][1]

def make_pie(num_female, num_male):
    labels = 'Female', 'Male'
    sizes = [num_female, num_male]
    # explode = (0, 0.1)  explode=explode,
    colors = "#FFB6C1", "#b7e2fc"

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  
    plt.title("Cats Available for Adoption in Ann Arbor\n and the Surrounding Area by Gender", fontweight="bold")
    plt.show()

make_pie(num_male=num_male,num_female=num_female)