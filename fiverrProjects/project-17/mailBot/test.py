# -*- coding: utf-8 -*-
import requests
from scrapy import Selector
import json


r = requests.get(input("Enter the URL: "))

respObj = Selector(text=r.content)

scriptData = respObj.xpath("normalize-space(//div[@id='body-wrapper']/following-sibling::script[1]/text())").get().encode("ascii", "ignore")
string_decode = scriptData.decode().split("window.webpackBundles")[0].replace("window.state = ","")
# print(string_decode)
# scriptData=scriptData.decode('utf-8','ignore').encode("utf-8")
# print(string_decode.strip()[:-1].replace("\n",""))
jsonObj = json.loads(string_decode.strip()[:-1].replace("\n",""))

# Serializing json 
json_object = json.dumps(jsonObj.get('property').get('data').get('phoneNumber'), indent = 4)

number1 = ",".join(i.strip() for i in jsonObj.get('property').get('data').get('phoneNumber').get('mobileNumbers') if i.strip())
number2 = ",".join(i.strip() for i in jsonObj.get('property').get('data').get('phoneNumber').get('phoneNumbers') if i.strip())
agencyName = jsonObj.get('property').get('data').get('agency').get('name')
contactName = jsonObj.get('property').get('data').get('contactName')

print(f'''Number1: {number1}\nNumber2: {number2}\nagencyName: {agencyName}\ncontactName: {contactName}\n''')

# Writing to sample.json
# with open("sample.json", "w") as outfile:
#     outfile.write(json_object)

# //div[@id='body-wrapper']/following-sibling::script[1]/text()

#-- Extracting contact details from the javascript tags --#
# def extractContactDetails(self, start, end):
#     start = s.find(start) + len(start)
#     end = s.find(end)
#     substring = s[start:end]
#     return substring