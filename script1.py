from bs4 import BeautifulSoup
#from urllib2 import urlopen
#from pyvirtualdisplay import Display
import csv
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.common.action_chains import ActionChains
import csv
import MySQLdb
#display = Display(visible=0, size=(1024, 768))
#display.start()

url = "http://www.gigstart.com"
relativeUrl = raw_input(" enter the link ")
if relativeUrl and len(relativeUrl) > 0:
    url = url + "/" + relativeUrl
print url
driver = webdriver.PhantomJS()
driver.set_window_size(1024, 768)driver.get(url)
while True:
    try:
        link = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "more")))
	#ActionChains(driver).move_to_element(link).perform()
        link.click()
        time.sleep(4) 
    except TimeoutException:
        break
#url = urlopen("http://www.gigstart.com/singer")
readHtml = driver.page_source
soup = BeautifulSoup(readHtml, 'lxml')

titles1 = []
cities = []
types = []
users = []
links = []
links2 = []
url1 = "http://www.gigstart.com"

Results = soup.find("div", { "class" : "row" })
for row in Results.find_all('li'):
    title=row.find_all('div', {"class" : "row card-info text-center"})
      
    for titletp in title:
	    titles1.append(titletp.a.string.encode("utf-8"))
    for titlec in title:
		cities.append(titlec.p.text.encode("utf-8"))
    for titles in title:
		types.append(titles.small.string.encode("utf-8"))
    for titletu in title:
        users.append(titletu.h4.a['href'].rsplit('/',1)[1])  
    for titletl in title:
        links.append(titletu.h4.a['href'])

for l in links:
	l = url1 + l
	links2.append(l)

with open('tests4.csv','wb') as file:
		
    writer=csv.writer(file)
    rows = zip(users,titles1,cities,types,links2)
    for row in rows:
        writer.writerow(row)
driver.quit() 
display.stop()

con = MySQLdb.connect("localhost","root","root","test1", charset='utf8', use_unicode=True )
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS alldata (username VARCHAR(35) PRIMARY KEY, name VARCHAR(35), city VARCHAR(35), type VARCHAR(35), link VARCHAR(55));")

with open('tests4.csv','rb') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr1 = csv.reader(fin, delimiter=',') # comma is default delimiter
    for row in dr1:
            #to_db1 = [unicode(row[0], "utf8"), unicode(row[1], "utf8"), unicode(row[2], "utf8"), unicode(row[3], "utf8"), unicode(row[4], "utf8")] # Appends data from CSV file representing and handling of VARCHAR(35)
            cur.execute('INSERT IGNORE INTO alldata (username , name, city, type, link)' 'VALUES(%s, %s, %s, %s, %s)' , row)
            
            con.commit()

