import scrapy
import pandas as pd



def get_urls(path='../data/brasseries.csv'):
    """ Returns url links acquired during Google Maps API calls """
    df = pd.read_csv(path)
    return df['website'].dropna().to_list()
    
class MenuSpider(scrapy.Spider):
    name = "menu"
    start_urls = get_urls()
    keywords = ['la carte', 'le menu', 'menu', 'carte']


    def parse(self, response):
        matching_links = []

        # Look for all the 'a' tags on the page
        links = response.xpath('//a')
        
        for link in links:
            # Check the text of the link
            link_text = link.xpath('normalize-space(text())').get().lower()
            for keyword in self.keywords:
                if keyword in link_text:
                    url = link.xpath("./@href").get()
                    if url not in matching_links:
                        matching_links.append(url)
            # # Check the class and id attributes for the keywords
            # link_class = link.attrib.get('class', '').lower()
            # link_id = link.attrib.get('id', '').lower()

            # # Check if any of the keywords appear in the link's text, class, or ID
            # if any(keyword.lower() in (link_text or '') for keyword in self.keywords) or \
            #    any(keyword.lower() in link_class for keyword in self.keywords) or \
            #    any(keyword.lower() in link_id for keyword in self.keywords):
                
            #     # If the link matches the criteria, add it to the list
            #     matching_links.append(link.attrib.get('href'))

        # If there are matching links, yield them to be processed
        if matching_links:
            yield {
                'url': response.url,
                'matching_links': matching_links
            }
