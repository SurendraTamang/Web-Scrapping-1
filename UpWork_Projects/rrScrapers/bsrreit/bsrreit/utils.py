from http.cookies import SimpleCookie

def cookie_parser():
    cookie_string = '''_ga=GA1.2.1849973957.1601865499; _gid=GA1.2.501218214.1601865499; ARRAffinity=1065498437e49ed27544ec9e123507371f88b62e500ea156753f5a95459fa30f'''
    cookie = SimpleCookie()
    cookie.load(cookie_string)

    cookies = {}

    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    
    return cookies