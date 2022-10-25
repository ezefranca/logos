import wget
import re
import os

script_dir = os.path.dirname(__file__)
images_dir = script_dir + '/images/'
script_dir = script_dir + '/files/'

try: 
    os.mkdir(images_dir) 
except OSError as error: 
    pass

images_file = open(script_dir + 'images.txt', 'r')
images = images_file.readlines()

names_file = open(script_dir + 'names.txt', 'r')
names = names_file.readlines()

for i, (name, image) in enumerate(zip(names, images)):
    image_name = re.sub('\s', '', name.strip()) + '.png'
    image_path = images_dir + image_name.lower()
    print(f'\n [ downloading {i + 1} of {len(names)} ]')
    try:
        wget.download(image, image_path)
    except Exception as e:
        print(f"Could not download file {image}")
        print(e)
        pass