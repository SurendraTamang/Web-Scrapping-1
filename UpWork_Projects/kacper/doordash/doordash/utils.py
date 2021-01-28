from http.cookies import SimpleCookie


def cookie_parser():
    cookie_string = '''ajs_anonymous_id=%22ac5b9841-83ad-4a60-a306-8525f2ebcdb7%22; amplitude_idundefineddoordash.com=eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==; _gcl_au=1.1.1177683341.1610538431; dd_device_id=dx_10b62e99e4c34bbb9eccc104ec92fa81; dd_login_id=lx_51c85bfdf78f439685a6ddda2a82d26f; dd_device_id_2=dx_91b75e15a79a4965804f12a6e7d6e760; _fbp=fb.1.1610538435216.164603983; optimizelyEndUserId=oeu1610538471496r0.5967561599735574; __cfduid=d4350929517541fe3db3909edca9ba4741610538492; __cfruid=e5728175e532c5a920c2f195b54c1a5ccc8488e1-1610538493; _vwo_uuid_v2=D933D69F2D27D83D8E30981DFBDD2891C|896bb89696b0734ee79c8b13bd6f1c42; dd_session_id_2=sx_1fd2f6d7db2e4cf1a25f3b05e3552755; dd_guest_id=baacc57f-242d-4bc2-8722-26625920fc5b; dd_session_id=sx_34724b65220f4ef0bd0364ecfb4c4ddf; doordash_attempt_canary=0; amplitude_id_8a4cf5f3981e8b7827bab3968fb1ad2bdoordash.com=eyJkZXZpY2VJZCI6IjNjMTQwOTY3LWRhZTMtNDMxZC04ZGE2LTA3N2JmYTgyMjEzYlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTYxMTgxODQyMTYyNiwibGFzdEV2ZW50VGltZSI6MTYxMTgxODQyMTY0NSwiZXZlbnRJZCI6MTk4LCJpZGVudGlmeUlkIjo0Miwic2VxdWVuY2VOdW1iZXIiOjI0MH0=; _gid=GA1.2.217304333.1611818422; _gat_UA-36201829-6=1; _uetsid=48ea2460613911ebad67a3c33772ef15; _uetvid=1409f770559511eb90c7212a351df239; _ga=GA1.1.107515329.1610538432; _ga_J4BQM7M3T2=GS1.1.1611818421.3.1.1611818453.28'''
    cookie = SimpleCookie()
    cookie.load(cookie_string)

    cookies = {}

    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    
    return cookies