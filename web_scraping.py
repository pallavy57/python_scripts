import csv
from bs4 import BeautifulSoup as soup
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}
my_url = "https://www.flipkart.com/search?q=data%20science%20book&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

url = requests.get(my_url, headers=headers)
# print(url.content)
page_soup = soup(url.content, "html.parser")

containers = page_soup.findAll("div", {"class": "_4ddWXP"})
# print(soup.prettify(containers[0]))

    
# Open the csv file for writing
with open('products.csv', 'w',encoding="utf-8", newline='') as fileObj:
    # Creater a CSV writer object
    writerObj = csv.writer(fileObj)
    # Add header row as the list
    writerObj.writerow(['Product_Name', 'Pricing', 'Discount', 'Delivery'])
    title = None
    price = None
    discount = None
    delivery = None
    for container in containers:
        title = container.find("a", {"class": "s1Q9rs"})
        price = container.find("div", {"class": "_30jeq3"})
        title = title.get_text()
        price = price.get_text()
        discount = container.find("div", {"class": "_3Ay6Sb"})
        if (discount != None):
            discount = discount.find("span")
            discount = discount.get_text()
            discount = discount.split(" ")[0]
        else:
            discount = 0
        delivery = container.find("div", {"class": "_2Tpdn3"})
        if (delivery != None):
            if (type(delivery) == 'str'):
                delivery = delivery
            else:
                delivery = delivery.get_text()
        else:
            delivery = "No Status"
        row=(title, price, discount,delivery)   
        print(row ) 
        # Append the list as a row to the csv file
        writerObj.writerow(row)    
  
