import requests, csv
import json, os

class realestate_Scraper:
    def __init__(self,catageory,fileName):
        self.catageory = catageory
        self.fileName = fileName

    def getPageHeaders(self):
        headers = {
            'authority': 'platform.realestate.co.nz',
            'accept': 'application/vnd.api+json',
            'accept-language': 'en-US,en;q=0.9',
            'if-none-match': 'W/"2f093-BlRfVC4uFiutnglLI6nPuH2isH8"',
            'origin': 'https://www.realestate.co.nz',
            'referer': 'https://www.realestate.co.nz/',
            'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57',
        }
    
    def getPageResponse(self,headers,page):
        params = {
            'filter[category][]': f'{self.catageory}',
            'filter[showcaseCount]': 'true',
            'meta[aggs]': 'propertyType,listingCategoryCode,region',
            'page[offset]': f'{page}',
            'page[limit]': '100',
            'page[groupBy]': 'featured',
        }
        response = requests.get('https://platform.realestate.co.nz/search/v1/listings', params=params, headers=headers)
        jsonData = response.json()
        
    def getMetrics(self,listingId,headers):
        url = f'https://platform.realestate.co.nz/search/v1/listings/{listingId}/total-reach'
        listtingViewsResp = requests.get(url, headers=headers)
        jsonViewResp = listtingViewsResp.json()
        totalViews = jsonViewResp.get('attributes', {}).get('total', '-')
        return totalViews
    
    def extract_Data(self,jsonData,totalresults,headers):
        allResults = totalresults
        alldata = jsonData.get('data')
        for index,data in enumerate(alldata,start=1):
            url = data['attributes'].get('website-full-url', '')
            region = data['attributes']['address'].get('region', '')
            city = data['attributes']['address'].get('district', '')
            district = data['attributes']['address'].get('suburb', '')
            address = data['attributes']['address'].get('display-address', '')
            title = data['attributes'].get('header', '')
            propertyType = data['attributes'].get('listing-sub-type', '')
            listing_Number = data['attributes'].get('listing-no', '')
            listingDate = data['attributes'].get('created-date', '').split('T')[0]
            description = data['attributes'].get('description', '')
            price = data['attributes'].get('price-display', '')
            Building_Area = data['attributes'].get('land-area', '')
            Plot_Area = data['attributes'].get('floor-area','')
            getListingId = data.get('id')
            metrics = self.getMetrics(getListingId,headers)
            print(f'[{index} of {allResults}] Getting Property [Title]:- {title}')
            row = [title, url, region, city, district, address, propertyType, price, Plot_Area, Building_Area, listing_Number, listingDate,metrics, description]
            self.saveData(row)

    def header(self):
        header = ['Property Title', 'Property Url', 'Region', 'City','District', 'Address', 'Property Type', 'Price', 'Plot Area', 'Building Area', 'Listing Number', 'Listing Date','Total Views', 'Property Details']
        with open(self.fileName,mode='w',newline='',encoding='UTF-8') as file:
            csv.writer(file).writerow(header)

    def saveData(self,row):
        with open(self.fileName,mode='a',newline='',encoding='UTF-8') as file:
            csv.writer(file).writerow(row)

    def run(self):
        if self.fileName not in os.listdir():
            self.header(self)
        headers = self.getPageHeaders()
        page = 0
        while True:
            jsonData = self.getPageResponse(headers,page)
            totalresults = jsonData
            checkData = jsonData
            if checkData == []: break
            self.extract_Data(jsonData,totalresults,headers)
            page += 100
            
if __name__ == '__main__':
    print(f'\n[INFO] Which is the catageory you want to scrape..(Sale OR Lease)')
    print(f'[INFO] If you want to select Sale then write "s" else "l"...')
    answer = input('enter your decision (s OR l):- ')
    if answer.lower() == 's':
        catageory = 'com_sale'
        fileName = 'Realestate_ForSale.csv'
        scraper = realestate_Scraper(catageory,fileName)
        scraper.run()
    else:
        catageory = 'com_lease'
        fileName = 'Realestate_ForLease.csv'
        scraper = realestate_Scraper(catageory,fileName)
        scraper.run()

