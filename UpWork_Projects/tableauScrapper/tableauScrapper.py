import requests


img_api_url = "https://public.tableau.com/vizql/tilecache/4A3F460C31624C80AD3D0EDE225DD840-0:0/9100/f57e020587657f67853f14c959c5fdcb4130e985bb3f8ff43f7b0b434c0fcb87/views.10185889182365737109_17797799621814179364.yheader.0.100.png?=1590152907555Z2"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
img_bytes = requests.get(img_api_url, headers={'User-Agent': user_agent}).content

with open('sample_img2.jpg', 'wb') as img_file:
        img_file.write(img_bytes)
        print(f'Image is downloaded !!')