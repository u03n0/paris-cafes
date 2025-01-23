from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import re

def scrape_menu_links(url_list):
    # List to store the scraped data
    menu_data = []
    
    # Iterate over each URL in the list
    for url in url_list:
        print(f"Scraping URL: {url}")
        
        # Send a GET request to the URL
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception if the request failed (status code != 200)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            menu_data.append({'url': url, 'menu_link': None, 'error': str(e)})
            continue
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # If the URL is already a direct link to a menu, we can directly store it
        if 'menu' in url.lower():
            menu_data.append({'url': url, 'menu_link': url})
        else:
            # Otherwise, look for potential menu links on the website
            menu_link = find_menu_on_website(soup)
            
            # Store the result
            menu_data.append({'url': url, 'menu_link': menu_link})

    return menu_data


def find_menu_on_website(soup):
    # Search for common menu keywords like "menu", "menus", "food", etc.
    possible_menu_keywords = ['menu', 'menus', 'food', 'carte', 'la carte']
    
    # Find all <a> tags and check if their href attribute contains any of the keywords
    for link in soup.find_all('a', href=True):
        link_href = link['href']
        
        # Search for the presence of menu-related keywords in the link
        if any(keyword in link_href.lower() for keyword in possible_menu_keywords):
            return link_href
    
    # If no menu link found, return None
    return None

def save_all_text_from_page(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: Unable to fetch page {url}")
        return
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract all text from the page
    all_text = soup.get_text(separator="\n", strip=True)  # separator="\n" for better readability
    
    return all_text




df = pd.read_csv("brasseries.csv")
name = df['name'].to_list()
links = df['website'].to_list()[:8]

# # Scrape the URLs
menu_info = scrape_menu_links(links)
menu_links = []
for link in menu_info:
    url = link['url']
    broken = url.split(".")[:3]
    index = 2 if len(broken) == 3 else 1
    domain = "." + broken[index].split("/")[0]
    body = ".".join(broken[:index])
    base = body + domain
    menu = link['menu_link']
    if menu and 'http' not in menu:
        menu_url = base + menu
        menu_links.append(menu_url)


print(len(menu_links))
test = menu_links[0]

stuff = []
for link in menu_links:
    info = save_all_text_from_page(link)
    stuff.append(info)

print(stuff[0])