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