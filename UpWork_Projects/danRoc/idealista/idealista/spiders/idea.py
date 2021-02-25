import scrapy
import pandas as pd
import difflib
import csv
import random
import os
import time


class IdeaSpider(scrapy.Spider):
    name = 'idea'

    headers = [
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36.'},
    ]

    cookies = [
        {"_pxvid" : '''906be331-3e1f-11eb-9ab9-35c006ce2520; cto_lwid=962c340a-d47b-43da-8873-584d68ac33a2; didomi_token=eyJ1c2VyX2lkIjoiMTc2NjFkNGYtMDQxNy02YjRlLWEzOWYtNzZlN2JkOGU0NDljIiwiY3JlYXRlZCI6IjIwMjAtMTItMTRUMTU6MTg6NDAuNDM1WiIsInVwZGF0ZWQiOiIyMDIwLTEyLTE0VDE1OjE4OjQwLjQzNVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZmFjZWJvb2siLCJ0d2l0dGVyIiwiZ29vZ2xlIiwiYzptaXhwYW5lbCIsImM6aWRlYWxpc3RhLWZlUkVqZTJjIiwiYzppZGVhbGlzdGEtTHp0QmVxRTMiLCJjOmFidGFzdHktTExrRUNDajgiLCJjOmhvdGphciIsImM6YXQtaW50ZXJuZXQiLCJjOnlhbmRleG1ldHJpY3MiLCJjOmJlYW1lci1IN3RyN0hpeCIsImM6Y2hhcmJlYXQtWjRRazhDYWgiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiYW5hbGl0aWNhcy1keUZWR1JlOCIsImdlb2xvY2F0aW9uX2RhdGEiXX0sInZlcnNpb24iOjJ9; euconsent-v2=CO-axckO-axckAHABBENBECoAP_AAAAAAAAAF5wAwAWgBbAXmAAAAgNAnABUAFYALgAhgBkADLAGoANkAdgA_ACAAEFAIwAUsAp4BV4C0ALSAawA3gB1QD5AIbAQ6Ai8BIgCbAE7AKRAXIAwIBhIDDwGMAMnAZyAzwBnwDkgHKEoHAACAAFgAUAAyABwAEUAMAAxAB4AEQAJgAVQAuABfADEAGYANoAhABDQCIAIkARwApQBbgDCAGUANUAbIA7wB-AEYAI4AU8Aq8BaAFpALqAYoA3ABxADqAHyAQ6Ai8BIgCbAFigLYAXaAvMBh4DIgGTgM5AZ4Az4BpADWAHAFIJgAC4AKAAqABkADgAIAARAAqgBgAGMANAA1AB5AEMARQAmABPACkAFUALAAXAAvgBiADMAHMAQgAhoBEAESAKUAWIAtwBhADKAGiANUAbIA74B9gH6ARYAjABHACUgFBAKGAVcArYBcwC8gGEANoAbgA9ACHQEXgJEATYAnYBQ4CmgFbALFAWwAuABcgC7QF5gMNAYeAxgBkQDJAGTgMuAZyAzwBn0DSANJgawBrIDY4HJgcoQggAALAAoABkAEQAKgAXAAxACGAEwAKoAXAAvgBiADMAG8APQAjgBYgDCAGUANQAb4A74B9gH4AP8AgYBGACOAEpAKCAUMAp4BV4C0ALSAXMAvwBhADFAG0AOoAegBIICRAEqAJsAU0AsUBaMC2ALaAXAAuQBdoDDwGJAMiAZOAzkBngDPgGiANJAaWA4AByQ6DQAAuACgAKgAZAA4ACAAEQAKgAXQAwADGAGgAagA8AB9AEMARQAmABPgCqAKwAWAAuABfADEAGYAN4AcwA9ACEAENAIgAiQBHQCWAJgATQApQBYgC3gGEAYYAyABlADRAGoANkAb4A7wB7QD7AP0Af8BFgEYAI5ASkBKgCggFPAKuAWKAtAC0gFzALqAXkAvwBhADFAG0ANwAcSA6YDqAHoAQ2Ah0BEQCLwEggJEASoAmwBOwChwFNAKsAWKAtCBbAFsgLgAXIAu0Bd4C8wGDAMJAYaAw8BiQDGAGPAMkAZOAyoBlwDOQGfANEgaQBpIDSwGnANYAbGA4uByQHKhILQACAAFwAUABUADIAHAAPAAgABEACoAGEANAA1AB5AEMARQAmABPgCqAKwAWAAuABvADmAHoAQgAhoBEAESAI6ASwBLgCaAFKALcAYYAyABlwDUANUAbIA7wB7AD4gH2AfoBAICLgIwARoAjgBKQCggFLAKeAVcAuYBfgDCAGKANYAbQA3ABvADiAHoAPkAhsBDoCKgEXgJEATEAmUBNgCdgFDgKRAWKAtABbAC5AF3gLzAYEAwYBhIDDQGHgMiAZIAycBlwDOQGfANIAadA1gDWYHIgcqMgOgAUABUAEMAJgAXABHADLAGoAOyAfYB-AEYAI4AUsAq4BWwDeAJiATYAtEBbAC8wGBAMPAZEAzkBngDPgHJAOUFQIAAKAAqACGAEwALgAjgBlgDUAHYAPwAjABHAClgFXgLQAtIBvAEggJiATYApsBbAC5AF5gMCAYeAyIBnIDPAGfANyAckA5QAAA.f_gAAAAAAAAA; xtvrn=$352991$; xtant352991=1; xtan352991=2-anonymous; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%225711b1bd-be67-47a0-8419-98c64828fd61%22%2C%22options%22%3A%7B%22end%22%3A%222022-01-15T15%3A18%3A41.274Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-582065-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; _hjTLDTest=1; _hjid=7351204d-fa43-4f66-91b8-0836552e3625; TestIfCookie=ok; TestIfCookieP=ok; pbw=%24b%3d16860%3b%24o%3d11100%3b%24sw%3d1600%3b%24sh%3d768; pid=7298665147171149685; pdomid=3; userUUID=a33dbac5-4869-436e-86ad-75cf6292bf19; lcsrd=2020-12-29T17:01:01.0367800Z; vs=33114=4212853; ABTasty=uid=mekmq311vj5kwn4m&fst=1607959121203&pst=1609763599586&cst=1609769595132&ns=43&pvt=463&pvis=463&th=; sended25f9a7-b6d0-4af4-88ef-ec5ae152c20d="{'friendsEmail':null,'email':null,'message':null}"; SESSION=a7afeee3-b560-41be-8710-0e43d11ca0f5; _hjIncludedInSessionSample=1; _hjAbsoluteSessionInProgress=0; utag_main=v_id:017661d487130014f014011f6a1903083001607b009dc$_sn:46$_se:2$_ss:0$_st:1612430402132$ses_id:1612428587150%3Bexp-session$_pn:2%3Bexp-session$_prevVtSource:directTraffic%3Bexp-1612432188116$_prevVtCampaignCode:%3Bexp-1612432188116$_prevVtDomainReferrer:%3Bexp-1612432188116$_prevVtSubdomaninReferrer:%3Bexp-1612432188116$_prevVtUrlReferrer:%3Bexp-1612432188116$_prevVtCampaignLinkName:%3Bexp-1612432188116$_prevCompletePageName:11%3A%3Amunicipios%3A%3Awww.idealista.com%2Fventa-viviendas%2Fmalaga-provincia%2Fmunicipios%3Bexp-1612432202674$_prevAdId:undefined%3Bexp-1612432202678$_prevAdOriginTypeRecommended:undefined%3Bexp-1612432188122; cookieSearch-1="/venta-viviendas/alhaurin-de-la-torre-malaga/:1612428621349"; contacta7afeee3-b560-41be-8710-0e43d11ca0f5="{'email':null,'phone':null,'phonePrefix':null,'friendEmails':null,'name':null,'message':null,'message2Friends':null,'maxNumberContactsAllow':10,'defaultMessage':true}"; WID=30d152d7aa58f317|YBu1U|YBu1K; datadome=_mh3ZwMp1N7cCuAU97bOpV~jqrcC6DU5IPnf5Dmgd7m_eiSwNP~mDkj~SFbpE.rVaPy6DlAEieP7IpvY~Nm8c_Nc~gEMqCs3AaNY13xlss; criteo_write_test=ChUIBBINbXlHb29nbGVSdGJJZBgBIAE'''},
        {"userUUID" : '''9f912be7-1a25-428a-a7ea-27205641eca6; SESSION=400828d1-373a-4097-9c03-8b640fc0c7b5; criteo_write_test=ChUIBBINbXlHb29nbGVSdGJJZBgBIAE; cto_lwid=97e05629-8c3a-4b4a-8ec7-d941cf814588; didomi_token=eyJ1c2VyX2lkIjoiMTc3NmM0MzItYjg3MC02ZmM1LThkMGEtZWZjMGNlYTc1NjdjIiwiY3JlYXRlZCI6IjIwMjEtMDItMDRUMDg6NTg6MDEuMDUxWiIsInVwZGF0ZWQiOiIyMDIxLTAyLTA0VDA4OjU4OjAxLjA1MVoiLCJ2ZXJzaW9uIjoyLCJwdXJwb3NlcyI6eyJlbmFibGVkIjpbImFuYWxpdGljYXMtZHlGVkdSZTgiLCJnZW9sb2NhdGlvbl9kYXRhIl19LCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZmFjZWJvb2siLCJ0d2l0dGVyIiwiZ29vZ2xlIiwiYzptaXhwYW5lbCIsImM6aWRlYWxpc3RhLWZlUkVqZTJjIiwiYzppZGVhbGlzdGEtTHp0QmVxRTMiLCJjOmFidGFzdHktTExrRUNDajgiLCJjOmhvdGphciIsImM6eWFuZGV4bWV0cmljcyIsImM6YmVhbWVyLUg3dHI3SGl4IiwiYzpjaGFyYmVhdC1aNFFrOENhaCJdfSwiYWMiOiJBa3VBQ0Frcy5BQUFBIn0=; euconsent-v2=CPBFSb7PBFSb7AHABBENBLCoAP_AAAAAAAAAF5wAwAWgBbAXmAAAAgNAnABUAFYALgAhgBkADLAGoANkAdgA_ACAAEFAIwAUsAp4BV4C0ALSAawA3gB1QD5AIbAQ6Ai8BIgCbAE7AKRAXIAwIBhIDDwGMAMnAZyAzwBnwDkgHKEoHQACAAFgAUAAyABwAEUAMAAxAB4AEQAJgAVQAuABfADEAGYANoAhABDQCIAIkARwAowBSgC3AGEAMoAaoA2QB3gD8AIwARwAp4BV4C0ALSAXUAxQBuADiAHUAPkAh0BF4CRAE2ALFAWwAu0BeYDDwGRAMnAZYAzkBngDPgGkANYAcAUgmgALgAoACoAGQAOQAfACAAEQAKoAYABjADQANQAeQBDAEUAJgATwApABVACwAFwAL4AYgAzABzAEIAIaARABEgCjAFKALEAW4AwgBlADRAGqANkAd8A-wD9AIsARgAjgBKQCggFDAKuAVsAuYBeQDaAG4APQAh0BF4CRAE2AJ2AUOApoBWwCxQFsALgAXIAu0BeYDDQGHgMYAZEAyQBk4DLgGcgM8AZ9A0gDSYGsAayA2OByYHKAOXIQPwAFgAUAAyACIAFQALgAYgBDACYAFUALgAXwAxABmADeAHoARwAsQBhADKAGoAN8Ad8A-wD8AH-ARgAjgBKQCggFDAKeAVeAtAC0gFzAL8AYoA2gB1AD0AJBASIAlQBNgCmgFigLRgWwBbQC4AFyALtAYeAxIBkQDJwGcgM8AZ8A0QBpIDSwHAAOSAdGOg2AALgAoACoAGQAOQAfACAAEQAKgAXQAwADGAGgAagA8AB9AEMARQAmABPgCqAKwAWAAuABfADEAGYAN4AcwA9ACEAENAIgAiQBHQCWAJgATQAowBSgCxAFvAMIAwwBkADKAGiANQAbIA3wB3gD2gH2AfoA_wCBwEWARgAjkBKQEqAKCAU8Aq4BYoC0ALSAXMAuoBeQC_AGKANoAbgA4kB0wHUAPQAhsBDoCIgEXgJBASIAlQBNgCdgFDgKaAVYAsUBaEC2ALZAXAAuQBdoC7wF5gMGAYSAw0Bh4DEgGMAMeAZIAycBlQDLAGXAM5AZ8A0SBpAGkgNLAacA1gBsYDi4HJAcqA5cB0YSC2AAgABcAFAAVAAyAByADwAQAAiABUADCAGgAagA8gCGAIoATAAnwBVAFYALAAXAA3gBzAD0AIQAQ0AiACJAEdAJYAlwBNAClAFuAMMAZAAy4BqAGqANkAd4A9gB8QD7AP0AgABA4CLgIwARoAjgBKQCggFLAKeAVcAuYBfgDFAGsANoAbgA3gBxAD0AHyAQ2Ah0BFQCLwEiAJiATKAmwBOwChwFIgLFAWgAtgBcgC7wF5gMCAYMAwkBhoDDwGRAMkAZOAy4BnIDPgGkANOgawBrMDkQOVAcuA6MZAdAAoACoAIYATAAuACOAGWANQAdkA-wD8AIwARwApYBVwCtgG8ATEAmwBaIC2AF5gMCAYeAyIBnIDPAGfAOSAcoKgQAAUABUAEMAJgAXABHADLAGoAOwAfgBGACOAFLAKvAWgBaQDeAJBATEAmwBTYC2AFyALzAYEAw8BkQDOQGeAM-AbkA5IBygAAA.f_gAAAAAAAAA; utag_main=v_id:01776c43280b0025cfd3ec585cf003073001d06b009dc$_sn:1$_se:2$_ss:0$_st:1612430881805$ses_id:1612429076494%3Bexp-session$_pn:2%3Bexp-session$_prevVtSource:portalSites%3Bexp-1612432682667$_prevVtCampaignCode:%3Bexp-1612432682667$_prevVtDomainReferrer:idealista.com%3Bexp-1612432682667$_prevVtSubdomaninReferrer:www.idealista.com%3Bexp-1612432682667$_prevVtUrlReferrer:https%3A%2F%2Fwww.idealista.com%2Fen%2F%3Bexp-1612432682667$_prevVtCampaignLinkName:%3Bexp-1612432682667$_prevCompletePageName:11%3A%3Amunicipios%3A%3Awww.idealista.com%2Fen%2Fventa-viviendas%2Fa-coruna-provincia%2Fmunicipios%3Bexp-1612432682670$_prevAdId:undefined%3Bexp-1612432682672$_prevAdOriginTypeRecommended:undefined%3Bexp-1612432682674; xtvrn=$352991$; xtan352991=2-anonymous; xtant352991=1; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%22a9a00e0d-b11f-48a0-b21a-7027cee165c1%22%2C%22options%22%3A%7B%22end%22%3A%222022-03-08T08%3A58%3A05.287Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-582065-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; cookieSearch-1="/venta-viviendas/mugardos-a-coruna/:1612429086350"; contact400828d1-373a-4097-9c03-8b640fc0c7b5="{'email':null,'phone':null,'phonePrefix':null,'friendEmails':null,'name':null,'message':null,'message2Friends':null,'maxNumberContactsAllow':10,'defaultMessage':true}"; WID=503ae74b1083bcf5|YBu3I|YBu3E; datadome=LKGd3GxORaxDfU05LiawjqfT4jaIhmN3g7-8~KWQVHiCHkKZIs5BK.NCto4s.7HAnafsJYXwJtsPxU6YU0y1Y8F_tqzW1P87XWyKMr7UtY'''},
        {'userUUID' : '''7050dc9a-204d-4447-8813-6c76c9af589d; SESSION=184864b8-809a-413a-9610-708219ca54c0; cto_lwid=a0ce9e12-c57e-4f4a-b81a-87da059d6ba5; didomi_token=eyJ1c2VyX2lkIjoiMTc3NmMzMTctNjJhMS02MDZlLTg3N2YtNDcyMjEwZjlkM2M3IiwiY3JlYXRlZCI6IjIwMjEtMDItMDRUMDg6Mzg6NDguNTM5WiIsInVwZGF0ZWQiOiIyMDIxLTAyLTA0VDA4OjM4OjQ4LjUzOVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZmFjZWJvb2siLCJ0d2l0dGVyIiwiZ29vZ2xlIiwiYzptaXhwYW5lbCIsImM6aWRlYWxpc3RhLWZlUkVqZTJjIiwiYzppZGVhbGlzdGEtTHp0QmVxRTMiLCJjOmFidGFzdHktTExrRUNDajgiLCJjOmhvdGphciIsImM6eWFuZGV4bWV0cmljcyIsImM6YmVhbWVyLUg3dHI3SGl4IiwiYzpjaGFyYmVhdC1aNFFrOENhaCJdfSwicHVycG9zZXMiOnsiZW5hYmxlZCI6WyJhbmFsaXRpY2FzLWR5RlZHUmU4IiwiZ2VvbG9jYXRpb25fZGF0YSJdfSwidmVyc2lvbiI6MiwiYWMiOiJBa3VBQ0Frcy5BQUFBIn0=; euconsent-v2=CPBFPn1PBFPn1AHABBENBLCoAP_AAAAAAAAAF5wAwAWgBbAXmAAAAgNAnABUAFYALgAhgBkADLAGoANkAdgA_ACAAEFAIwAUsAp4BV4C0ALSAawA3gB1QD5AIbAQ6Ai8BIgCbAE7AKRAXIAwIBhIDDwGMAMnAZyAzwBnwDkgHKEoHQACAAFgAUAAyABwAEUAMAAxAB4AEQAJgAVQAuABfADEAGYANoAhABDQCIAIkARwAowBSgC3AGEAMoAaoA2QB3gD8AIwARwAp4BV4C0ALSAXUAxQBuADiAHUAPkAh0BF4CRAE2ALFAWwAu0BeYDDwGRAMnAZYAzkBngDPgGkANYAcAUgmgALgAoACoAGQAOQAfACAAEQAKoAYABjADQANQAeQBDAEUAJgATwApABVACwAFwAL4AYgAzABzAEIAIaARABEgCjAFKALEAW4AwgBlADRAGqANkAd8A-wD9AIsARgAjgBKQCggFDAKuAVsAuYBeQDaAG4APQAh0BF4CRAE2AJ2AUOApoBWwCxQFsALgAXIAu0BeYDDQGHgMYAZEAyQBk4DLgGcgM8AZ9A0gDSYGsAayA2OByYHKAOXIQPwAFgAUAAyACIAFQALgAYgBDACYAFUALgAXwAxABmADeAHoARwAsQBhADKAGoAN8Ad8A-wD8AH-ARgAjgBKQCggFDAKeAVeAtAC0gFzAL8AYoA2gB1AD0AJBASIAlQBNgCmgFigLRgWwBbQC4AFyALtAYeAxIBkQDJwGcgM8AZ8A0QBpIDSwHAAOSAdGOg2AALgAoACoAGQAOQAfACAAEQAKgAXQAwADGAGgAagA8AB9AEMARQAmABPgCqAKwAWAAuABfADEAGYAN4AcwA9ACEAENAIgAiQBHQCWAJgATQAowBSgCxAFvAMIAwwBkADKAGiANQAbIA3wB3gD2gH2AfoA_wCBwEWARgAjkBKQEqAKCAU8Aq4BYoC0ALSAXMAuoBeQC_AGKANoAbgA4kB0wHUAPQAhsBDoCIgEXgJBASIAlQBNgCdgFDgKaAVYAsUBaEC2ALZAXAAuQBdoC7wF5gMGAYSAw0Bh4DEgGMAMeAZIAycBlQDLAGXAM5AZ8A0SBpAGkgNLAacA1gBsYDi4HJAcqA5cB0YSC2AAgABcAFAAVAAyAByADwAQAAiABUADCAGgAagA8gCGAIoATAAnwBVAFYALAAXAA3gBzAD0AIQAQ0AiACJAEdAJYAlwBNAClAFuAMMAZAAy4BqAGqANkAd4A9gB8QD7AP0AgABA4CLgIwARoAjgBKQCggFLAKeAVcAuYBfgDFAGsANoAbgA3gBxAD0AHyAQ2Ah0BFQCLwEiAJiATKAmwBOwChwFIgLFAWgAtgBcgC7wF5gMCAYMAwkBhoDDwGRAMkAZOAy4BnIDPgGkANOgawBrMDkQOVAcuA6MZAdAAoACoAIYATAAuACOAGWANQAdkA-wD8AIwARwApYBVwCtgG8ATEAmwBaIC2AF5gMCAYeAyIBnIDPAGfAOSAcoKgQAAUABUAEMAJgAXABHADLAGoAOwAfgBGACOAFLAKvAWgBaQDeAJBATEAmwBTYC2AFyALzAYEAw8BkQDOQGeAM-AbkA5IBygAAA.f_gAAAAAAAAA; xtvrn=$352991$; xtan352991=2-anonymous; xtant352991=1; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%2231f899a9-b07c-4cea-a927-170b0c3a9a0d%22%2C%22options%22%3A%7B%22end%22%3A%222022-03-08T08%3A38%3A56.235Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-582065-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; _hjTLDTest=1; _hjid=416d6cc7-5275-4295-90dc-4295817ad7f2; _hjFirstSeen=1; _hjIncludedInSessionSample=1; _hjAbsoluteSessionInProgress=0; TestIfCookie=ok; TestIfCookieP=ok; contact184864b8-809a-413a-9610-708219ca54c0="{'email':null,'phone':null,'phonePrefix':null,'friendEmails':null,'name':null,'message':null,'message2Friends':null,'maxNumberContactsAllow':10,'defaultMessage':true}"; cookieSearch-1="/venta-viviendas/a-coruna-a-coruna/:1612427961986"; send184864b8-809a-413a-9610-708219ca54c0="{'friendsEmail':null,'email':null,'message':null}"; WID=4089c4757ae68fb2|YBuy2|YBuyi; datadome=KJGaA8seSxTt9kBJ6pQHQuNfW-flXE-Y0JloR5T-XI-QG84-wPQuzCA-5eWu6fOQ9AasmnXKDoUAXV7D3hvn4FPgf2bsgUOEdK2R9ID87W; criteo_write_test=ChUIBBINbXlHb29nbGVSdGJJZBgBIAE; utag_main=v_id:01776c316fcc0043f88da2ea2ef803082001a07a009dc$_sn:1$_se:5$_ss:0$_st:1612429794965$ses_id:1612427915215%3Bexp-session$_pn:5%3Bexp-session$_prevVtSource:directTraffic%3Bexp-1612431528595$_prevVtCampaignCode:%3Bexp-1612431528595$_prevVtDomainReferrer:%3Bexp-1612431528595$_prevVtSubdomaninReferrer:%3Bexp-1612431528595$_prevVtUrlReferrer:%3Bexp-1612431528595$_prevVtCampaignLinkName:%3Bexp-1612431528595$_prevCompletePageName:11%3A%3Adetail%3A%3A%3A%3A%3A%3Ahome%3Bexp-1612431595114$_prevAdId:91899144%3Bexp-1612431595117$_prevAdOriginTypeRecommended:undefined%3Bexp-1612431528600'''}
    ]

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
        fileExists = os.path.isfile(self.DATAFILE_PATH)
        with open(self.DATAFILE_PATH, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
            if not fileExists:
                writer.writeheader()
            writer.writerow(dict_data)

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
            time.sleep(random.randint(2,6))
            yield scrapy.Request(
                url=startReqUrl,
                callback=self.getAreaUrls,
                cookies=random.choice(self.cookies),
                headers=random.choice(self.headers)
            )

    def getAreaUrls(self, response):
        provAreas = response.xpath("//ul[@id='location_list']/li/ul/li")
        for area in self.areaLi:                
                for provArea in provAreas:
                    areaCount = str(provArea.xpath("normalize-space(.//text()[2])").get())                  
                    if "all" in self.areaLi:
                        if int(areaCount.replace(".","")) > 1800:
                            time.sleep(random.randint(1,3))
                            yield scrapy.Request(
                                url=f'''https://www.idealista.com{provArea.xpath(".//a/@href").get()}''',
                                callback=self.getSubAreaUrls,
                                cookies=random.choice(self.cookies),
                                headers=random.choice(self.headers)
                            )
                        else:
                            time.sleep(random.randint(1,3))
                            yield scrapy.Request(
                                url=f'''https://www.idealista.com{provArea.xpath(".//a/@href").get()}''',
                                callback=self.getListings,
                                cookies=random.choice(self.cookies),
                                headers=random.choice(self.headers)
                            )
                    else:
                        inp = area
                        mch = provArea.xpath("normalize-space(.//a/text())").get()
                        if difflib.SequenceMatcher(None, f'{inp.lower()}', f'{mch.lower()}').ratio() > 0.8 :
                            if int(areaCount.replace(".","")) > 1800:
                                time.sleep(random.randint(1,3))
                                yield scrapy.Request(
                                    url=f'''https://www.idealista.com{provArea.xpath(".//a/@href").get()}''',
                                    callback=self.getSubAreaUrls,
                                    cookies=random.choice(self.cookies),
                                    headers=random.choice(self.headers)
                                )
                            else:
                                time.sleep(random.randint(1,3))
                                yield scrapy.Request(
                                    url=f'''https://www.idealista.com{provArea.xpath(".//a/@href").get()}''',
                                    callback=self.getListings,
                                    cookies=random.choice(self.cookies),
                                    headers=random.choice(self.headers)
                                )

    def getSubAreaUrls(self, response):
        subArUrls = response.xpath("//nav[@class]//span[contains(@class, 'arrow-dropdown')]/following-sibling::div/ul//strong/following-sibling::ul/li")
        for subArUrl in subArUrls:
            time.sleep(random.randint(1,3))
            yield scrapy.Request(
                url=f'''https://www.idealista.com{subArUrl.xpath(".//a/@href").get()}''',
                callback=self.getListings,
                cookies=random.choice(self.cookies),
                headers=random.choice(self.headers)
            )

    def getListings(self, response):
        subArCount = str(response.xpath("normalize-space(//nav[@class='breadcrumb-geo']/ul/li[last()]/span[@class='breadcrumb-info']/text())").get())
        if int(subArCount.replace(".","")) > 1800:
            time.sleep(random.randint(1,3))
            yield scrapy.Request(
                url=response.url,
                callback=self.getSubAreaUrls,
                cookies=random.choice(self.cookies),
                headers=random.choice(self.headers)
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
                    time.sleep(random.randint(1,3))
                    yield scrapy.Request(
                        url=adUrl,
                        callback=self.parse,
                        cookies=random.choice(self.cookies),
                        headers=random.choice(self.headers),
                        meta={
                            'image': img,
                            'propertyType': propType
                        }
                    )
            nextPage = response.xpath("//span[text()='Siguiente']/parent::a/@href").get()
            if nextPage:
                time.sleep(random.randint(1,3))
                yield scrapy.Request(
                    url=f"https://www.idealista.com{nextPage}",
                    callback=self.getListings,
                    cookies=random.choice(self.cookies),
                    headers=random.choice(self.headers)
                )

    def parse(self, response):
        onrName = response.xpath("normalize-space(//span[@class='particular']/input/@value)").get()
        phone = response.xpath("normalize-space(//p[contains(@class, 'Phone')]/text())").get()
        if onrName and phone:
            addr_raw = response.xpath("//h2[text()='Ubicación']/following-sibling::ul/li/text()").getall()
            ref_no = response.xpath("normalize-space(//p[contains(text(), 'Anuncio')]/text())").get()
            # area = response.xpath("normalize-space(//h2[text()='Características básicas']/following-sibling::div/ul/li[contains(text(),'m²')]/text())").get()
            area = response.xpath("normalize-space(//span[text()=' m² ']/span/text())").get()
            bed = response.xpath("normalize-space(//h2[text()='Características básicas']/following-sibling::div/ul/li[contains(text(),'habit')]/text())").get()
            bath = response.xpath("normalize-space(//h2[text()='Características básicas']/following-sibling::div/ul/li[contains(text(),'baño')]/text())").get()
            
            dict_data= {
                'Property Title': response.xpath("normalize-space(//h1/span/text())").get(),
                # 'Area in meter sq': area.split(" ")[0],
                'Area in meter sq': area,
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
            print(dict_data,"\n")
            self.writeCSV(dict_data, ["Property Title", "Area in meter sq", "Bed", "Bath", "Price", "Owner Name", "Phone", "Reference No", "Type", "Rent/Sale", "Address", "Image", "Url"])
