import requests
from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
 
 
def count_words(url, the_word):
    print(url, the_word)
    r = urllib2.urlopen(url)
    return str(r.read()).count(the_word)
    soup = BeautifulSoup(r.read(), 'lxml')
    words = soup.find(text=lambda text: text and the_word in text)
    if words == None:
        return 0
    print(words)
    return len(words)
 
 
def search(lasturls, url):
    for i in lasturls:
        try:
            page = urllib2.urlopen(i)
        except Exception:
            print("Couldn't load ", i)
            pass
        soup = BeautifulSoup( page, "lxml")
        for link in soup.findAll('a', attrs = {'href':re.compile("^http://")}):
            url.add(link.get('href'))
        for link in soup.findAll('a', attrs = {'href':re.compile("^https://")}):
            url.add(link.get('href'))
            # print(link)

def main():
    f = open('websites.txt', "r")
    f2 = open("websites_ranked.txt", "w")
    f3 = open("dictionary.txt", "r")
    dictt = f3.readlines()
    f3.close()
    lines = []
    z = f.readlines()
    for url in z:
        urls = {url}
        lasturls = {url}

        search(lasturls, urls)
        lasturls = set()
        for i in urls:
            if i not in urls:
                lasturls.add(i)
        search(lasturls, urls)
        lasturls = set()
        for i in urls:
            if i not in urls:
                lasturls.add(i)
        search(lasturls, urls)
        count = 0
        
        for i in urls:
            print(i)
        for word in dictt:
            count = count + count_words(url, word)

        if count > 0:
            lines.append(url.replace("\n", "") + " " + str(count))
        # print('\nUrl: {}\ncontains {} occurrences of word: {}'.format(url, count, word))
    f.close()
    for line in lines:
        f2.write(line + "\n")
    f2.close()
 
if __name__ == '__main__':
    main()