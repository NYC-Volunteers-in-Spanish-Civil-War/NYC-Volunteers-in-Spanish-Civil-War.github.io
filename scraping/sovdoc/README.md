# Sovdoc and Interbrigades Scraper

## About

Collates publicly available information from sovdoc.rusarchives.ru and interbrigades.inforost.org and parses/translates them

## Usage

```
export GOOGLE_APPLICATION_CREDENTIALS="<google translate api JSON verification file>"
python3 -m sovdoc_scraper.py -o sovdoc_data.json
python3 -m interbrigades_scraper.py -o interbrigades_data.json
python3 process_scraped_data.py

```
