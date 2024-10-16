## Play Scraper (CIM edition)

A light weight web scraper for the Google Play store.

## Installation

The code can be installed as a package through pip:
```
pip install -U git+https://github.com/iaine/google-play-scraper-cim.git
```
Alternatively, it can be cloned from Github. 

## Usage

#### Search 
The library can search the store for apps:
```
results = scraper.get_app_ids_for_query(term, country=country, 
            lang=language, num=num_apps_collected)
```      

#### Similar

Using an application as a seed, similar apps may be discovered.
```
similar = scraper.get_similar_app_ids_for_app(app_id, country = country, lang = language)
```

#### Developer
Using an application as a seed, similar apps may be discovered.
```
developer = scraper.get_app_ids_for_developer(developer_id, country=country, lang=language)
```

Each function gets app ids and the details for the apps can be got by using:
```
scraper.get_multiple_app_details(application_ids, country=country, lang=language)
```
A helper function to convert the data is provided:
```
scraper.convert_json_csv(filename, developer_app_details)
```

## Issues 

Please raise issues, features, and bugs on the Github queue. Contributions will be acknowledged in a contributors files. 

Not sure where to start? Documentation and tests are helpful, especially if they include internationalisation. 
