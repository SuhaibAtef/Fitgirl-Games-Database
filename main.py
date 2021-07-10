from logging import error
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.errorhandler import ErrorCode
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from game import game
import re 
import time 
from openpyxl import Workbook, workbook

Games = []
ganras = set() 
errors_occoured = [] 
compan = set()

# fitgirl site:https://fitgirl-repacks.site/all-my-repacks-a-z
link = "https://fitgirl-repacks.site/all-my-repacks-a-z"
driver = webdriver.Chrome()
driver.get(link)


wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.ID, 'smart_push_smio_not_allow')))
ignorebutton = driver.find_element_by_id('smart_push_smio_not_allow')
ignorebutton.click()

fP = driver.find_element_by_class_name('lcp_currentpage')
firstPage = int(fP.text)
print("First Page Number is :" + str(firstPage))
ahreftypes = driver.find_elements_by_xpath(".//article//div//ul[2]/li[.]")
lastPage = int(ahreftypes[len(ahreftypes)-2].text) 
print("Last Page Number is :" + str(lastPage))
for n in range(1,(lastPage+1)):
    url = "https://fitgirl-repacks.site/all-my-repacks-a-z/?lcp_page0=" + str(n)
    webpages = driver.get(url)
    gameslist = driver.find_elements_by_xpath(".//article//div//ul[1]//li[.]")
    for j in range(len(gameslist)):  
        try:
            webpages = driver.get(url)
            gameslist = driver.find_elements_by_xpath(".//article//div//ul[1]//li[.]")
            link = gameslist[j].find_element_by_xpath(".//a[1]")
            link = link.get_attribute("href")
            gamePage = driver.get(link)
            time.sleep(1)
            companies = []
            languages = []
            genres = []
            originalSize = ""
            repackSize = ""
            elemen = driver.find_element_by_xpath(".//article//div//p[1]")
            desc = elemen.get_attribute("innerHTML")
            attribs = re.findall('(.*)<strong>(.*)</strong>',desc)
            Gname = driver.find_element_by_xpath(".//article//header//h1[1]")
            for item in attribs:
                if item[0].find("Ori")!=-1:
                    originalSize=item[1]
                elif item[0].find("Re")!=-1:
                    repackSize=item[1]
                elif item[0].find("Tags")!=-1:
                    genres = genres + item[1].split(", ")
                elif item[0].find("Companie")!=-1:
                    companies = companies + re.split(', |/', item[1])
                elif item[0].find("Languages")!=-1:
                    languages = languages + item[1].split("/")
            name = Gname.text
            print(name+" : " + originalSize +" / "+ repackSize)
            game1 = game(name,link,originalSize,repackSize,companies,genres,languages)
            ganras.update(genres)
            compan.update(companies)
            Games.append(game1)
            web = driver.back()
            gameslist = driver.find_elements_by_xpath(".//article//div//ul[1]//li[.]")
            break;
        except Exception as e: 
            print(e)
            j-=1
            errors_occoured.append(name)         
    break;

workbook = Workbook()
sheet = workbook.active

listGanras = list(ganras)
listCompan = list(compan)
for g in range(0,len(Games)):
    sheet['A'+str(g+1)] = g+1
    sheet['B'+str(g+1)] = Games[g].getName()
    sheet['C'+str(g+1)] = Games[g].getURL()
    sheet['D'+str(g+1)] = Games[g].getOri()
    sheet['E'+str(g+1)] = Games[g].getRe()
    sheet['F'+str(g+1)] = ' '.join(map(str, Games[g].getlang()))
    sheet['G'+str(g+1)] = ' '.join(map(str, Games[g].getgenra()))
    sheet['H'+str(g+1)] = ' '.join(map(str, Games[g].getComp()))

for e in range(len(errors_occoured)):
    sheet['I'+str(e+1)] = e+1
    sheet['J'+str(e+1)] = errors_occoured[e]

for s in range(len(listGanras)):
    sheet['K'+str(s+1)] = s+1
    sheet['L'+str(s+1)] = listGanras[s]

for c in range(len(listCompan)):
    sheet['M'+str(c+1)] = listCompan[c]

workbook.save(filename="GamesList.xlsx")