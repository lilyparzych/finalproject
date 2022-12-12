from matplotlib import pyplot as plt

import numpy as np 

barWidth = 0.25 
fig = plt.figure(figsize=(15,4), constrained_layout=True)

RareBreeds = ['Scottish Fold', 'Norwegian Forest', 'Turkish Angora', 'American Bobtail', 'Burmilla', 'Devon Rex', 'Egyptian Mau', 'Tonkinese', 'Chartreux', 'Bombay', 'Selkirk Rex', 'American Wirehair', 'Sphynx', 'Korat', 'Ocicat', 'Cornish Rex', 'Singapura', 'Havana Brown']
Affection_Levels = [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
Energy_Levels = [3,3,5,3,3,5,5,5,2,3,3,3,3,3,5,5,5,3]
Intelligence = [3,4,5,5,3,5,4,5,4,5,3,3,5,5,5,5,5,5]
Hypoallergenic = [0,0,0,0,0,1,0,0,1,0,1,0,1,0,1,1,0,0]

bar1 = np.arange(len(RareBreeds))
bar2 = [x + barWidth for x in bar1]
bar3 = [x + barWidth for x in bar2]
bar4 = [x + barWidth for x in bar3]

plt.bar(bar1,Affection_Levels, color = 'maroon', width=barWidth, label = 'Affection Levels')
plt.bar(bar2,Energy_Levels, color = 'orangered', width=barWidth, label = 'Energy Levels')
plt.bar(bar3,Intelligence, color = 'mediumseagreen', width=barWidth, label = 'Intelligence')
plt.bar(bar4,Hypoallergenic, color = 'lightskyblue', width=barWidth, label = 'Hypoallergenic')

plt.xlabel('Cat Breeds', fontweight ='bold', fontsize = 15)
plt.ylabel('Rating', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(RareBreeds))], RareBreeds)
plt.xticks(fontsize = 10)
plt.xticks(rotation=90)
plt.title("Characteristics of Rare Cat Breeds")


plt.legend()
plt.show()