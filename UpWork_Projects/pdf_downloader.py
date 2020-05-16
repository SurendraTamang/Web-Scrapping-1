import requests
from urllib.request import urlopen
from urllib.request import urlretrieve
import cgi
import os.path

def retrive_file_name(url):
    #url = 'https://material.ibear.pt/BTHorarios2019/FileGet.aspx?FileId=5601'
    remotefile = urlopen(url)
    blah = remotefile.info()['Content-Disposition']
    _, params = cgi.parse_header(blah)
    filename = params["filename"]
    #urlretrieve(url, filename)
    return filename

def pdf_downloader():
    for i in range (0,10000):
        
        cntr = ''
        l = len(str(i))

        if l<4:            
            for _ in range(0,(4-l)):
                cntr += '0'
            cntr += str(i)
        else:
            cntr = str(i)
        
        try:
            url = f"https://material.ibear.pt/BTHorarios2019/FileGet.aspx?FileId={cntr}"
            response = requests.get(url)
            if response.status_code == 200:
                file_name = retrive_file_name(url)
                file_path1 = f'D:/upworkWorkspace/25032020_pdf_downloader/downloads/{file_name}'
                file_path2 = f'D:/upworkWorkspace/25032020_pdf_downloader/downloads/copy_{cntr}_{file_name}'
                if not os.path.isfile(file_path1) and not os.path.isfile(file_path2):
                    print(file_name)
                    with open(file_path1, 'wb') as f:
                        f.write(response.content)
                else:
                    print(f'copy_{cntr}_{file_name}')
                    with open(file_path2, 'wb') as f:
                        f.write(response.content)
            else:
                print("Counter: ", cntr)
        except:
            pass
    

pdf_downloader()