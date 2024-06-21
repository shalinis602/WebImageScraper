#!/home/shalini/anaconda2/bin/python

# import modules, classes, functions
from bs4 import BeautifulSoup
import os
import re
import requests
from urllib.parse import urljoin

# take url as input
url = input('Enter the URL:')
out_folder = input('Enter location where you want to save the images:')

if not os.path.exists(out_folder):
    os.makedirs(out_folder)

# Two HTTP request methods - GET - request data from server & POST -
# submit data to be processed to server
req = requests.get(url)

# parse url
soup = BeautifulSoup(req.text, 'html.parser')

# get all image tags
img_tags = soup.find_all('img')

# get urls of all images, store in a list
urls = [urljoin(url, img['src']) for img in img_tags]

# download images
for image in urls:
    filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', image)
    if not filename:
    	continue

    # get full path to save the image
    image_path = os.path.join(out_folder, filename.group(1))
	    	
    # searches src with .jpg,png,gif ext
    try:
        response = requests.get(image)
        response.raise_for_status()
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {image}")
    except(requests.exceptions.MissingSchema, requests.exceptions.RequestException) as e:
        print(f"Failed to download {image}: {e}")
