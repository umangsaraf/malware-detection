from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json
import time
import os
import urllib.request
import io
import gzip
import config
import numpy as np
import warnings
from tqdm import tqdm



def get_all_links():
    """
    Gets all the gz files url links from the sitemap of ApkPure
    Return: A list with all the gz url links
    """
    url = ('https://apkpure.com/sitemap.xml') # URL to the sitemap
    response = requests.get(url)    
    urlText = response.text #Grabs the content of the request object
    soup = BeautifulSoup(urlText, 'lxml') # Creates the HTML to soup object
    gz_list = []   # List to store all gz file url's
    for link in soup.find_all('a', href=True):
        gz_list.append(link['href']) #Gets the href tag
    gz_list = [i.text for i in soup.find_all('loc')]  #Grabs the link from the href tag
    return gz_list


def get_xml(url):
    """
    Takes the url for the gz file and writes it as an xml file 
    url: The Url file name 
    Returns: The name of the downloaded linked file
    """
    response = requests.get(url)
    compressed_file = io.BytesIO(response.content)
    decompressed_file = gzip.GzipFile(fileobj=compressed_file)
    OUTFILE_PATH = '.'.join(url.split('/')[-1].split('.')[:-1])
    with open(OUTFILE_PATH, 'wb') as outfile:
        outfile.write(decompressed_file.read())
    return OUTFILE_PATH

def get_links_from_xml(xml):
    """
    Extracts all the links from the XML file
    xml: Name of xml file 
    Returns: A list with all Url's from the XML file
    """
    file = open(xml, 'r') #Creates a handle to open xml file
    cont= file.read()  #reads the content of the file 
    command = 'rm ' + xml
    os.system(command)
    soup = BeautifulSoup(cont, 'lxml') #creates a soup object of the xml file
    links = soup.find_all('loc') # grabs all the links in the xml file 
    return [link.text for link in links]



def create_apk(url, outpath):
    #creates a response object with the home page of the app url
    response = requests.get(url) 
    # grabs the text of the page 
    urlText = response.text  
    #creates the urltext into a soup object 
    soup = BeautifulSoup(urlText, features="html") 
    if soup.find('div', attrs ={'class','ny-down'}) != None: 
        down_link = soup.find('div', attrs ={'class','ny-down'}).find('a', attrs={'class':'da'}).get('href') 
    else: 
        down_link = soup.find('div', attrs ={'class','down'}).find('a').get('href') 
    # add link extension     
    url = 'https://apkpure.com'+down_link  
    response = requests.get(url)
    urlText = response.text
    soup = BeautifulSoup(urlText,  features="html")
    if not os.path.isdir('./'+outpath ): 
        os.mkdir(outpath) #creates directory if it doesnt exist
    if not os.path.isdir('./'+outpath + '/apk_files'):
        direc = outpath + '/apk_files'
        os.mkdir(direc)
    if soup.find('a', attrs = {'id':'download_link'}) == None:
        return False 
    #finds the link to download 
    a =soup.find('a', attrs = {'id':'download_link'}).get('href') 
    resp = requests.get(a, stream = True) 
    #gets content of apk files 
    data = resp.content
    app_name = url.split('/')[3]  #get names of apk files 
    folder = os.path.abspath('') 
    #output file location 
    out  = os.path.join(folder, outpath+'/'+ 'apk_files/' + app_name+'.apk') 
    if len(out) > 200:
        return False
    
    
    with open(out, 'wb') as fh:
        fh.write(data)
    return app_name
    
def get_smalli(outpath, app_name):
    if not os.path.isdir('./'+outpath + '/smali'):
        direc = outpath + '/smali'
        os.mkdir(direc)
    command = 'apktool d ' + outpath+ '/apk_files/' + app_name + '.apk' 
    os.system(command)
    #moves file to output folder
    command3 = 'mv ' +app_name + ' '+outpath+'/smali/' 
    os.system(command3)
    
def main_scrape(name_path,kwargs):
    #To track all scraped xml files
    gz_list = []
    #Keep track of scraped apps
    scraped_apps = [] 
    #Keeps track of all apk_files
    apk_files = []
    # returns all links
    all_links = get_all_links() 


    i = 0
    np.random.seed(44)
    print('downloading APKs')
    pbar = tqdm(total = kwargs['total_links'])
    #runs till we collect the number of files needed
    while i < kwargs['total_links']: 
        #randomly choses a gz url
        gz_link = np.random.choice(all_links) 
        #checks if we have already scraped it 
        if gz_link not in gz_list: 
            #adds the gz url to scraped gz list
            gz_list.append(gz_link)  
            #Downoads the gz files and write is as an xml
            xml = get_xml(gz_link) 
            #grabs all the links to app's Apk's
            links = get_links_from_xml(xml) 
            j = 0
            while j < kwargs['Link_in_each_cat']:
                #randomly choses a link to app's apk
                apk_links = np.random.choice(links) 
                #to check if we havent already scraped it 
                if apk_links not in scraped_apps: 
                    #dowloads APK 
                    apk_file_name = create_apk(apk_links,name_path[0]) 
                    if apk_file_name == False:
                        break 
                    apk_files.append(apk_file_name)
                    scraped_apps.append(apk_links)  
                    i = i+1
                    j = j+1
                    pbar.update(1)

    pbar.close()
    print('output saved to /' + name_path[0]+ '/apk')
    print('decompiling APK files into smali code')
    #Decompile all Benign APK files into smali code
    for apk_ in tqdm(apk_files):
        get_smalli(name_path[0], apk_)
    print('output saved to /'+ name_path[0]+ '/smali')
    




