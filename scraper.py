# Trey Phillips
# SpotTubeScraper: takes Spot playlist and downloads each song
#   using YT and ytmp3.com.
#
# HINT: use "globals" for custom settings and site setup
#
# DISCLAIMER: FOR EDUCATIONAL PURPOSES ONLY
#
# TODO:
#   * can't download songs with japanese characters - implement other character sets
#   * verify operability with other browsers, OSs
#       developed on Firefox on Ubuntu
#   * exceptions & exception handling
#   * metadata edits upon file creation (including album?)
#   * better yt vid selection process (not first video necessrily lol)
#   * allow '\' and '/' without screwing up directory reading
#   * create list for failed downloads
#   * catch occasional error from ytmp3.com

#------------------------------------------------------------------------------

import time

from splinter import Browser
import re
import requests

#------------------------------------------------------------------------------

# "globals" - for custom setups
custom_playlist = 'https://open.yourplaylist'
browser_type = 'firefox'
directory = '/your/folder/here'
yt-site = 'https://www.yt.com/'

#------------------------------------------------------------------------------

# setup windows
# open playlist and wait a lil
spotwindow = Browser(browser_type)
spotwindow.visit(custom_playlist)
time.sleep(5)

# open YT
ytbwindow = Browser(browser_type)
ytbwindow.visit(yt-site)

# open ytmp3
ytmp3window = Browser(browser_type)
ytmp3window.visit('https://ytmp3.cc/en13/')

#------------------------------------------------------------------------------

# meat and potatoes
# gather tracklist
tracklist = spotwindow.find_by_css('ol.tracklist').find_by_tag('li')

# for each row/song in playlist:
for row in tracklist:
    # copy song title and artist name
    song = row.find_by_css('div.tracklist-name.ellipsis-one-line').value
    artist = row.find_by_css('a.tracklist-row__artist-name-link').value

    # make search query for yt search and filename, print in terminal
    query = str(song + " - " + artist)
    query = re.sub('[/]', '', query)
    print(query)

    # paste query in yt search bar, click 'search', wait
    search = ytbwindow.find_by_name('search_query')
    search.clear()
    search.fill(query)
    ytbwindow.find_by_id('search-icon-legacy').click()
    time.sleep(10)

    # copy first link of results
    link = str(ytbwindow.find_by_css('ytd-video-renderer.style-scope.ytd-item-section-renderer')[0].find_by_id('thumbnail')['href'])

    # paste url in ytmp3 input, click convert/submit, wait for processing
    submission = ytmp3window.find_by_name('video')
    submission.clear()
    submission.fill(link)
    ytmp3window.find_by_id('submit').click()
    time.sleep(30)

    # find main menu for simpler code and link retrieval
    # buttons[0] = Download, buttons[1] = Dropbox, buttons[2] = Convert next
    buttons = ytmp3window.find_by_id('buttons').find_by_tag('a')

    # use provided download link in 'Download' to create download request
    r = requests.get(str(buttons[0]['href']))

    # create file in directory, write data to it, wait
    file = directory + query
    open(file, 'wb').write(r.content)
    time.sleep(5)

    # prepare page for next song, wait
    ytmp3window.visit(str(buttons[2]['href']))
    time.sleep(5)

#------------------------------------------------------------------------------

# done making requests, close all windows
spotwindow.quit()
ytbwindow.quit()
ytmp3window.quit()
