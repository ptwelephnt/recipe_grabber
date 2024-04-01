
def get_all_links_by_class(soup, class_name):
    hrefs = []

    a_tags = soup.find_all('a', class_=class_name)
    for tag in a_tags:
        href = tag.get('href')
        hrefs.append(href)
    
    return hrefs

def create_full_urls(prefix, hrefs):
    return [prefix + href for href in hrefs]

def get_directory_files(directory_path):
    import os

    filepaths = []
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath):
            filepaths.append(filepath)
    return filepaths

def random_sleep(start, end):
    import time
    import random
    random_time = random.randint(start, end)
    print(random_time)
    time.sleep(random_time)

import json
filepaths = get_directory_files('link_files/')
for filepath in filepaths:
    data = ''
    with open(filepath, 'r') as file:
        json_data = file.read()
        data = json.loads(json_data)
    with open(filepath, 'w') as file:
        json_data = json.dumps(data, indent=4)
        file.write(json_data)