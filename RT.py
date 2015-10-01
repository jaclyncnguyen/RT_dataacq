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


def latest_earnings():
    rotten = feedparser.parse('http://www.rottentomatoes.com/browse/box-office')
    # links = soup.find('form', {'class': 'rt fl'})
    # links = links.findAll('option')

    # date_links = dict()
    # for url in links:
    #     dt_range = url.contents[0]
    #     date_links[dt_range] = "www.rottentomatoes.com" + (re.search(r'/browse/box.office/.rank.id.\d+.amp.country.us', str(url))).group()

    movie_urls = []
    soup = BeautifulSoup(rotten['feed']['summary'])
    links = soup.find('form', {'class': 'rt fl'})
    earnings = soup.findAll('td')
    for i in range(0,len(earnings), 9):
        rank = earnings[i].contents[0]
        last_rank = earnings[i+1].contents[0]
        rating = earnings[i+2].contents[0]
        try:
            rating2 = rating.find('span',{'class':'tMeterScore'}).contents[0]
        except:
            continue
        name = earnings[i +3].find('a',{'target':'_top'}).contents[0]
        movie_url = earnings[i+3].a['href']
        movie_urls.append(movie_url)
        weeks = (earnings[i+4]).contents[0]
        wkend_gross = (earnings[i+5]).contents[0]
        total_gross = (earnings[i+6]).contents[0]
        theat_avg = (earnings[i+7]).contents[0]
        num_theat = (earnings[i+8]).contents[0]

        write_output(rank, last_rank, rating2, name, weeks, wkend_gross, total_gross, theat_avg, num_theat)
    return movie_urls

latest_earnings()


# <form class="rt fl">
#  <option value="/browse/box-office/?rank_id=0&country=us">Last Weekend</option>
# <option value="/browse/box-office/?rank_id=1&country=us">Sep 18-Sep 20</option>
# <option value="/browse/box-office/?rank_id=2&country=us">Sep 11-Sep 13</option>
# <option value="/browse/box-office/?rank_id=3&country=us">Sep 04-Sep 06</option>
# <option value="/browse/box-office/?rank_id=4&country=us">Aug 28-Aug 30</option>
# <option value="/browse/box-office/?rank_id=5&country=us">Aug 21-Aug 23</option>
# <option value="/browse/box-office/?rank_id=6&country=us">Aug 14-Aug 16</option>
# <option value="/browse/box-office/?rank_id=7&country=us">Aug 07-Aug 09</option>
# <option value="/browse/box-office/?rank_id=8&country=us">Jul 31-Aug 02</option>
# <option value="/browse/box-office/?rank_id=9&country=us">Jul 24-Jul 26</option>
# <option value="/browse/box-office/?rank_id=10&country=us">Jul 17-Jul 19</option>
# <option value="/browse/box-office/?rank_id=11&country=us">Jul 10-Jul 12</option>
# <option value="/browse/box-office/?rank_id=12&country=us">Jul 03-Jul 05</option>
# <option value="/browse/box-office/?rank_id=13&country=us">Jun 26-Jun 28</option>
# <option value="/browse/box-office/?rank_id=14&country=us">Jun 19-Jun 21</option>