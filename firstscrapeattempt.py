'''
I wrote this code to practice web scraping.
I'm going to try and get all the books on the books.toscrape.com
that cost less than £50 and save them in a list of dictionaries
where I'd have all the ratings and prices and titles.
This ought to be fun.
'''
import re
import requests
import bs4

#All the pages with books generally come in this format
BASE_URL = 'http://books.toscrape.com/catalogue/page-{}.html'
#Initialize my list
UNDER_FIFTY = []
#I checked the website and there are 50 pages numbered 1 to 50
for n in range(1, 51):
    #Format the base url to the current page
    to_scrape_url = BASE_URL.format(n)
    #Use the get method from the requests library to pull the site HTML
    page = requests.get(to_scrape_url)
    #Use the Beautiful Soup Library and lxml engine to turn the site into a more accessible format
    soup = bs4.BeautifulSoup(page.text, 'lxml')
    #Checked the site for the class used to store the books
    #Use the select method to retrieve everything inside that class
    books = soup.select('.product_pod')
    #Loop through the books on the current page
    for book in books:
        #Use the select method again to pull out the price text
        price_text = book.select('.price_color')[0].text
        #Regex pattern for finding money (excluded the currency symbol)
        money_pattern = r'\d+.\d+'
        #Use the search method from the Regular Expressions library
        price = re.search(money_pattern, price_text)
        #Check if the price is under 50
        if float(price.group()) < 50:
            #Pull the title of the book
            title = book.select('a')[1]['title']
            price_actual = float(price.group())
            #Star ratings are formatted a little weird
            #Created this regex pattern to find them
            star_pattern = r'star-rating\s\w+'
            #Used the string version of the page to make it easier
            #I know this may not work on all sites
            star = re.search(star_pattern, str(book))
            star_text = star.group()
            star_rating = star_text.split()[1]
            #Make a dictionary with the book's info
            bookdict = {'title': title, 'price': price_actual, 'star-rating': star_rating}
            #Add that dictionary to my list
            UNDER_FIFTY.append(bookdict)
print(UNDER_FIFTY[0]['title'])
            