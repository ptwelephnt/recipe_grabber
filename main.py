import requests
from bs4 import BeautifulSoup

url = 'https://delish.com/cooking/recipe-ideas/'

html = requests.get(url)

soup = BeautifulSoup(html.text, 'html.parser')

# a_tags = soup.find_all('a')
# for link in a_tags:
#     href = link.get('href')
#     if 'https://www.delish.com/cooking/recipe-ideas/' in href:
#         print(href)

def interact_with_links(links, function):
    for link in links:
        function(link)

def find_tags(soup, tag):
    tags = soup.find_all(tag)
    return tags

def choose_links(a_tags, prefix):
    chosen_links = []
    for link in a_tags:
        href = link.get('href')
        if prefix == href[:len(prefix)]:
            chosen_links.append(href)
    return chosen_links

if __name__ == '__main__':
    a_tags = find_tags(soup, 'a')
    url_prefix = 'https://www.delish.com/cooking/recipe-ideas/'
    recipe_links = choose_links(a_tags, url_prefix)
    link_html = requests.get(recipe_links[0])
    link_soup = BeautifulSoup(link_html.text, 'html.parser')
    link_a_tags = find_tags(link_soup, 'a')
    prefix = '/cooking/'
    links = choose_links(link_a_tags, prefix)
    recipe_html = requests.get(f'https://www.delish.com{links[5]}')
    recipe_soup = BeautifulSoup(recipe_html.text, 'html.parser')
    list_tags = find_tags(recipe_soup, 'li')
    for list_tag in list_tags:
        class_names = list_tag.get('class')
        if class_names is not None:
            for class_name in class_names:
                if class_name == 'css-gpfiiw':
                    print(list_tag)
    # div_tags = find_tags(recipe_soup, 'div')
    # for div_tag in div_tags:
    #     class_names = div_tag.get('class')
    #     if class_names is not None:
    #         for class_name in class_names:
    #             if class_name == 'ingredients-body':
    #                 print(div_tag)