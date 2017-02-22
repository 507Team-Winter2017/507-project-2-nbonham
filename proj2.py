#proj2.py
from bs4 import BeautifulSoup
import re

from urllib.request import urlopen
import urllib.request, urllib.parse, urllib.error
import ssl
# And then I use urllib.request.Xxx to reference methods (like urlopen) and objects (like Request) within the urllib.request library.

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

################################################################################################################
#### Problem 1 ####
print('\n*********** PROBLEM 1 ***********')
print('New York Times -- First 10 Story Headings\n')

### Your Problem 1 solution goes here
count = 1

url = 'https://www.nytimes.com/'
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

# example: <h2 class="story-heading"><a href="https://www.nytimes.com/interactive/2017/02/08/world/americas/before-the-wall-life-along-the-us-mexico-border.html">Before the Wall: <br>Life Along the U.S.-Mexico Border</a></h2>
tags = soup.select(".story-heading")
for tag in tags:
    #print(str(count) + " " + tag.get_text().strip())
    print(tag.get_text().strip())
    count += 1
    if count == 11 :
        break
    else :
        continue


################################################################################################################
#### Problem 2 ####
print('\n*********** PROBLEM 2 ***********')
print('Michigan Daily -- MOST READ\n')

### Your Problem 2 solution goes here
#count = 1

url = 'https://www.michigandaily.com/'
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

# example: <div class="view view-most-read view-id-most_read view-display-id-panel_pane_1 view-dom-id-99658157999dd0ac5aa62c2b284dd266">  <div class="item-list"><ol><li class="first"><a href="/section/crime/racist-emails-sent-university-engineering-computer-science-students">Racist and anti-Semitic emails sent to University engineering, computer science students</a></li>
# <div class="panel-pane pane-mostread">
data = soup.findAll('div',attrs={'class':'view-id-most_read'})
for div in data:
    links = div.findAll('a')
    for a in links:
        #print(str(count) + " " + a.get_text().strip())
        print(a.get_text().strip())
        #count += 1


################################################################################################################
#### Problem 3 ####
print('\n*********** PROBLEM 3 ***********')
print("Mark's page -- Alt tags\n")

### Your Problem 3 solution goes here
url = 'http://newmantaylor.com/gallery.html'
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

#print(soup)
imgs = soup.findAll('img')

for i in imgs :
    print(i.get('alt'))

#for img in div.find_all('img', alt=True):
#        print(img['alt'])

################################################################################################################
#### Problem 4 ####
print('\n*********** PROBLEM 4 ***********')
print("UMSI faculty directory emails\n")

### Your Problem 4 solution goes here
contactURLs = []
emails = []
count = 1
pagenation = 1
umichURL = 'https://www.si.umich.edu'

url = 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4'
req = urllib.request.Request(url, None, {'User-Agent': 'SI_CLASS'})
html = urlopen(req, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

## get all the contact details urls on one page in a list
#<div class="field-item even"><a href="/node/9915">Contact Details</a>
#<a href="/node/9915">Contact Details</a>

def getSlugs(s) :
    contactSlugs = soup.findAll(href=re.compile('node'),class_="")

    for slug in contactSlugs :
        contactURLs.append(umichURL + slug.get('href'))

getSlugs(soup)

## get all the contact details for all 6 pages in the same list (can hard code, but will need to actually do the crawling)
#https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4&page=4

while pagenation < 6:

    url = 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4&page=' + str(pagenation)
    pagenation += 1
    #html = urlopen(url, context=ctx).read()
    req = urllib.request.Request(url, None, {'User-Agent': 'SI_CLASS'})
    html = urlopen(req, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    getSlugs(soup)

## iterate through the list and open each url in a for loop
## extract the email out of the approriate location and store that in a list
for contact in contactURLs :
    url = contact
    #html = urlopen(url, context=ctx).read()
    req = urllib.request.Request(url, None, {'User-Agent': 'SI_CLASS'})
    html = urlopen(req, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    #<a href="mailto:shevonad@umich.edu">shevonad@umich.edu</a>
    facultyEmail = soup.findAll(href=re.compile('mailto'))

    for e in facultyEmail :
        emails.append(e.get_text())

    #print((facultyEmail))
    #emails.append(facultyEmail.get_text())

## print out the list of emails with a number before the email like 1 ackerm@umich.edu
for email in emails :
    print (str(count) + " " + email)
    count += 1
