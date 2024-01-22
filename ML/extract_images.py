import requests
from bs4 import BeautifulSoup
import os


def extract(search_term,base_dir="ML/"):

    # define the search term and URL
    #search_term = 'cats'
    url = f'https://www.google.com/search?q={search_term}&tbm=isch'

    # create a folder for the downloaded images
    if not os.path.exists(base_dir+search_term):
        os.mkdir(base_dir+search_term)

    # download the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # extract the image URLs and download them
    image_tags = soup.find_all('img')
    for i, img in enumerate(image_tags):
        try:
            img_url = img['src']
            # ignore data URLs and other non-image sources
            if not img_url.startswith('data:'):
                img_data = requests.get(img_url).content
                with open(f'{base_dir}{search_term}/{i}.jpg', 'wb') as f:
                    f.write(img_data)
        except:
            pass