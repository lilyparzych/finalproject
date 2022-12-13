from matplotlib import pyplot as plt
import os
import sqlite3

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

cur,conn = open_database("cat_database.db")



def create_bar_chart(labels: list,data: list):
    width = .8
    color = "#28a993"
    plt.bar(labels, data, width=width, color=color)
    plt.title("Average Distance of Available Cat from AA by Breed", fontweight="bold")
    plt.xlabel("Cat Breed", fontweight="bold")
    plt.ylabel("Average Distance from\nAnn Arbor", fontweight="bold")
    plt.xticks(rotation=90, fontsize=8)
    plt.tight_layout()
    plt.show()


rows = (cur.execute("SELECT breed, AVG(distance) FROM Animals GROUP BY breed").fetchall())
lambda_labels = [rows[i][0] for i in range(len(rows))]
lambda_data = [row[1] for row in rows]
create_bar_chart(lambda_labels,lambda_data)
