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

table = root.xpath('.//*[@class="statistics"]')[0]  
for row in table.xpath(".//tr")[1:]:
	currentLink = row.xpath(".//th/a/@href")[0]

	for currency in row.xpath("//td/text()"):
		if currency.find('\r') == -1:
			currencyName = currency
	
	#print "currentLink: " +  currentLink
	for name in row.xpath(".//th/a/text()"):
		if name.find('\r') == -1:
			currentName = name

	links.append(currentLink)
	countryNames.append(currentName)
	currencies.append(currencyName)
	#print " current Name: " + currentName
	#print currentName
	#print [cell for cell in row.xpath(".//th/a/@href")]
#print "links: " 
#print links
i = 0
for i in range(0, len(links)):
	response2 = requests.get(url + links[i])
	print "currentLink (second loop) : " + (url + links[i])
	root2 = fromstring(response2.content) 
	table2 = root2.xpath('.//*[@class="statistics"]')[0]  
	for eachRow in table2.xpath(".//tr")[1:]:
    
	    currentDate = eachRow.xpath(".//th/text()")[0]
	    currentRate = (eachRow.xpath(".//td/text()")[0].strip())
	    #currentRate.replace(" ", "")
	    #print " currentDate: " + currentDate
	    #print "currentRate: " + currentRate
	    dates.append(currentDate)
	    rates.append(currentRate)
	tableData = []
	tableData.append(dates)
	tableData.append(rates)
	exchangeInfo[countryNames[i]] = tableData
	print "type of: " + str(type(rates[0]))
	dates = []
	rates = []


# print "countryNames: " 
# print countryNames

# print "rates: "
# print rates

# print "dates: "
# print dates
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
# json=json.dumps(exchangeInfo)
# print json	


with open('data.json', 'w') as outfile:
    json.dump(countries, outfile,indent=4, sort_keys=True)
    
