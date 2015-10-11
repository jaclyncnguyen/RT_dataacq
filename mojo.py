from BeautifulSoup import BeautifulSoup
import re
import csv
import codecs

def write_output(title, gross):
    with open('mojo.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',lineterminator='\n')
        writer.writerow([title, gross])
    csvfile.close()
    return None

def get_mojo():

    movie_2014 = []
    mojo = codecs.open('mojo.html', 'r', 'utf-8')
    soup = BeautifulSoup(mojo)
    blah = soup.findAll('tr')
    for i in range(9, 109):
        title = (blah[i].find('a')).contents[0]
        gross = (blah[i].findAll('b'))[1].contents[0]
        gross = gross.replace('$','')
        gross = gross.replace(',', '')
        gross = int(gross)
        write_output(title,gross)
        movie_2014.append(title)
    return movie_2014
movie_titles_2014 = get_mojo()