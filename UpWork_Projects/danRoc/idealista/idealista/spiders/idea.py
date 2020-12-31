import scrapy
import pandas as pd
import difflib
import csv


class IdeaSpider(scrapy.Spider):
    name = 'idea'
    cookies = {
        "userUUID" : '''22894d19-d441-45d9-9d43-993725606771; cto_lwid=2afecd24-4e53-4f7f-a41c-161d32e7c521; contact4f51b8e1-f52e-495a-bb36-d6b835b53fb7="{'email':null,'phone':null,'phonePrefix':null,'friendEmails':null,'name':null,'message':null,'message2Friends':null,'maxNumberContactsAllow':10,'defaultMessage':true}"; SESSION=4f51b8e1-f52e-495a-bb36-d6b835b53fb7; send4f51b8e1-f52e-495a-bb36-d6b835b53fb7="{'friendsEmail':null,'email':null,'message':null}"; cookieSearch-1="/venta-viviendas/a-coruna-a-coruna/:1608840985403"; criteo_write_test=ChUIBBINbXlHb29nbGVSdGJJZBgBIAE; didomi_token=eyJ1c2VyX2lkIjoiMTc2OTY2NTUtMDZiNi02NTFjLWFhMzYtY2RhNWNhZjg1OTgzIiwiY3JlYXRlZCI6IjIwMjAtMTItMjRUMjA6MTY6MzIuOTUyWiIsInVwZGF0ZWQiOiIyMDIwLTEyLTI0VDIwOjE2OjMyLjk1MloiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZmFjZWJvb2siLCJ0d2l0dGVyIiwiZ29vZ2xlIiwiYzptaXhwYW5lbCIsImM6aWRlYWxpc3RhLWZlUkVqZTJjIiwiYzppZGVhbGlzdGEtTHp0QmVxRTMiLCJjOmFidGFzdHktTExrRUNDajgiLCJjOmhvdGphciIsImM6eWFuZGV4bWV0cmljcyIsImM6YmVhbWVyLUg3dHI3SGl4IiwiYzpjaGFyYmVhdC1aNFFrOENhaCJdfSwicHVycG9zZXMiOnsiZW5hYmxlZCI6WyJhbmFsaXRpY2FzLWR5RlZHUmU4IiwiZ2VvbG9jYXRpb25fZGF0YSJdfSwidmVyc2lvbiI6MiwiYWMiOiJBa3VBQ0Frcy5BQUFBIn0=; euconsent-v2=CO-8adKO-8adKAHABBENBECoAP_AAAAAAAAAF5wAwAWgBbAXmAAAAgNAnABUAFYALgAhgBkADLAGoANkAdgA_ACAAEFAIwAUsAp4BV4C0ALSAawA3gB1QD5AIbAQ6Ai8BIgCbAE7AKRAXIAwIBhIDDwGMAMnAZyAzwBnwDkgHKEoHAACAAFgAUAAyABwAEUAMAAxAB4AEQAJgAVQAuABfADEAGYANoAhABDQCIAIkARwApQBbgDCAGUANUAbIA7wB-AEYAI4AU8Aq8BaAFpALqAYoA3ABxADqAHyAQ6Ai8BIgCbAFigLYAXaAvMBh4DIgGTgM5AZ4Az4BpADWAHAFIJgAC4AKAAqABkADgAIAARAAqgBgAGMANAA1AB5AEMARQAmABPACkAFUALAAXAAvgBiADMAHMAQgAhoBEAESAKUAWIAtwBhADKAGiANUAbIA74B9gH6ARYAjABHACUgFBAKGAVcArYBcwC8gGEANoAbgA9ACHQEXgJEATYAnYBQ4CmgFbALFAWwAuABcgC7QF5gMNAYeAxgBkQDJAGTgMuAZyAzwBn0DSANJgawBrIDY4HJgcoQggAALAAoABkAEQAKgAXAAxACGAEwAKoAXAAvgBiADMAG8APQAjgBYgDCAGUANQAb4A74B9gH4AP8AgYBGACOAEpAKCAUMAp4BV4C0ALSAXMAvwBhADFAG0AOoAegBIICRAEqAJsAU0AsUBaMC2ALaAXAAuQBdoDDwGJAMiAZOAzkBngDPgGiANJAaWA4AByQ6DQAAuACgAKgAZAA4ACAAEQAKgAXQAwADGAGgAagA8AB9AEMARQAmABPgCqAKwAWAAuABfADEAGYAN4AcwA9ACEAENAIgAiQBHQCWAJgATQApQBYgC3gGEAYYAyABlADRAGoANkAb4A7wB7QD7AP0Af8BFgEYAI5ASkBKgCggFPAKuAWKAtAC0gFzALqAXkAvwBhADFAG0ANwAcSA6YDqAHoAQ2Ah0BEQCLwEggJEASoAmwBOwChwFNAKsAWKAtCBbAFsgLgAXIAu0Bd4C8wGDAMJAYaAw8BiQDGAGPAMkAZOAyoBlwDOQGfANEgaQBpIDSwGnANYAbGA4uByQHKhILQACAAFwAUABUADIAHAAPAAgABEACoAGEANAA1AB5AEMARQAmABPgCqAKwAWAAuABvADmAHoAQgAhoBEAESAI6ASwBLgCaAFKALcAYYAyABlwDUANUAbIA7wB7AD4gH2AfoBAICLgIwARoAjgBKQCggFLAKeAVcAuYBfgDCAGKANYAbQA3ABvADiAHoAPkAhsBDoCKgEXgJEATEAmUBNgCdgFDgKRAWKAtABbAC5AF3gLzAYEAwYBhIDDQGHgMiAZIAycBlwDOQGfANIAadA1gDWYHIgcqMgOgAUABUAEMAJgAXABHADLAGoAOyAfYB-AEYAI4AUsAq4BWwDeAJiATYAtEBbAC8wGBAMPAZEAzkBngDPgHJAOUFQIAAKAAqACGAEwALgAjgBlgDUAHYAPwAjABHAClgFXgLQAtIBvAEggJiATYApsBbAC5AF5gMCAYeAyIBnIDPAGfANyAckA5QAAA.f_gAAAAAAAAA; xtvrn=$352991$; xtan352991=2-anonymous; xtant352991=1; WID=3db49eae99c96f8b|X+T3J|X+TlF; datadome=E75SA9g4zxlqWU4bCC6HWr1QhSuuBGv3d3YnrC3gyHbYo0sr6i9YuSgKVtMeLgG1I5Ldl4_XZlwC~Q~l1giIuAIqerX.9_9sGl7-pbfQil; utag_main=v_id:01769512a9e6001e57e73f93d1e103083002c07b009dc$_sn:2$_se:2$_ss:0$_st:1608842794507$ses_id:1608840991540%3Bexp-session$_pn:2%3Bexp-session$_prevVtSource:portalSites%3Bexp-1608844593039$_prevVtCampaignCode:%3Bexp-1608844593039$_prevVtDomainReferrer:idealista.com%3Bexp-1608844593039$_prevVtSubdomaninReferrer:www.idealista.com%3Bexp-1608844593039$_prevVtUrlReferrer:https%3A%2F%2Fwww.idealista.com%2Fventa-viviendas%2Fa-coruna-a-coruna%2F%3Bexp-1608844593039$_prevVtCampaignLinkName:%3Bexp-1608844593039$_prevCompletePageName:11%3A%3Alisting%3A%3AresultList%3A%3Aothers%3Bexp-1608844593042$_prevAdId:undefined%3Bexp-1608844593045$_prevAdOriginTypeRecommended:undefined%3Bexp-1608844593047'''
    }

    #   READING REQUIRED FILES  #
    DATAFILE_PATH = "idealistaData.csv"
    PROVINCE_DF = pd.read_excel("provUrls.xlsx")
    DATA_DF = pd.read_csv(DATAFILE_PATH)
    oldDataUrls = DATA_DF['Url'].to_list()

    #  TAKING USER INPUTS  #
    print("============================================================================================")
    print("\n\nWELCOME TO idealista SCRAPER\n")
    print("============================================================================================")
    provinceLi = list(map(str, input("ENTER THE PROVINCE NAME (Separate multiple values with a ,): ").rstrip().split(',')))
    areaLi = list(map(str, input("ENTER THE AREA (separate multiple values with ,) / (type all to scrape all the areas): ").rstrip().split(',')))
    buyRent = input("\nENTER THE TYPE (buy / rent) : ")  
    print("============================================================================================")
    print("\nTHANKS FOR THE INPUTS. STARTING THE SCRAPER ..... \n\n")
    print("============================================================================================")
    
    #   WRITING THE DATA INTO CSV FILE  #
    def writeCSV(self, dict_data, fieldName):
        with open(self.DATAFILE_PATH, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
            for data in dict_data:
                writer.writerow(data)

    def start_requests(self):
        startReqUrlLi = []
        propTypes = ['obranueva', 'garajes', 'trasteros', 'oficinas', 'locales', 'terrenos', 'edificios']
        for _,val in self.PROVINCE_DF.iterrows():
            if val['provinceName'] in self.provinceLi:
                provinceUrl = val['provinceUrl']
                if self.buyRent == "rent":
                    provinceUrl = val['provinceUrl'].replace("venta-viviendas","alquiler-viviendas")
                startReqUrlLi.append(provinceUrl)
                for propType in propTypes:
                    x = provinceUrl.replace("-viviendas",f"-{propType}")
                    startReqUrlLi.append(x)

        for startReqUrl in startReqUrlLi:
            yield scrapy.Request(
                url=startReqUrl,
                callback=self.getAreaUrls,
                cookies=self.cookies
            )

    def getAreaUrls(self, response):
        provAreas = response.xpath("//ul[@id='location_list']/li/ul/li")
        for area in self.areaLi:                
                for provArea in provAreas:
                    areaCount = str(provArea.xpath("normalize-space(.//text()[2])").get())                  
                    if "all" in self.areaLi:
                        if int(areaCount.replace(".","")) > 1800:
                            yield scrapy.Request(
                                url=f'''https://www.idealista.com{provArea.xpath(".//a/@href").get()}''',
                                callback=self.getSubAreaUrls,
                                cookies=self.cookies
                            )
                        else:
                            yield scrapy.Request(
                                url=f'''https://www.idealista.com{provArea.xpath(".//a/@href").get()}''',
                                callback=self.getListings,
                                cookies=self.cookies
                            )
                    else:
                        inp = area
                        mch = provArea.xpath("normalize-space(.//a/text())").get()
                        if difflib.SequenceMatcher(None, f'{inp.lower()}', f'{mch.lower()}').ratio() > 0.8 :
                            if int(areaCount.replace(".","")) > 1800:
                                yield scrapy.Request(
                                    url=f'''https://www.idealista.com{provArea.xpath(".//a/@href").get()}''',
                                    callback=self.getSubAreaUrls,
                                    cookies=self.cookies
                                )
                            else:
                                yield scrapy.Request(
                                    url=f'''https://www.idealista.com{provArea.xpath(".//a/@href").get()}''',
                                    callback=self.getListings,
                                    cookies=self.cookies
                                )

    def getSubAreaUrls(self, response):
        subArUrls = response.xpath("//nav[@class]//span[contains(@class, 'arrow-dropdown')]/following-sibling::div/ul//strong/following-sibling::ul/li")
        for subArUrl in subArUrls:
            yield scrapy.Request(
                url=f'''https://www.idealista.com{subArUrl.xpath(".//a/@href").get()}''',
                callback=self.getListings,
                cookies=self.cookies
            )

    def getListings(self, response):
        subArCount = str(response.xpath("normalize-space(//nav[@class='breadcrumb-geo']/ul/li[last()]/span[@class='breadcrumb-info']/text())").get())
        if int(subArCount.replace(".","")) > 1800:
            yield scrapy.Request(
                url=response.url,
                callback=self.getSubAreaUrls,
                cookies=self.cookies
            )
        else:
            adLi = response.xpath("//section[@class='items-container']/article[contains(@class, 'item')]")
            for ad in adLi:
                image = ad.xpath(".//picture[contains(@class,'gallery')]/img/@data-ondemand-img").get()
                try:
                    img = image.replace("WEB_LISTING","WEB_DETAIL_TOP")
                except:
                    img = None
                adUrl = f'''https://www.idealista.com{ad.xpath(".//a[@role='heading']/@href").get()}'''
                if not ad.xpath(".//picture[@class='logo-branding']") and adUrl not in self.oldDataUrls:
                    self.oldDataUrls.append(adUrl)
                    propTypeRaw = ad.xpath("normalize-space(//a[@role='heading']/text())").get()
                    try:
                        propType = propTypeRaw.split(" en ")[0]
                    except:
                        propType = None
                    yield scrapy.Request(
                        url=adUrl,
                        callback=self.parse,
                        cookies=self.cookies,
                        meta={
                            'image': img,
                            'propertyType': propType
                        }
                    )
            nextPage = response.xpath("//span[text()='Siguiente']/parent::a/@href").get()
            if nextPage:
                yield scrapy.Request(
                    url=f"https://www.idealista.com{nextPage}",
                    callback=self.getListings,
                    cookies=self.cookies
                )

    def parse(self, response):
        onrName = response.xpath("normalize-space(//span[@class='particular']/input/@value)").get()
        phone = response.xpath("normalize-space(//p[contains(@class, 'Phone')]/text())").get()
        if onrName and phone:
            addr_raw = response.xpath("//h2[text()='Ubicación']/following-sibling::ul/li/text()").getall()
            ref_no = response.xpath("normalize-space(//p[contains(text(), 'Anuncio')]/text())").get()
            area = response.xpath("normalize-space(//h2[text()='Características básicas']/following-sibling::div/ul/li[contains(text(),'m²')]/text())").get()
            bed = response.xpath("normalize-space(//h2[text()='Características básicas']/following-sibling::div/ul/li[contains(text(),'habit')]/text())").get()
            bath = response.xpath("normalize-space(//h2[text()='Características básicas']/following-sibling::div/ul/li[contains(text(),'baño')]/text())").get()
            
            dataList=[]
            dataList.append(
                {
                    'Property Title': response.xpath("normalize-space(//h1/span/text())").get(),
                    'Area in meter sq': area.split(" ")[0],
                    'Bed': bed.split(" ")[0],
                    'Bath': bath.split(" ")[0],
                    'Price': f'''{response.xpath("normalize-space(//span[contains(@class, 'price')]/span/text())").get()} €''',
                    'Owner Name': onrName,
                    'Phone': f'''{phone}''',
                    'Reference No': f'''{ref_no.replace("Anuncio: ","")}''',
                    'Type': response.request.meta['propertyType'],
                    'Rent/Sale': self.buyRent,
                    'Address': " , ".join(addr.strip() for addr in addr_raw if addr.strip()),
                    'Image': response.request.meta['image'],
                    'Url': response.url
                }
            )
            self.writeCSV(dataList, ["Property Title", "Area in meter sq", "Bed", "Bath", "Price", "Owner Name", "Phone", "Reference No", "Type", "Rent/Sale", "Address", "Image", "Url"])
