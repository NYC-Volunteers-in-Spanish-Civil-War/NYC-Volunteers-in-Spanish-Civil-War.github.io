import codecs
import urllib2
import time
from bs4 import BeautifulSoup

#GLOBALS
NY_FLAGS = set(["nyc", "new york", "manhattan", "brooklyn", "staten island", "queens", "bronx"])
EXECUTION_TIME = 0
START_TIME = time.time()
TOTAL_TIME = 0

# Open a file to write the information to
f = codecs.open("data.txt", "w", encoding="utf-8")

current_range = 0 #Which range (from current_range to current_range + 20) of volunteers are shown on this page
while current_range < 2660:
    #Keep track of the progress of the script
    percentage_complete = round((current_range + 1.0) / 2677, 3)
    start_time = time.time()
    temp = TOTAL_TIME
    TOTAL_TIME *= (1 / (percentage_complete+ .001))
    TOTAL_TIME -= temp
    #EXECUTION_TIME -= START_TIME
    hours = TOTAL_TIME // 3600
    minutes = TOTAL_TIME // 60 - 3600*hours
    seconds = TOTAL_TIME - 60*minutes
    
    print "Now looping over volunteers {}-{}".format(current_range + 1, current_range + 20).ljust(40), "Total Percentage Complete : {}%".format(percentage_complete).ljust(35), "Estimated time remaining: {}:{}:{}".format(int(hours), int(minutes), int(seconds))
    #Get the url for the range
    url = "http://www.alba-valb.org/volunteers/browse/?b_start:int=" + str(current_range) + "&-C="
    #Pull the webpages data and parse it
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, features="lxml")
    #Get the volunteer items and loop through them
    table = soup.find("table", {"class": "bio-table"})
    for tr in table.findChildren("tr", recursive=False)[1 if current_range == 0 else 0:-1]: #First page has an additional broken volunteer at the beginning. Ignore it.
        #Get the link to the volunteer's full biography
        a = tr.find("table").find("a")
        #Fetch and parse the volunteer webpage
        volunteer_page = urllib2.urlopen(a["href"]).read()
        volunteer_soup = BeautifulSoup(volunteer_page, features = "lxml")
        #Fetch and clean up the biography data of the volunteer, getting rid of unnecesary data. 
        biography = volunteer_soup.find("div", {"class":"comment_box"})
        if not biography: #For some reason, some biography pages don't have the same format as the rest of them
            biography = volunteer_soup.find(id="parent-fieldname-body")
        biography = biography.findAll("p")
        #There are multiple paragraphs in the biography with varying information. The largest one tends to be the main one, so sort them by size and get the last one in the list
        biography = sorted([p for p in biography if not (p.has_attr("class"))], key = lambda k:len(k.getText())) 
        biography = biography[-1].getText() if len(biography) > 0 else "" #Some biographies don't exist, so filler data needs to be used
        #If the volunteer was indeed a New Yorker, print their data
        matches = [flag for flag in NY_FLAGS if flag in biography.lower()]
        if "nyc" in matches or len(matches) >= 2: #gets rid of NY state matches, as well as accidental ship name matches(Ex: the ship "manhattan")
            f.write(a.getText().ljust(30) +  " ----      " + a["href"] + "\n")
            f.write(biography +  "\n");
            f.write("----------------------------------------------------------------------------------------------------------------------------------\n")
    EXECUTION_TIME = time.time()-start_time
    TOTAL_TIME = time.time() - START_TIME
    current_range += 20
