import json

with open("C:/Users/jmpan/Desktop/response1.json") as f:
  data = json.load(f)

cntr = 0
for i in data.get('response').get('discoverables'):
    cntr+=1
    print(i.get('title'))
print(cntr)
