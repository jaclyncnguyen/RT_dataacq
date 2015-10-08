import urllib2
import json
import feedparser
from BeautifulSoup import BeautifulSoup
import re
import csv

def write_output(rank, last_rank, rating2, name, weeks, wkend_gross, total_gross, theat_avg, num_theat):
    with open('latest_earnings.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',lineterminator='\n')
        writer.writerow([rank, last_rank, rating2, name, weeks, wkend_gross, total_gross, theat_avg, num_theat])
    csvfile.close()
    return None

def write_allearnings(weekend, rank, rating2, name, weeks, wkend_gross):
    with open('weekend_earnings.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',lineterminator='\n')
        writer.writerow([weekend, rank, rating2, name, weeks, wkend_gross])
    csvfile.close()
    return None


def latest_earnings():
    rotten = feedparser.parse('http://www.rottentomatoes.com/browse/box-office')

    movie_names = set()
    soup = BeautifulSoup(rotten['feed']['summary'])

    links = soup.find('form', {'class': 'rt fl'})
    links = links.findAll('option')

    date_links = dict()
    for url in links:
        dt_range = url.contents[0]
        date_links[dt_range] = "https://www.rottentomatoes.com" + (re.search(r'/browse/box.office/.rank.id.\d+.amp.country.us', str(url))).group()
    del date_links['Last Weekend']

    earnings = soup.findAll('td')
    for i in range(2,len(earnings), 9):
        rank = earnings[i].contents[0]
        last_rank = earnings[i+1].contents[0]
        rating = earnings[i+2].contents[0]
        try:
            rating2 = rating.find('span',{'class':'tMeterScore'}).contents[0]
        except:
            continue
        name = earnings[i +3].find('a',{'target':'_top'}).contents[0]
        movie_url = earnings[i+3].a['href']
        movie_names.add(name)
        weeks = (earnings[i+4]).contents[0]
        wkend_gross = (earnings[i+5]).contents[0]
        total_gross = (earnings[i+6]).contents[0]
        theat_avg = (earnings[i+7]).contents[0]
        num_theat = (earnings[i+8]).contents[0]

        write_output(rank, last_rank, rating2, name, weeks, wkend_gross, total_gross, theat_avg, num_theat)
    return movie_names, date_links

def gross_earning(movie_names, date_links):
    for link in date_links:
        new_url = date_links[link]
        rotten2 = feedparser.parse(new_url)
        soup = BeautifulSoup(rotten2['feed']['summary'])
        gross_earnings = soup.findAll('td')
        for i in range(2, len(gross_earnings), 5):
            rank = gross_earnings[i].contents[0]
            if re.match(r'^\d+$', str(rank)) is None:
                continue
            rating = gross_earnings[i+1].contents[0]
            try:
                rating2 = rating.find('span',{'class':'tMeterScore'}).contents[0]
            except:
                continue
            try:
                name = gross_earnings[i +2].find('a',{'target':'_top'}).contents[0]
                movie_url = gross_earnings[i+2].a['href']
                movie_names.add(name)
            except:
                continue
            wkend_gross = (gross_earnings[i+4]).contents[0]
            weeks = (gross_earnings[i+3]).contents[0]
            write_allearnings(link, rank, rating2, name, weeks, wkend_gross)
    return movie_names

def main():
    movie_names, date_links = latest_earnings()
    movie_names2 = gross_earning(movie_names, date_links)
    print movie_names2
main()
