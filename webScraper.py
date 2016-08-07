import requests
from lxml.html import fromstring
import json	

url = "https://www.federalreserve.gov/releases/h10/hist/"
response = requests.get(url)
root = fromstring(response.content)

links = []
dates = []
countryNames = []
currencies = []
rates = []
exchangeInfo = {}
countries = {}

#Get Country names and links from the initial page
table = root.xpath('.//*[@class="statistics"]')[0]  
for row in table.xpath(".//tr")[1:]:
	currentLink = row.xpath(".//th/a/@href")[0]

	for currency in row.xpath("//td/text()"):
		if currency.find('\r') == -1:
			currencyName = currency
	
	
	for name in row.xpath(".//th/a/text()"):
		if name.find('\r') == -1:
			currentName = name

	links.append(currentLink)
	countryNames.append(currentName)
	currencies.append(currencyName)

#Get remaining dates and exchange rates for each of the countries
i = 0
for i in range(0, len(links)):
	response2 = requests.get(url + links[i])
	print "currentLink: " + (url + links[i])
	root2 = fromstring(response2.content) 
	table2 = root2.xpath('.//*[@class="statistics"]')[0]  
	for eachRow in table2.xpath(".//tr")[1:]:
	    currentDate = eachRow.xpath(".//th/text()")[0]
	    currentRate = (eachRow.xpath(".//td/text()")[0].strip())
	    dates.append(currentDate)
	    rates.append(currentRate)
	tableData = []
	tableData.append(dates)
	tableData.append(rates)
	exchangeInfo[countryNames[i]] = tableData
	
	dates = []
	rates = []



print "length of names: " + str(len(countryNames))

i = 0
while i < len(countryNames):
	countries[countryNames[i]] = {
			'link' : links[i],
			'currencyName' : currencies[i],
			'Date' : exchangeInfo[countryNames[i]][0],
			'Rates' : exchangeInfo[countryNames[i]][1]
	}
	i+=1

print "countryNames: "
print countryNames
print "dates: "
print dates



with open('data.json', 'w') as outfile:
    json.dump(countries, outfile,indent=4, sort_keys=True)
    
