#!/usr/bin/env python
# coding: utf-8

# In[1]:


#First we will import all the required libraries for web-scraping.
#We will require two libraries for web-scraping:
# requests: This will be used to send get request to the web page server to get the source-code of the webpage
#BeautifulSoup: It will be used to parse the source code and to extract the required data from the parsed structure.
get_ipython().system('pip install bs4')
get_ipython().system('pip install requests')
import pandas as pd


# In[2]:


# importing the required libraries
from bs4 import BeautifulSoup
import requests


# 1. Write a python program to display all the header tags from wikipedia.org.

# In[3]:


#send get request to the webpage server to get source code of the page
page = requests.get('https://en.wikipedia.org/wiki/Main_Page')


# In[4]:


page


# In[5]:


#page content
soup = BeautifulSoup(page.content)
soup


# In[6]:


#Scraping headers
headers=[]
for i in soup.find_all('h2',class_="mp-h2"):
    headers.append(i.text)
headers


# 2. Write a python program to display IMDB's Top rated 100 movies' data (i.e. name, rating, year of release) and make data frame.

# In[7]:


source = requests.get('https://www.imdb.com/chart/top/')


# In[8]:


source


# In[9]:


soup = BeautifulSoup(source.text,'html.parser')
print(soup)


# In[10]:


movies = soup.find('tbody',class_='lister-list').find_all('tr')


# In[11]:


print(len(movies))


# In[12]:


for movie in movies:
    name = movie.find('td',class_='titleColumn').a.text
    rank = movie.find('td',class_="titleColumn").get_text(strip=True).split('.')[0]
    year = movie.find('td',class_="titleColumn").span.text.strip('()')
    rating = movie.find('td',class_="ratingColumn imdbRating").strong.text
    print(rank,name,year,rating)    
    

    


# # Q3.Write a python program to display IMDB's Top rated 100 Indian movies data (i.e. name, rating and year of release)

# In[13]:


source1= requests.get("https://www.imdb.com/india/top-rated-indian-movies/")
source1


# In[14]:


soup1 = BeautifulSoup(source1.text,'html.parser')
print(soup1)


# In[15]:


movies1 = soup1.find('tbody',class_='lister-list').find_all('tr')


# In[16]:


print(len(movies1))


# In[17]:


for movie1 in movies1:
    name1 = movie1.find('td',class_='titleColumn').a.text
    rank1 = movie1.find('td',class_="titleColumn").get_text(strip=True).split('.')[0]
    year1 = movie1.find('td',class_="titleColumn").span.text.strip('()')
    rating1 = movie1.find('td',class_="ratingColumn imdbRating").strong.text
    print(rank1,name1,year1,rating1)    
    


# Q4. Write a python program to scrape cricket ranking from icc-cricket.com.
#  a. Top 10 ODI teams in men's cricket along with the records for matches, points and ratings
#  b. Top 10 ODI Batsmen in menalong with the records of their team and rating.
#  c. Top 10 ODI Bowlers along with the records of their team and rating.

# import re

# urls=["https://www.icc-cricket.com/rankings/mens/player-rankings/test/batting",
#      "https://www.icc-cricket.com/rankings/mens/player-rankings/test/bowling",
#      "https://www.icc-cricket.com/rankings/mens/player-rankings/odi/batting",
#      "https://www.icc-cricket.com/rankings/mens/player-rankings/odi/bowling"]

# for url in urls:
#     request_object=requests.get(url)
#     html_content=request_object.text
#     print(request_object.status_code,"->",url)
# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# Q6. Write a python program to scrape details of all the posts from coreyms.com. Scrape the heading, data,content and the code for the video from the link for the youtube video from the post.

# In[18]:


source6 = requests.get('https://coreyms.com')
source6


# In[19]:


soup6 = BeautifulSoup(source6.text,'html.parser')
print(soup6.prettify())


# In[20]:


for article in soup6.find_all('article'):
    headline=article.h2.a.text    
    print(headline)
    summary = article.find('div',class_='entry-content').p.text
    print(summary)
    try:
        
        vid_scr=article.find('iframe',class_='youtube-player')['src']
        vid_id = vid_scr.split('/')[4]
        vid_id = vid_id.split('?')[0]
        yt_link = f'https://youtube.com/watch?v={vid_id}'
    except Exception as e:
        yt_link = None
    print(yt_link)
    
    print()


# Q7. Write a python program to scrape house details from mentioned URL. It should include house title, location, area, EMI and price from nobroker.in.
# 

# In[21]:


from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import itertools
import matplotlib.pyplot as plt


# In[22]:


headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
link = 'https://www.nobroker.in/property/rent/chennai/Chennai/?searchParam=W3sibGF0IjoxMy4wNDM3NjE'


# chennai.to_csv('chennai_rent.csv')

# In[23]:


# dataframe
titles = []
addresses = []
rents = []
sizes = []
deposits = []
furnishings = []
property_ages = []
available_fors = []
immediate_possessions = []



