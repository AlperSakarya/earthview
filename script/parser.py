import urllib.request
import json
from bs4 import BeautifulSoup
import concurrent.futures

result = []

with open('output.txt', 'a') as file:
    for x in range(1000, 7030):
        try:
            print("Fetching " + str(x) + " ...")
            url = f'https://earthview.withgoogle.com/{x}'
            with urllib.request.urlopen(url) as response:
                html = response.read()
                soup = BeautifulSoup(html, "lxml")
                
                region_element = soup.find("div", class_="content__location__region")
                country_element = soup.find("div", class_="content__location__country")
                everything = soup.find("a", id="globe", href=True)
                
                if region_element:
                    region = str(region_element.text.encode('utf-8'))
                else:
                    region = "N/A"  # or any default value
                    
                if country_element:
                    country = str(country_element.text.encode('utf-8'))
                else:
                    country = "N/A"  # or any default value
                    
                if everything:
                    gmaps_url = everything['href']
                else:
                    gmaps_url = "N/A"  # or any default value
                
                image = 'https://www.gstatic.com/prettyearth/assets/full/' + str(x) + '.jpg'
                result.append({'region': region, 'country': country, 'map': gmaps_url, 'image': image})

        except urllib.request.HTTPError as e:
            continue

    json_results = json.dumps(result)
    file.write(json_results)
