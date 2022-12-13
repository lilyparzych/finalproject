import matplotlib.pyplot as plt


labels = 'Female', 'Male'
sizes = [97, 73]
# explode = (0, 0.1)  explode=explode,
colors = "#FFB6C1", "#b7e2fc"

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Cats Available for Adoption in Ann Arbor\n and the Surrounding Area by Gender")
plt.show()
