import time

from splinter import Browser
import requests

#------------------------------------------------------------------------------

# setup windows
# open youtube
ytbwindow = Browser('firefox')
ytbwindow.visit('https://www.youtube.com/')

# open youtubetomp3
ytmp3window = Browser('firefox')
ytmp3window.visit('https://ytmp3.cc/en13/')

# open playlist and wait a lil
spotwindow = Browser('firefox')
spotwindow.visit('https://open.spotify.com/playlist/7281Ff25XGcPg7HiAIJKA2?si=s4h3lp3AQp-YOw2G4zciaw')
time.sleep(5)

#------------------------------------------------------------------------------

# meat and potatoes
# gather tracklist
tracklist = spotwindow.find_by_css('ol.tracklist').find_by_tag('li')

# for each row/song in playlist:
for row in tracklist:
    # select and copy song title
    song = row.find_by_css('div.tracklist-name.ellipsis-one-line').value
    # and artist name
    artist = row.find_by_css('a.tracklist-row__artist-name-link').value

    # make search query for yt search and filename, print in terminal
    query = str(song + " " + artist)
    print(query)

    # paste query in yt search bar, click 'search'
    search = ytbwindow.find_by_name('search_query')
    search.clear()
    search.fill(query)
    ytbwindow.find_by_id('search-icon-legacy').click()

    # copy first link of results
    link = str(ytbwindow.find_by_css('ytd-video-renderer.style-scope.ytd-item-section-renderer')[0].find_by_id('thumbnail')['href'])

    # paste url in ytmp3 input, click convert or 'submit'
    submission = ytmp3window.find_by_name('video')
    submission.clear()
    submission.fill(link)
    ytmp3window.find_by_id('submit').click()

    # wait to allow ample time for processing
    time.sleep(30)
    # find main menu for simpler code and link retrieval
    buttons = ytmp3window.find_by_id('buttons').find_by_tag('a')

    # use provided download link in 'Download' to create download request
    r = requests.get(str(buttons[0]['href']))
    # create new file in 'Downloads' folder, wait
    file = '/home/yuh/Downloads/' + query
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
