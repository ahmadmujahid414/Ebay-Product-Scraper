from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import os ,sys

s = HTMLSession()

def get_product_link(url):
	try:
		r = s.get(url)
		soup = BeautifulSoup(r.content,'lxml')
		product_list = soup.find_all('div', class_='s-item__wrapper clearfix')
	
		productlinks = []
	except:
		print("Wrong Link Provide")

	for item in product_list:
		for link in item.find_all('a', href=True):
			productlinks.append(link['href'])
	return productlinks

def get_product_details(p_url):
    data = {}
    r = s.get(p_url)
    soup = BeautifulSoup(r.content,'lxml')
    try:
        try:
            name = soup.find('h1',class_='x-item-title__mainTitle').text.encode("utf-8")
        except:
            name = soup.find('h1',class_='product-title').text.encode("utf-8")
    except:
        try:
            name = soup.find('h1',class_='it-ttl').text.encode("utf-8")
        except:
            name = "NaN"

    link = p_url
    try:
        try:
            status = soup.find_all('div',class_='d-quantity__availability')[0].text
        except:
            status = soup.find_all('div',class_='u-flL condText  ')[0].text
    except:
        status = 'NaN'
    try:
        try:
            price = soup.find('div',class_='x-price-primary').text
        except:
            price = soup.find('div',class_='u-flL w29 vi-price').text
    except:
        try:
            price = soup.find('div',class_='display-price').text
        except:
            price = "NaN"
        
    data['name'] = name
    data['price'] = price
    data['status'] = status
    data['link'] = link
	
    return data

def save_data(data):
	print("Please Enter a name for a csv file in which the data will be stored")
	filename = input('filename: ')
	
	df = pd.DataFrame(data)
	if not(df.to_csv(filename+'.csv')):
		print('-----------------------------------------')
		print("Process Completed")
	else:
		print('-----------------------------------------')
		print('Process Incomplete')

def scrape_link(url):
	link = list(dict.fromkeys(get_product_link(url)))
	data = []
	print('-----------------------------------------')
	print('Scrapping in Process')
	count=1
	for i in link:
		print("scraped page "+str(count)+"/"+str(len(links)))
		data.append(get_product_details(i))
		count=count+1
	save_data(data)


def Scrap_file(filename):
	if filename.lower() in ["x", "exit"]:
		sys.exit()

	scrap_data = [] 
	
	if os.path.isfile(filename):
		print("File found . Scraping data ......")

		with open(filename , "r") as f:
			links = f.read().splitlines()
			count=1
			for l in links:
				try:
					print("scraped page "+str(count)+"/"+str(len(links)))
					scrap_data.append(get_product_details(l))
					count=count+1
				except:
					continue
	else:
		print(f"File {filename} not found")

	save_data(scrap_data)
	


if __name__ == '__main__':
	print("Welcome To Ebay Scrapper")
	print("-------------------------------------")
	print("If you want to search by link which contain Multiple product")
	print("press 0")
	print("if you want to search by a file which cotain multiple product link")
	print("press 1")
	print("-----------------------------------------------------")
	press = int(input("Enter: "))
	print("---------------------------------------")
	
	if press == 1:
		print("""
    			Enter file name  with  links
				enter 'x' or 'exit'  to close program 
				""")
				
		filename = input("> ")
		Scrap_file(filename)
	elif press == 0:
		print("Hello Please Provide an Ebay Link")
		print('Which Contain Multiple Product List')
		print("--------------------------------------")
		url = input('Ebay Link: ')
		scrape_link(url)
	else:
		print("Try Later!")
	
	

