import scrapy
import pandas as pd
from collections import defaultdict


def get_urls(path='../data/interim/brasseries_w_link.csv'):
    """ Returns url links acquired during Google Maps API calls """
    df = pd.read_csv(path)
    return df['website'].dropna().to_list()
    
def fix_link(link, response):
    if link:
        if "@" in link:
            return None
        if 'http' not in link:
            base_url = response.url
            if not base_url.endswith("/"):
                base_url = base_url + "/"
            if link.startswith("/"):
                link = link.strip("/")
                return base_url + link
    else:
        return link

class MenuSpider(scrapy.Spider):
    name = "menu"
    start_urls = get_urls()
    keywords = ['la carte', 'le menu', 'menu', 'carte', 'pdf']
    
    def get_matches(self, tag):
        attr = ""
        url = tag.xpath("./@href").get()
        attr = attr + url if url else attr
        tag_text = tag.xpath("normalize-space(text())").get()
        attr = attr + tag_text if tag_text else attr
        tag_id = tag.xpath("./@id").get()
        attr = attr + tag_id if tag_id else attr
        tag_class = tag.xpath("./@class").get()
        attr = attr + tag_class if tag_class else attr
        if attr:
            if any(keyword in attr for keyword in self.keywords) and url:
                return url
        return None

    def parse(self, response):
        htmls = []
        possible_matches = []
        pdfs = []
        images = []
        a_tags = response.xpath("//a")

        for a_tag in a_tags:
            link = a_tag.xpath("./@href").get()
            if link:
                if link and '.pdf' in link and link not in pdfs:
                    pdfs.append(link)
                elif link and ('.jpg' in link or '.jpeg' in link or '.png' in link) and link not in images:
                    images.append(link)
                elif link and link not in htmls:
                    htmls.append(link)
        yield {
                "website": response.url,
                "htmls": htmls,
                "pdfs": pdfs,
                "images": images
                }


            
    def parse_deeper(self, response):
        website = ""
        for k,v in self.dic.items():
            if response.url in v:
                website = k 

        if website:
            self.dic2[website]
            possible_matches = []
            try:
                a_tags = response.xpath("//a")
                for a_tag in a_tags:
                    attr = ""
                    url = a_tag.xpath("./@href").get()
                    attr = attr + url if url else attr
                    a_tag_text = a_tag.xpath("normalize-space(text())").get()
                    attr = attr + a_tag_text if a_tag_text else attr
                    tag_id = a_tag.xpath("./@id").get()
                    attr = attr + tag_id if tag_id else attr
                    tag_class = a_tag.xpath("./@class").get()
                    attr = attr + tag_class if tag_class else attr
                    if attr:
                        if any(keyword in attr for keyword in self.keywords) and url not in possible_matches and url:
                            possible_matches.append(url)
                            self.dic2[website].append(url)
                yield {"website": website,
                                    "possible_matches": possible_matches}



            except:
                self.dic2[website].append(response.url)
                yield {"website": website,
                       "possible_matches": response.url}
