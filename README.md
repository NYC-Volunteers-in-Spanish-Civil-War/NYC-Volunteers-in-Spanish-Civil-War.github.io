# Stuyvesant's Spanish Civil War Archives

## Overview
This repository contains the code for all aspects of Stuyvesant's Spanish Civil War Archives. Included is the code for the original webscraper, the website, the biographies of the volunteers, and the backend interface for seamlessly updating it.

## Original Web Scraping Code
The repository includes the original webscraping code that allowed us to find the New Yorkers who volunteered in the Spanish Civil War. It pulls and compiles the data from http://www.alba-valb.org/

Contained within the folder `scraping`:
  - `data.txt`: Contains all the volunteers from NYC and their data.
  - `names.txt`: Contains just the names of the volunteers.
  - `stuy_volunteers.txt`: Contains the names of volunteers that may have gone to Stuyvesant High School.
  - `scraper.py`: A script that pulled the data from http://www.alba-valb.org/ and analyzed it, writing the volunteers from NYC to `data.txt`.
  - `stuy_finder.py`: Finds the volunteers that may have gone to Stuyvesant High School. Depends on a file `stuy_graduates.csv` that I can't release.

## The Website
Fairly straightforward. Can be visited here: https://scwnyc.stuy.edu/. The archive page contains all the information for the volunteers.

## The Backend Interface
For all intents and purposes a fancy GUI wrapper for git in this very specific case.

### How to use

Requires: Python2.7 (Will eventually be ported to Python3)

1) Clone the repository to your computer.
2) Navigate to the directory and execute the command './run.sh'.
3) Open http://127.0.0.1:8000 in your web-browser of choice.
4) Make any changes you like.
5) Click the button marked "Upload Changes".
6) Select which changes you would like uploaded in the popup checklist.
7) Enter your github username and password and then click "Save Changes".
8) Assuming you have access to this repository, your changes will be live in just a few minutes!

### Screenshots
[![image.png](https://i.postimg.cc/7hc5Y70n/image.png)](https://postimg.cc/Lgt9xJyJ)

[![image.png](https://i.postimg.cc/Gm4YGYbL/image.png)](https://postimg.cc/BjGXGj8k)

## Devlog
Contains all the development history for the website, giving a day by day look into the repo's history.
Viewable [Here](DEVLOG.md).

## Contact
Questions or concerns? Problems in the site? Just like what you see? https://theadorabledev.github.io/contact.html.
