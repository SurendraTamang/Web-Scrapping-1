import csv


FIELD_NAMES = ['Handle','Title','Body (HTML)','Vendor','Type','Tags','Collection','Published','Option1 Name','Option1 Value','Option2 Name','Option2 Value','Option3 Name','Option3 Value','Variant SKU','Variant Grams','Variant Inventory Tracker','Variant Inventory Qty','Variant Inventory Policy','Variant Fulfillment Service','Variant Price','Variant Compare At Price','Variant Requires Shipping','Variant Taxable','Variant Barcode','Image Src','Image Position','Image Alt Text','Gift Card','SEO Title','SEO Description','Google Shopping metafields','Variant Image','Variant Weight Unit','Variant Tax Code','Cost per item']

def writeCSV(data, fieldName, file_name):
    fileExists = os.path.isfile(file_name)
    with open(file_name, 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
        if not fileExists:
            writer.writeheader()
        writer.writerow(data)

with open('tescoWooCommerceTemplate.csv') as csv_file:
    # with open('test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for indx,data in enumerate(csv_reader):
            if indx != 0:
                vendor = None
                if "tesco" in data[0].lower():
                    vendor = "tesco"
                dataDict = {
                    FIELD_NAMES[0]: data[0].lower().replace(" ","-"),
                    FIELD_NAMES[1]: data[1],
                    FIELD_NAMES[2]: data[2],
                    FIELD_NAMES[3]: vendor,
                    FIELD_NAMES[4]: data[17],
                    FIELD_NAMES[5]: None,
                    FIELD_NAMES[6]: None,
                    FIELD_NAMES[7]: "TRUE",
                    FIELD_NAMES[8]: "Title",
                    FIELD_NAMES[9]: "Default Title",
                    FIELD_NAMES[9]: None,
                    FIELD_NAMES[10]: None,
                    FIELD_NAMES[11]: None,
                    FIELD_NAMES[12]: None,
                    FIELD_NAMES[13]: data[4],
                }
                writeCSV(dataDict, FIELD_NAMES, "shopify.csv")