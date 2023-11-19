from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time,csv

class ZmeenPk():
    def __init__(self) -> None:
        pass

    def header(self):
        header = ['House Title','Url','Image','Area','Location','Bed Rooms','Purpose','Creation Date','Price','Property Description']
        with open(file="zmeenPk.csv",mode='w',newline='') as file:
            csv.writer(file).writerow(header)

    def openBrowser(self):
        driverpath = EdgeChromiumDriverManager().install()
        servc = Service(driverpath)
        driver = webdriver.Edge(service=servc)

    def getAndSaveLink(self,driver,weburl):
        driver.get(weburl)
        time.sleep(4)
        urlTag = driver.find_elements(By.XPATH,'//ul//a')
        for tag in urlTag:
            productLinks = tag.get_attribute('href')
            with open(file='productLinks.txt',mode='a') as file:
                file.write(productLinks + '\n')

    def readAndgetLinks(self):
        with open(file='productLinks.txt',mode='r') as file:
            readData = file.readlines()
            productUrls = [link.strip() for link in readData]
            return productUrls

    def parseData(self,driver,productUrls):
        for url in productUrls:
            driver.get(url)
            time.sleep(4)
            try: title = driver.find_element(By.XPATH,'//div/h1').text.strip()
            except: title = 'None'
            try: image = driver.find_element(By.XPATH,'//picture/img[@aria-label="Cover Photo"]').get_attribute('src')
            except: image = 'None'
            try: price = driver.find_element(By.XPATH,'//div[text() = "PKR"]').get_attribute("textContent")
            except: price = 'None'
            try: area = driver.find_element(By.XPATH,'//li/span[@aria-label="Area"]/span').text.strip()
            except: area = 'None'
            try: location = driver.find_element(By.XPATH,'//li/span[@aria-label="Location"]').text.strip()
            except: location = 'None'
            try: bedrooms = driver.find_element(By.XPATH,'//li/span[@aria-label="Beds"]').text.strip()
            except: bedrooms = 'None'
            try: purpose = driver.find_element(By.XPATH,'//li/span[@aria-label="Purpose"]').text.strip()
            except: purpose = "None"
            try: creationDate = driver.find_element(By.XPATH,'//li/span[@aria-label="Creation date"]').text.strip()
            except: creationDate = 'None'
            try: propertyDescription = driver.find_element(By.XPATH,'//div[@aria-label="Property description"]//span').get_attribute('textContent')
            except: propertyDescription = 'None'
            row = [title,url,image,area,location,bedrooms,purpose,creationDate,price,propertyDescription]
            print(f"[Info] Getting House:- {title}")
            self.checkandSave(row)
    
    def checkandSave(self, row):
        with open(file="zmeenPk.csv", mode='r', encoding='UTF-8') as f:
            check_data = csv.reader(f)
            if row not in check_data:
                with open(file="zmeenPk.csv", mode='a', encoding='UTF-8', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow(row)

    def run(self):
        driver = self.openBrowser()
        startPage = int(input('Enter your page where you want to start:- '))
        endPage = int(input('Enter your page where you want to end:- ')) + 1
        for page in range(startPage,endPage):
            webUrl = f"https://www.zameen.com/Houses_Property/Lahore-1-{page}.html"
            print(f"\n[Info] Getting data from Url:- {webUrl}\n")
            self.getAndSaveLink(driver,webUrl)
            productLinks = self.readAndgetLinks()
            self.parseData(driver,productLinks)

open(file='productLinks.txt',mode='w').close()
myClass = ZmeenPk()
print(f"[Info] Do you want to delete all data and add new data! ")
answer = input('enter your decision (y/n):- ')
if answer == 'y':
    myClass.header()
    myClass.run()
else:
    myClass.run()