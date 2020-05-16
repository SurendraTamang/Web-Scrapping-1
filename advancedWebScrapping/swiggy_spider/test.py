'''
import json


#Code for extracting hotel names

with open('C:/Users/byom/Desktop/WebScrapping/advancedWebScrapping/swiggy_spider/swiggy_hotels.json', 'r') as f:
    data = json.load(f)

items = data.get('data').get('cards')
for item in items:
    id = item.get('data').get('data').get('id')
    name = item.get('data').get('data').get('name')
    area = item.get('data').get('data').get('area')

    print(f"{id}: {name}: {area}")


# Code for extracting menu details

with open("C:/Users/byom/Desktop/WebScrapping/advancedWebScrapping/swiggy_spider/swiggy.json", "r") as read_file:
    data = json.load(read_file)

op = data.get('data').get('menu').get('items')

for key in op:
    name = data.get('data').get('menu').get('items').get(key).get('name')
    price = data.get('data').get('menu').get('items').get(key).get('price')
    if data.get('data').get('menu').get('items').get(key).get('isVeg'):
        category = "Veg"
    else:
        category = "Non-Veg"
    print(f"{name}: {price}: {category}")

'''


price = "36000"
print(price[:-2])