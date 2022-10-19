import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# set target website
baseurl = "https://www.nespresso.co.id/"

# set user agent to access
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
productlinks = []
t={}
data=[]
c=0

# get from specific product category
for x in range(1,6):
    k = requests.get('https://www.nespresso.co.id/coffee.html'.format(x)).text
    soup=BeautifulSoup(k,'html.parser')
    # get list of product under category
    productlist = soup.find_all("li",{"class":"product"})
    # print(productlist)

    # get link to list of product under category
    for product in productlist:
        product_name = product.find("div",{"class":"product-name"})
        link = product_name.find("a").get('href')
        productlinks.append(link)

# access each product link
for link in productlinks:
    f = requests.get(link,headers=headers).text
    hun=BeautifulSoup(f,'html.parser')
  
    # get product price
    try:
        price=hun.find("span",{"class":"price"}).text.replace('\n',"")
    except:
        price = None

    # get product description
    try:
        description=hun.find("div",{"class":"wysiwyg"}).text.replace('\n',"")
    except:
        description=None

    # get product attribute
    try:
        attribute_ = hun.find("div",{"class":"value"})
        attribute = attribute_.find("p").text.replace('\n',"")
        # print(attribute)
    except:
        attribute=None

    # get product name
    try:
        name=hun.find("span",{"class":"base"}).text.replace('\n',"")
    except:
        name=None

    coffee = {"name":name,"price":price,"attribute":attribute,"description":description}

    data.append(coffee)
    c=c+1
    print("completed",c)

df = pd.DataFrame(data)

# path = os.getcwd()
# UPLOAD_FOLDER = os.path.join(path, 'upload')
# df.to_json(UPLOAD_FOLDER+'/data.json', orient='records', lines=True)
# df.to_csv(UPLOAD_FOLDER+'/data.csv', encoding='utf-8', index=False)

# generate output in json and csv 
df.to_json('output.json', orient='records', lines=True)
df.to_csv('output.csv', encoding='utf-8')
