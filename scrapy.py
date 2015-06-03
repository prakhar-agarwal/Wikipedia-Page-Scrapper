import requests
from bs4 import BeautifulSoup as bs
import urllib
import re
import sys
import os
import threading
import Queue
import random
reload(sys)
sys.setdefaultencoding('UTF-8')

queue = Queue.Queue()

def fetch(url):
	response = requests.get(url)
	soup = bs(response.text)
	title=soup.title.contents[0].encode('ascii','ignore')
	print "--------------Creating Directory--------------"
	location="ScrapedData"+"/"+title
	img_location=location+"/"+"images"
	try:
		os.stat(location)
	except:
		os.makedirs(location)
	os.makedirs(img_location)
	print "All data stored at " + location
	f = open(location+"/"+"content", 'w')
	f.write ('\t\t\t%s' %(title) + "\n\n")
	#f.write
	element = soup.find("div", class_ = "mw-content-ltr")
	allelements = element.children
	pattern = r'\A<p>'
	print "------------- Downloading Page Content -------------------"
	for element in allelements:
		matchObj = re.match(r'\A<p>', str(element))
		if matchObj:
			element=re.sub("[\(\[].*?[\)\]]", "", element.text)
			#print element
			#print
			f.write(element+"\n\n")
			#f.write
		matchObj = re.match(r'\A<h', str(element))
		if matchObj:
			element=re.sub("[\(\[].*?[\)\]]", "", element.text)
			#print element
			#print
			f.write(element+"\n\n")
			#DOwnloading all images from the page
	img_links = soup.findAll("a", {"class":"image"})
	x=1
	print "------------- Downloading Images -------------------"
	for img_link in img_links:
		image_url="http:"+unicode(img_link.img['src'],"utf-8")
		print "	Downloading Image "+ image_url + " as " + str(x)+".JPG"
		urllib.urlretrieve(image_url,img_location+"/"+str(x)+".JPG")
		x=x+1
	queue.get()


def main(url):
	response = requests.get(url)
	soup = bs(response.text)
	title=soup.title.contents[0].encode('ascii','ignore')
	element = soup.find("div", class_ = "mw-content-ltr")
	threading.Thread(target=fetch,args=(url,)).start()
	random_links=element.findAll("a")
	numberOfLinks=len(random_links)
	count=1
	while True:
		if (count<11):
			fetchedLink=str(random_links[random.randint(0,numberOfLinks)])
			if "/wiki/" in fetchedLink:
				s=bs(fetchedLink)
				for a in s('a',href=True):
					keyword=a['href']
				fetchedUrl="http://en.wikipedia.org" + keyword
				# url passed to the new thread
				threading.Thread(target=fetch,args=(fetchedUrl,)).start()
				queue.put("Queue_count") #ihbibi
				count=count+1
		else:
			break
	
if __name__ == '__main__':
	print "Enter URL"
	url=raw_input()
	#url = "http://en.wikipedia.org/wiki/Haitian_Revolution"
	main(url)
	while True :
		if queue.empty() :
			break
