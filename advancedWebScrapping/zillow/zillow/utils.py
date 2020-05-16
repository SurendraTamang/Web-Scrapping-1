from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs, urlencode
import json


URL = '''https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Miami%2C%20FL%22%2C%22mapBounds%22%3A%7B%22west%22%3A-80.46569227148436%2C%22east%22%3A-80.02898572851561%2C%22south%22%3A25.608075629225908%2C%22north%22%3A25.937033401335228%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12700%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Afalse%2C%22mapZoom%22%3A11%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%7D'''

def cookie_parser():
    cookie_string = '''zguid=23|%24c45f79a8-01cf-4b73-afc5-2134b644cee6; zgsession=1|da801456-05b0-4594-95a8-cdac8d032df2; _ga=GA1.2.1508658913.1585928611; zjs_user_id=null; zjs_anonymous_id=%22c45f79a8-01cf-4b73-afc5-2134b644cee6%22; _gcl_au=1.1.1548337654.1585928616; DoubleClickSession=true; _pxvid=e2e5e495-75c1-11ea-9ad1-0242ac120008; _fbp=fb.1.1585928619493.1468465127; _derived_epik=dj0yJnU9M0QtR2pLczEzRWN0RXJoTmJ2Wl9sbm01aXNkQTktRzImbj1MT0NMbFV6RlBjem83bDNsNWQ0UlV3Jm09NyZ0PUFBQUFBRjZIYW13; _gid=GA1.2.2049307968.1586274214; _pxff_tm=1; JSESSIONID=D6CC354EAA462B8094903F29F412EF81; KruxPixel=true; GASession=true; _gat=1; KruxAddition=true; AWSALB=/Ejk4KIiY6LA/w8pCSTkhIYyd+9bvP3bS3JGF+ESh+5dSRM20H/yCNIShSqKNL1i49pu6Laj7j11vup12V/4+//jiLg4kBGHzUIX3o8uZOEtFUGBepWYECqxfEAZ; AWSALBCORS=/Ejk4KIiY6LA/w8pCSTkhIYyd+9bvP3bS3JGF+ESh+5dSRM20H/yCNIShSqKNL1i49pu6Laj7j11vup12V/4+//jiLg4kBGHzUIX3o8uZOEtFUGBepWYECqxfEAZ; search=6|1588866324093%7Crect%3D25.937033401335228%252C-80.02898572851561%252C25.608075629225908%252C-80.46569227148436%26rid%3D12700%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D0%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%09%0912700%09%09%09%09%09%09'''
    cookie = SimpleCookie()
    cookie.load(cookie_string)

    cookies = {}

    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    
    return cookies


    #print(cookies)
    #print(cookie.items())
# cookie_parser()

def parse_new_url(url, page_number):
    url_parsed = urlparse(url)
    query_string = parse_qs(url_parsed.query)
    search_query_state = json.loads(query_string.get('searchQueryState')[0])
    search_query_state['pagination'] = {'currentPage': page_number}
    query_string.get('searchQueryState')[0] = search_query_state
    encoded_qs = urlencode(query_string, doseq=1)
    new_url = f"https://www.zillow.com/search/GetSearchPageState.htm?{encoded_qs}"
    
    return new_url