import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class IdeaSpider(scrapy.Spider):
    name = 'idea'
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.idealista.com/inmueble/1735609/",
            cookies={
                '_pxvid': '''906be331-3e1f-11eb-9ab9-35c006ce2520; _pxhd=a8fed09a61199a7568d7de50ffa31579feca84cd1187ba911f3ce746a6a6fa4f:906be331-3e1f-11eb-9ab9-35c006ce2520; cto_lwid=962c340a-d47b-43da-8873-584d68ac33a2; didomi_token=eyJ1c2VyX2lkIjoiMTc2NjFkNGYtMDQxNy02YjRlLWEzOWYtNzZlN2JkOGU0NDljIiwiY3JlYXRlZCI6IjIwMjAtMTItMTRUMTU6MTg6NDAuNDM1WiIsInVwZGF0ZWQiOiIyMDIwLTEyLTE0VDE1OjE4OjQwLjQzNVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZmFjZWJvb2siLCJ0d2l0dGVyIiwiZ29vZ2xlIiwiYzptaXhwYW5lbCIsImM6aWRlYWxpc3RhLWZlUkVqZTJjIiwiYzppZGVhbGlzdGEtTHp0QmVxRTMiLCJjOmFidGFzdHktTExrRUNDajgiLCJjOmhvdGphciIsImM6YXQtaW50ZXJuZXQiLCJjOnlhbmRleG1ldHJpY3MiLCJjOmJlYW1lci1IN3RyN0hpeCIsImM6Y2hhcmJlYXQtWjRRazhDYWgiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiYW5hbGl0aWNhcy1keUZWR1JlOCIsImdlb2xvY2F0aW9uX2RhdGEiXX0sInZlcnNpb24iOjJ9; euconsent-v2=CO-axckO-axckAHABBENBECoAP_AAAAAAAAAF5wAwAWgBbAXmAAAAgNAnABUAFYALgAhgBkADLAGoANkAdgA_ACAAEFAIwAUsAp4BV4C0ALSAawA3gB1QD5AIbAQ6Ai8BIgCbAE7AKRAXIAwIBhIDDwGMAMnAZyAzwBnwDkgHKEoHAACAAFgAUAAyABwAEUAMAAxAB4AEQAJgAVQAuABfADEAGYANoAhABDQCIAIkARwApQBbgDCAGUANUAbIA7wB-AEYAI4AU8Aq8BaAFpALqAYoA3ABxADqAHyAQ6Ai8BIgCbAFigLYAXaAvMBh4DIgGTgM5AZ4Az4BpADWAHAFIJgAC4AKAAqABkADgAIAARAAqgBgAGMANAA1AB5AEMARQAmABPACkAFUALAAXAAvgBiADMAHMAQgAhoBEAESAKUAWIAtwBhADKAGiANUAbIA74B9gH6ARYAjABHACUgFBAKGAVcArYBcwC8gGEANoAbgA9ACHQEXgJEATYAnYBQ4CmgFbALFAWwAuABcgC7QF5gMNAYeAxgBkQDJAGTgMuAZyAzwBn0DSANJgawBrIDY4HJgcoQggAALAAoABkAEQAKgAXAAxACGAEwAKoAXAAvgBiADMAG8APQAjgBYgDCAGUANQAb4A74B9gH4AP8AgYBGACOAEpAKCAUMAp4BV4C0ALSAXMAvwBhADFAG0AOoAegBIICRAEqAJsAU0AsUBaMC2ALaAXAAuQBdoDDwGJAMiAZOAzkBngDPgGiANJAaWA4AByQ6DQAAuACgAKgAZAA4ACAAEQAKgAXQAwADGAGgAagA8AB9AEMARQAmABPgCqAKwAWAAuABfADEAGYAN4AcwA9ACEAENAIgAiQBHQCWAJgATQApQBYgC3gGEAYYAyABlADRAGoANkAb4A7wB7QD7AP0Af8BFgEYAI5ASkBKgCggFPAKuAWKAtAC0gFzALqAXkAvwBhADFAG0ANwAcSA6YDqAHoAQ2Ah0BEQCLwEggJEASoAmwBOwChwFNAKsAWKAtCBbAFsgLgAXIAu0Bd4C8wGDAMJAYaAw8BiQDGAGPAMkAZOAyoBlwDOQGfANEgaQBpIDSwGnANYAbGA4uByQHKhILQACAAFwAUABUADIAHAAPAAgABEACoAGEANAA1AB5AEMARQAmABPgCqAKwAWAAuABvADmAHoAQgAhoBEAESAI6ASwBLgCaAFKALcAYYAyABlwDUANUAbIA7wB7AD4gH2AfoBAICLgIwARoAjgBKQCggFLAKeAVcAuYBfgDCAGKANYAbQA3ABvADiAHoAPkAhsBDoCKgEXgJEATEAmUBNgCdgFDgKRAWKAtABbAC5AF3gLzAYEAwYBhIDDQGHgMiAZIAycBlwDOQGfANIAadA1gDWYHIgcqMgOgAUABUAEMAJgAXABHADLAGoAOyAfYB-AEYAI4AUsAq4BWwDeAJiATYAtEBbAC8wGBAMPAZEAzkBngDPgHJAOUFQIAAKAAqACGAEwALgAjgBlgDUAHYAPwAjABHAClgFXgLQAtIBvAEggJiATYApsBbAC5AF5gMCAYeAyIBnIDPAGfANyAckA5QAAA.f_gAAAAAAAAA; xtant352991=1; xtan352991=2-anonymous; xtvrn=$352991$; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%225711b1bd-be67-47a0-8419-98c64828fd61%22%2C%22options%22%3A%7B%22end%22%3A%222022-01-15T15%3A18%3A41.274Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-582065-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; _hjTLDTest=1; _hjid=7351204d-fa43-4f66-91b8-0836552e3625; TestIfCookie=ok; TestIfCookieP=ok; pbw=%24b%3d16860%3b%24o%3d11100%3b%24sw%3d1600%3b%24sh%3d768; pid=7298665147171149685; pdomid=3; lcsrd=2020-12-14T15:20:34.7216779Z; userUUID=a33dbac5-4869-436e-86ad-75cf6292bf19; askToSaveAlertPopUp=true; sasd=%24qc%3D1314370601%3B%24ql%3DLow%3B%24qpc%3D759001%3B%24qt%3D32_4084_114024t%3B%24dma%3D0; dyncdn=limit; send73ce2c2b-40f7-4a95-a338-9822133b4f3b="{'friendsEmail':null,'email':null,'message':null}"; Trk0=Value=253245&Creation=18%2f12%2f2020+15%3a04%3a26; sasd2=q=%24qc%3D1314370601%3B%24ql%3DUnknown%3B%24qpc%3D759001%3B%24qt%3D32_4084_114024t%3B%24dma%3D0&c=1&l&lo&lt=637439011768317238&o=1; SESSION=4e79f823-5d5e-471a-ac6e-4299dc711b50; _hjIncludedInSessionSample=1; _hjAbsoluteSessionInProgress=1; ABTasty=uid=mekmq311vj5kwn4m&fst=1607959121203&pst=1608300248594&cst=1608317146459&ns=10&pvt=197&pvis=197&th=; ABTastySession=mrasn=&lp=https://www.idealista.com/&sen=2; vs=33114=4188645; cnfq=1; csfq=1; cookieSearch-1="/venta-viviendas/a-coruna-provincia/:1608317158438"; contact4e79f823-5d5e-471a-ac6e-4299dc711b50="{'email':null,'phone':null,'phonePrefix':null,'friendEmails':null,'name':null,'message':null,'message2Friends':null,'maxNumberContactsAllow':10,'defaultMessage':true}"; WID=856ee353ead52159|X9z46|X9z41; datadome=WuLW1C8GLj92leXzWJBG0oAlHAcDE4kmLRzDB5strjRVePA410dKSgMWLU~muQAYhX44Uf.Ohe7OEKRoY_qMq6rgVayPZgsMx.cAyGke1s; criteo_write_test=ChUIBBINbXlHb29nbGVSdGJJZBgBIAE; utag_main=v_id:017661d487130014f014011f6a1903083001607b009dc$_sn:10$_se:3$_ss:0$_st:1608318960082$ses_id:1608317140700%3Bexp-session$_pn:3%3Bexp-session$_prevVtSource:directTraffic%3Bexp-1608320743771$_prevVtCampaignCode:%3Bexp-1608320743771$_prevVtDomainReferrer:%3Bexp-1608320743771$_prevVtSubdomaninReferrer:%3Bexp-1608320743771$_prevVtUrlReferrer:%3Bexp-1608320743771$_prevVtCampaignLinkName:%3Bexp-1608320743771$_prevCompletePageName:11%3A%3Amunicipios%3A%3Awww.idealista.com%2Fventa-viviendas%2Fa-coruna-provincia%2Fmunicipios%3Bexp-1608320747904$_prevAdId:undefined%3Bexp-1608320747906$_prevAdOriginTypeRecommended:undefined%3Bexp-1608320743782'''
            },
            wait_time=5,
            callback=self.parse
        )
    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h1/span"))) 
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//span[text()='Aceptar y cerrar']/parent::button").click()
        except:
            pass
        #   GETTING THE PAGE HEIGHT & SCROLLING GRADUALLY THROUGH THE PAGE TO LAOD ALL THE ELEMENTS #
        height = driver.execute_script("return document.body.scrollHeight")
        for i in range(1, (height//200)+1):
            driver.execute_script(f"window.scrollTo(0, {i*200});")
            time.sleep(0.1)
        time.sleep(3)
        input()

        html = driver.page_source
        resp_obj = Selector(text=html)

        addr_raw = resp_obj.xpath("//h2[text()='Ubicación']/following-sibling::ul/li/text()").getall()
        yield{
            'Property Title': resp_obj.xpath("normalize-space(//h1/span/text())").get(),
            'Area in meter sq': resp_obj.xpath("normalize-space(//h2[text()='Características básicas']/following-sibling::div/ul/li[contains(text(),'m²')]/text())").get(),
            'Bed': resp_obj.xpath("normalize-space(//h2[text()='Características básicas']/following-sibling::div/ul/li[contains(text(),'habit')]/text())").get(),
            'Bath': resp_obj.xpath("normalize-space(//h2[text()='Características básicas']/following-sibling::div/ul/li[contains(text(),'baño')]/text())").get(),
            'Price': resp_obj.xpath("normalize-space(//span[contains(@class, 'price')]/span/text())").get(),
            'Owner Name': resp_obj.xpath("normalize-space(//div[contains(text(), 'Particular')]/following-sibling::span/input/@value)").get(),
            'Phone': resp_obj.xpath("normalize-space(//p[contains(@class, 'Phone')]/text())").get(),
            'Reference No': resp_obj.xpath("normalize-space(//p[contains(text(), 'Anuncio')]/text())").get(),
            'Type': None,
            'Rent/Sale': None,
            'Address': " , ".join(addr.strip() for addr in addr_raw),
            'Images': resp_obj.xpath("//div[@id='main-multimedia']//div[contains(@class, 'image')]/img/@data-ondemand-img").getall(),
            'Image Main': resp_obj.xpath("//div[@class='main-image_first']/img/@src").get(),
            'Url': driver.current_url
        }
