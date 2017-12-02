import requests
import csv
from bs4 import BeautifulSoup
from calendar import monthrange

urlRoot = 'http://58.68.146.102/rmrb/'
urlDate = '20171012/'
urlPage = '1'

fromYear = int(input('Scrap from which year?(1946 - 2017): '))
fromMonth = int(input('Scrap from which month?(01 - 12 two digits): '))

toYear = int(input('Scrap to which year?(1946 - 2017): '))
toMonth = int(input('Scrap to which month?(01 - 12 two digits): '))

#create the file and store the data 
output_path = str(fromYear) + "-" + str(fromMonth) + "to" + str(toYear) + "-" + str(toMonth) + ".csv"
output = open(output_path, 'w')
writer = csv.writer(output)
writer.writerow(["Date", "Day", "Number of pages", "Pages scraped","Number of articles","Section", "Titles by page", "Number of titles scraped on this page"])

# for loop
for year in range(fromYear, toYear + 1, 1): 
    for month in range(fromMonth, toMonth + 1, 1):
        for day in range(1, monthrange(year, month)[1] + 1, 1):
            #
            #for page in range(1, pageNum + 1):
            #formatting the date url string
            urlDate = str(year) + str(month).zfill(2) + str(day).zfill(2) + '/'
            date  = str(year) + '/' + str(month).zfill(2) + '/'+ str(day).zfill(2)
            print(date)

            response = requests.get(urlRoot + urlDate + '1')
            html = response.content

            soup = BeautifulSoup(html, "lxml")
            soup.prettify()

            #the find results are list objects

            #extract date info number info
            day = soup.select("#UseWeek")
            day = day[0].string
            pageNum = soup.select("#UseRmrbPageNum")
            pageNum = int(pageNum[0].string)
            articleNum = soup.select("#UseRmrbNum")
            articleNum = int(articleNum[0].string)
            #extract date info

            for page in range(1, pageNum + 1, 1):
                urlPage = str(page)
                response = requests.get(urlRoot + urlDate + urlPage)
                html = response.content
                soup = BeautifulSoup(html, "lxml")
                title = []
                
                #extract the page info
                pageInfo = soup.find_all("div", class_="info")
                pageInfo = pageInfo[0].find_all('span')
                currentPage = int(pageInfo[0].string)
                pageName = pageInfo[1].string
                pageArtNum = int(pageInfo[2].string)
                #extract the page info
                row = [date, day, pageNum, currentPage, articleNum, pageName]
                #scrap title
                titleList = soup.find_all('h3')
                for titleNum in range(0, pageArtNum):
                    title.append(titleList[titleNum].find('a').string)
                row.append(title)
                secArtNum = len(title)
                row.append(str(secArtNum))
                writer.writerow(row)
                #scrap title
            
            print("Current url: " + urlRoot + urlDate + urlPage)
            print("Day: " + day)
            print("Page Number: " + str(pageNum))
            print("Total article number of the day: "+ str(articleNum))
            print("Current page number: " + str(currentPage))
            print("Current page: " + pageName)
            print("Current page article number: " + str(pageArtNum))

output.close()