# scraping through 1000 pages of nobroker website of places in Chennai
for page in range(1000):
    page += 1;
    link = "https://www.nobroker.in/property/rent/chennai/Chennai/?searchParam=W3sibGF0IjoxMy4wNDM3NjEyODI5MTkyLCJsb24iOjgwLjIwMDA2ODUxNjk2OTMsInNob3dNYXAiOmZhbHNlLCJwbGFjZUlkIjoiQ2hJSllUTjlULXBsVWpvUk05UmphQXVuWVc0IiwicGxhY2VOYW1lIjoiQ2hlbm5haSIsImNpdHkiOiJjaGVubmFpIn1d&sharedAccomodation=0&orderBy=nbRank,desc&radius=2&traffic=true&travelTime=30&propertyType=rent&pageNo="+str(page)

    response = get(link,headers=headers)

    # for testing if scraping of website is allowed...
    # print(response)
    # print(response.text[:1000])


    # Parsing through html page
    html_soup = BeautifulSoup(response.text,'html.parser')
    house_containers = html_soup.find_all('div', class_="card")
    if(house_containers != []):
        for container in house_containers:
            
            try:
                rent = container.find_all('h3')[2].find('span').text.replace(',','')
                rent = int(''.join(itertools.takewhile(str.isdigit,rent)))
                rents.append(int(rent))
            except:
                rents.append('-')
            try:
                size = int(container.find_all('h3')[0].find_all('span')[0].text.replace(',',''))
                sizes.append(int(size))
            except:
                sizes.append('-')
            try:
                deposit = int(container.find_all('h3')[1].find_all('span')[0].text.replace(',',''))
                deposits.append(int(deposit))
            except:
                deposits.append('-')
            title = (container.find('div','card-header-title').find('h2').text.replace('\n',''))
            address = (container.find('div','card-header-title').find('h5').text.replace('\n',''))
            titles.append(title)
            addresses.append(address)

            furnishing = (container.find('div','detail-summary').find_all('h5')[0].text.replace('\n',''))
            furnishings.append(furnishing)
    
            property_age = (container.find('div','detail-summary').find_all('h5')[1].text.replace('\n',''))
            property_ages.append(property_age)
    
            available_for = (container.find('div','detail-summary').find_all('h5')[2].text.replace('\n',''))
            available_fors.append(available_for)
    
            immediate_possession = (container.find('div','detail-summary').find_all('h5')[3].text.replace('\n',''))
            immediate_possessions.append(immediate_possession)
    else:
        break;

    Nothing
print("Successfully scraped {} pages containing {} properties.")



# In[24]:


# creating dataframe to save data in .csv format
cols = ['Title', 'Address', 'Rent(Rs)', 'Deposit(Rs)', 'Size(Acres)', 'Furnishing', 'Property age', 'Available for', 'Immediate possession']

chennai = pd.DataFrame({'Title': titles,
                        'Address': addresses,
                        'Rent(Rs)': rents,
                        'Deposit(Rs)': deposits,
                        'Size(Acres)': sizes,
                        'Furnishing': furnishings,
                        'Property age': property_ages,
                        'Available for': available_fors,
                        'Immediate possession': immediate_possessions})[cols]
chennai.to_csv('chennai_rent.csv')


# Q8. Write a python program to scrape mentioned details from dineout.co.in
# i)Restaurant name
# ii)Cuisine
# iii)Location
# iv)Ratings
# v)Image URL

# In[25]:


page8 = requests.get('https://www.dineout.co.in/delhi-restaurants/buffet-special')


# In[26]:


page8


# In[27]:


soup8 = BeautifulSoup(page8.content)
soup8


# In[28]:


#Now we have all the tags in which there are the job titles.
#Now we will extract the text from these tags one by one by looping over these tags
titles = [] #empty list for store the
for i in soup8.find_all('div',class_="restnt-info cursor"):
    titles.append(i.text)  
    
titles


# In[29]:


#Scraping multiple locations
location = [] #empty list
for i in soup8.find_all('div',class_="restnt-loc ellipsis"):
    location.append(i.text)
location


# In[30]:


#Scraping multiple prices
price = [] #empty list

for i in soup8.find_all('span',class_="double-line-ellipsis"):
    price.append(i.text.split('|')[0])
price


# In[31]:


#Scraping images url's
images =[]
for i in soup8.find_all("img",class_="no-img"):
    images.append(i['data-src'])
images


# In[32]:


#printing length
print(len(titles),len(location),len(price),len(images))


# In[33]:


#Making dataframe
import pandas as pd
df = pd.DataFrame({'Titles':titles,'Location':location,'Price':price,'Images_url':images})
df


# Q9. Write a python program to scrape weather details for last 24 hours from Tutiempo.net:
# i) Hour
# ii) Temperature
# iii) Wind
# iv) Weather condition
# v) Humidity
# vi) Pressure

# In[34]:


source9 = requests.get("https://en.tutiempo.net/delhi.html?data=last-24-hours")
source9


# In[ ]:


soup9 = BeautifulSoup(source9.text,'html.parser')
print(soup9)


# In[ ]:





# In[ ]:


temp =[]
for i in soup9.find_all("td",class_="t Temp"):
    temp.append(i.text)
temp


# In[ ]:


wind =[]
for i in soup9.find_all("td",class_="wind"):
    wind.append(i.text)
wind


# In[ ]:


humidity =[]
for i in soup9.find_all("td",class_="hr"):
    humidity.append(i.text)
humidity


# In[ ]:


pressure =[]
for i in soup9.find_all("td",class_="prob"):
    pressure.append(i.text)
pressure


# In[ ]:


for time in soup9.find_all('tr'):
    headline = time.find('td')  
        
    print(headline)


# In[ ]:


#Making dataframe
import pandas as pd
df = pd.DataFrame({'Temperature':temp,'wind':wind,'humidity':humidity,'pressure':pressure})
df


# Q10. Write a python program to scrape monument name, monument description, image URL about top 10 monuments from puredestinations.co.uk.

# In[35]:


source10= requests.get("https://www.puredestinations.co.uk/top-10-famous-monuments-to-visit-in-india/")
source10


# In[36]:


soup10 = BeautifulSoup(source10.text,'html.parser')
print(soup10)


# In[37]:



para = soup10.find_all('p')
for para1 in para:
    print(para1.text)
    
    


# In[38]:


#Scraping images url's
ima =[]
for i in soup10.find_all("img"):
    ima.append(i)
ima


# In[ ]:





# In[ ]:




