"""
Library to extend the existing Google Play Scraper. 
"""
from bs4 import BeautifulSoup
from google_play_scraper import search, app
import os
import networkx as nx
import pandas as pd
import requests



class PlayStoreScraper():
    
    def __init__(self) -> None:
        self.base_url = 'https://play.google.com/'

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
        
        url = "{}store/apps/details?id={}".format(self.base_url, app_id)
        url += "&hl={}".format(lang)
        url += "&gl={}".format(country)
        soup = self._parse_url_html(url)

        sim=[]
        
        for simlink in soup.find_all('a'):
            if simlink['href'].startswith('/store/apps/collection/cluster'):      
                soup1 = self._parse_url_html(self.base_url + simlink['href'])
                for link in soup1.find_all('a'):
                    if link['href'].startswith('/store/apps/details'):
                        sim.append(link['href'].replace('/store/apps/details?id=',''))
        return sim
    
    def get_app_ids_for_developer(self, developer_id, country="gb", lang="en") -> list:
        '''
        Find apps by developer. 
        '''

        url = "{}store/apps/details?id={}".format(self.base_url, developer_id)
        url += "&hl={}".format(lang)
        url += "&gl={}".format(country)
        soup = self._parse_url_html(url)
        devs = []
        for link in soup.find_all('a'):
            if link['href'].startswith('/store/apps/dev?id='):
                soup1 = self._parse_url_html(self.base_url + link['href'])
                for link in soup1.find_all('a'):
                    if link['href'].startswith('/store/apps/details'):
                        devs.append(link['href'].replace('/store/apps/details?id=',''))
            if link['href'].startswith('/store/apps/developer?id='):
                soup1 = self._parse_url_html(self.base_url + link['href'])
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
            df.to_csv(os.path.join(os.getcwd(),filename), index=False, encoding="utf-8") 
        except Exception as e:
            print(e)

    def write_gexf (self, incoming_csv, outgoing_gexf):
        """
        Convert CSV into GEXF. Useful for using with Gephi lite. 
        :param incoming_csv - CSV filename
        :param outgoing_gexf - GEXF filename
        """
        df = pd.read_csv(os.path.join(os.getcwd(),"appecology.csv"))
        df.columns = ['source', 'target']
        Graphtype = nx.Graph()
        G = nx.from_pandas_edgelist(df, create_using=Graphtype)
        nx.write_gexf(G, os.path.join(os.getcwd(),"appecology.gexf"))

    def similarity_network(self, startapp, csv_file, country="gb", language="uk"):
        """
        Function to get the Similarity Network
        :param startapp - Package Name of the app to start the search
        :param csv_file - CSV file to create
        :param country - store country name. Defaults to GB. 
        :param language - store language. Defaults to en_GB. 
        """
        fh = open(csv_file,"a")
        similar = self.get_similar_app_ids_for_app(startapp, country = country, lang = language)
        similar_app_details = self.get_multiple_app_details(similar, country=country, lang=language)

        for app in similar_app_details:
            sim_app_id = app["appId"]
            fh.write("{}, {}\n".format(startapp, sim_app_id))
            similar1 = self.get_similar_app_ids_for_app(sim_app_id, country = country, lang = language)
            similar_app_details1 = self.get_multiple_app_details(similar1, country=country, lang=language)
            for app1 in similar_app_details1:
                fh.write("{}, {}\n".format(sim_app_id, app1['appId']))

