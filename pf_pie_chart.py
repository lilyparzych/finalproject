from matplotlib import pyplot as plt

width = .75

x_axis = ["American\nShorthair", "Domestic\nLong\nHair", "Domestic\nMedium\nHair", "Domestic\nShort\nHair", "Extra-Toes Cat", "Siamese", "Tabby", "Tortoise-\nshell", "Tuxedo"]

y_axis = [58.8656, 50.72296, 50.205299999999994, 49.10541449275363, 72.13115, 55.093050000000005, 44.7338875, 54.78215, 58.7748]

plt.bar(x_axis, y_axis, width=width)
plt.title("Average Distance from AA of Adoptable Cat by Breed")
plt.xlabel("Cat Breed")
plt.ylabel("Average Distance from Ann Arbor")
plt.show()