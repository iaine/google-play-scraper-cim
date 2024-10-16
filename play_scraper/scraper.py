"""
Library to extend the existing Google Play Scraper. 
"""
from bs4 import BeautifulSoup
from google_play_scraper import search, app
import requests
import pandas as pd

class PlayStoreScraper():
    
    def __init__(self) -> None:
        pass

    def get_app_ids_for_query(self, term, country="gb",lang="en", num=25) -> list:
        '''
        Returns app ids for a search
        '''
        results = search(term, lang=lang, country=country,n_hits=num)
        apps_search = [x["appId"] for x in results]
        return apps_search
    
    def get_multiple_app_details(self, results, country="gb",lang="en",) -> list:
        '''
        Gets multiple app details
        '''
        rs = []
        for result in results:
            rs.append(self.get_app_details(result,lang=lang, country=country))

        return rs
    
    def get_app_details (self, app_id, country = "gb", lang = "en") -> list:
        '''
        Gets a single app details
        '''
        return app(app_id,lang=lang, country=country)
    
    def get_similar_app_ids_for_app(self, app_id, country = "gb", lang = "en") -> list:
        '''
        Finds the similar apps page url and returns a list of
        similar apps scraped from it. 
        '''
        base = 'https://play.google.com/'
        url = "{}store/apps/details?id={}".format(base, app_id)
        soup = self._parse_url_html(url)

        sim=[]
        
        for simlink in soup.find_all('a'):
            if simlink['href'].startswith('/store/apps/collection/cluster'):      
                soup1 = self._parse_url_html(base + simlink['href'])
                for link in soup1.find_all('a'):
                    if link['href'].startswith('/store/apps/details'):
                        sim.append(link['href'].replace('/store/apps/details?id=',''))
        return sim
    
    def get_app_ids_for_developer(self, developer_id, country="gb", lang="en") -> list:
        '''
        Find apps by developer. 
        '''
        
        #url = "https://play.google.com/store/apps/developer?id={}".format(developer_id)
        base = 'https://play.google.com/'
        url = "{}store/apps/details?id={}".format(base, app_id)
        soup = self._parse_url_html(url)
        devs = []
        for link in soup.find_all('a'):
            if link['href'].startswith('/store/apps/dev?id='):
                soup1 = self._parse_url_html(base + link['href'])
                for link in soup1.find_all('a'):
                    if link['href'].startswith('/store/apps/details'):
                        devs.append(link['href'].replace('/store/apps/details?id=',''))
            if link['href'].startswith('/store/apps/developer?id='):
                soup1 = self._parse_url_html(base + link['href'])
                for link in soup1.find_all('a'):
                    if link['href'].startswith('/store/apps/details'):
                        devs.append(link['href'].replace('/store/apps/details?id=',''))

        return devs


    ## Helper Functions 

    def _parse_url_html (self, url):
        '''
        Get page and return parsed object
        '''
        page = requests.get(url)
        parse = BeautifulSoup(page.content, "html.parser")
        return parse

    def json_to_dataframe (self, results_data):
        """
        Convert the generator object into a list and then JSON
        : param object results_data: the generator object to be converted
        : return data frame
        """
        if isinstance(results_data, dict):
            return pd.json_normalize(results_data)
        else:
            return pd.json_normalize(list(results_data))


    def convert_json_csv (self, filename, json_data):
        """
            Write the data to a defined CSV file
            : param str filename: the filename to be written
            : param object json_data: the results data to be written. 
        """
        try:
            df = self.json_to_dataframe(json_data)
            df.to_csv(filename, index=False, encoding="utf-8") 
        except Exception as e:
            print(e)