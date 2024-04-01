from functions import get_all_links_by_class, create_full_urls, get_directory_files, random_sleep
from seleniumbase import Driver
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import json
import time
import os

def sanitize_title_for_file_path(title):
    import re
    safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
    safe_title = safe_title.strip()

    max_length = 25
    safe_title = safe_title[:max_length]
    return safe_title

def remove_from_file(filepath):
    with open(filepath, 'r') as file:
        data = json.loads(file.read())
    if len(data) != 0:
        with open(filepath, 'w') as file:
            json_data = json.dumps(data[1:], indent=4)
            file.write(json_data)
    else:
        os.remove(filepath)
        print(f'Done with {filepath}')

url = "https://www.thekitchn.com/recipes"
class_name='jsx-1017570244'

def get_recipe(driver, url):
    driver.open(url)

    time.sleep(2)

    page_source = driver.get_page_source()

    soup = BeautifulSoup(page_source, 'html.parser')
    recipe = {
        'title': '',
        'ingredients': {},
        'steps': [],
    }
    try:
        title = soup.find('h1', class_='Post__headline').text.strip()
        recipe['title'] = title
        ingredient_groups = soup.find('div', class_='Recipe__ingredientsGroups')
        for group in ingredient_groups:
            ingredient_title = group.find('h4')
            if ingredient_title is not None:
                ingredient_title = ingredient_title.text.strip()
            else:
                ingredient_title = 'list'
            recipe['ingredients'][ingredient_title] = []
            ingredients = group.find_all('li')
            for ingredient in ingredients:
                ing_object = {}
                ingredient_name = ingredient.find('span', class_='Recipe__ingredientName')
                if ingredient_name is not None:
                    ing_object['name'] = ingredient_name.text.strip()
                ing_quantity = ingredient.find('span', class_='Recipe__ingredientQuantity')
                if ing_quantity is not None:
                    ing_object['quantity'] = ing_quantity.text.strip()
                ing_measureUnit = ingredient.find('span', class_='Recipe__ingredientMeasurementUnit')
                if ing_measureUnit is not None:
                    ing_object['unit'] = ing_measureUnit.text.strip()
                recipe['ingredients'][ingredient_title].append(ing_object)
        instruction_groups = soup.find_all('div', class_='Recipe__instructionsGroup')
        for ins_group in instruction_groups:
            group_steps = ins_group.find_all('li', class_='Recipe__instructionStep')
            step_number = 1
            for step in group_steps:
                recipe['steps'].append({step_number: step.text.strip()})
                step_number += 1
        safe_file_path = sanitize_title_for_file_path(title)
        filepath = f'recipes/{safe_file_path}.txt'
        with open(filepath, 'w') as file:
            file.write(json.dumps(recipe, indent=4))

    except (TypeError, AttributeError):
        with open('failure/links.txt', 'r') as file:
            json_data = file.read()
            data = json.loads(json_data)
        with open('failure/links.txt', 'w') as file:
            data.append(url)
            json_data = json.dumps(data, indent=4)
            file.write(json_data)

def write_links_selenium(url, filename, class_name):
    # Create a new instance of the Chrome driver
    driver = uc.Chrome()

    # Navigate to the webpage
    driver.get(url)

    # Extract the page source after waiting for some time for potential JavaScript execution
    time.sleep(2)  # Wait for 5 seconds to allow JavaScript to execute (adjust as needed)
    page_source = driver.page_source

    # Now, you can process the page source using Beautiful Soup or any other library
    # For example:
    soup = BeautifulSoup(page_source, 'html.parser')

    links = get_all_links_by_class(soup, class_name)

    full_links = create_full_urls('https://www.thekitchn.com', links)
    with open(filename, 'w') as file:
        file.write(json.dumps(full_links))

    # Finally, close the browser
    driver.quit()

def write_links_from_links(filepath, class_name):
    with open(filepath, 'r') as file:
        links = json.loads(file.read())
        for link in links:
            link_suffix = link.split('/')[-1] + '.txt'
            write_links_selenium(link, link_suffix, class_name)
            random_sleep(10, 120)

def scrape_recipes(directory):
    filepaths = get_directory_files(directory)
    driver = Driver(headless=True, uc=True)
    for filepath in filepaths:
        try:
            with open(filepath, 'r') as file:
                json_data = file.read()
                links = json.loads(json_data)
                for link in links:
                    get_recipe(driver, link)
                    remove_from_file(filepath)
                    print(link)
                    time.sleep(5)
        except KeyboardInterrupt:
            pass
        finally:
            driver.quit()
        
if __name__ == '__main__':
    # scrape_recipes('link_files/')
    files = get_directory_files('recipes/')
    print(len(files))
