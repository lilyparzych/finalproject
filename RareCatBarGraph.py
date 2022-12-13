from matplotlib import pyplot as plt

import numpy as np 
from adoptacat import * 
from catfacts import * 

barWidth = 0.25 
fig = plt.figure(figsize=(15,4), constrained_layout=True)

#read data
json_data = read_data('https://api.thecatapi.com/v1/breeds')
clean_json_data(json_data)
cur,conn = open_database('cat_database.db')
make_cat_table(json_data, cur, conn)
make_characteristics_table(json_data, cur, conn)
[rare_breed_names, rare_breed_info] = rare_breed_search(cur, conn)
print(len(rare_breed_names))
Affection_Levels = rare_breed_info[0]
print(len(Affection_Levels))
Energy_Levels = rare_breed_info[1]
print(Energy_Levels)
Intelligence = rare_breed_info[2]
print(Intelligence)
Hypoallergenic = rare_breed_info[3]
print(Hypoallergenic)

bar1 = np.arange(len(rare_breed_names))
bar2 = [x + barWidth for x in bar1]
bar3 = [x + barWidth for x in bar2]
bar4 = [x + barWidth for x in bar3]

plt.bar(bar1,Affection_Levels, color = 'maroon', width=barWidth, label = 'Affection Levels')
plt.bar(bar2,Energy_Levels, color = 'orangered', width=barWidth, label = 'Energy Levels')
plt.bar(bar3,Intelligence, color = 'mediumseagreen', width=barWidth, label = 'Intelligence')
plt.bar(bar4,Hypoallergenic, color = 'lightskyblue', width=barWidth, label = 'Hypoallergenic')

plt.xlabel('Cat Breeds', fontweight ='bold', fontsize = 15)
plt.ylabel('Rating', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(rare_breed_names))], rare_breed_names)
plt.xticks(fontsize = 10)
plt.xticks(rotation=90)
plt.title("Characteristics of Rare Cat Breeds")


plt.legend()
plt.show()