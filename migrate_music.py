import json
import os

from driver import Driver
from locators import *
from methods import BasePage
from variables import *

driver = Driver.get_driver()
methods = BasePage(driver)

# login
if EMAIL == '' or PASSWORD:
    raise Exception('Please fill credentials in the "variables.py"!')
methods.go_to_exact_url(LOGIN_URL)
methods.type(EMAIL, *email_input)
methods.click(*email_next_btn)
methods.type(PASSWORD, *password_input)
methods.click(*password_next_btn)
methods.wait_until_element_is_visible(login_check)

# Gather google music library
if not os.path.isfile('songs.json'):
    methods.go_to_exact_url(GOOGLE_MUSIC_URL)
    total_count = int(methods.get_attribute_value('data-count', *songs_table))
    music_library = []
    methods.click(*songs_table)
    for index in range(total_count):
        song_details = {'title': methods.get_text(*methods.get_parametrized_locator(song_name, [index])),
                        'artist': methods.get_text(*methods.get_parametrized_locator(song_artist, [index])),
                        'album': methods.get_text(*methods.get_parametrized_locator(song_album, [index]))}
        music_library.append(song_details)
        methods.click(*methods.get_parametrized_locator(song_name, [index]))
        methods.press_down()

    with open('songs.json', 'w') as file:
        file.write(json.dumps(music_library))
else:
    with open('songs.json') as f:
        music_library = json.load(f)

# YouTube music

methods.go_to_exact_url(YOUTUBE_MUSIC_URL)
if not methods.is_element_present(*google_playlist_item):
    methods.click(*create_playlist_btn)
    methods.click(*playlist_name_field)
    methods.type('Google music songs', *playlist_name_field)
    methods.click(*playlist_desc_field)
    methods.type('All songs migrated from the google music automatically', *playlist_desc_field)
    methods.click(*submit_playlist_btn)
else:
    methods.click(*playlist_link)
    methods.wait_until_element_is_visible(shuffle_play_btn)
    methods.scroll_page_playlist(*spinner)
    playlist_songs = [_.text for _ in methods.find_elements(*playlist_songs)]
    for pl_song in playlist_songs:
        if pl_song.lower() in [_['title'].lower() for _ in music_library]:
            music_library.remove([_ for _ in music_library if _['title'].lower() == pl_song.lower()][0])
    with open('songs.json', 'w') as file:
        file.write(json.dumps(music_library))

not_found_songs = []
for song in music_library:
    found = False
    if song['artist'].lower() == 'space of variations' or song['album'] == 'I Loved You at Your Darkest':
        break
    url = f'{YOUTUBE_MUSIC_SEARCH_URL}{song["title"].replace(" ", "+")}+{song["artist"].replace(" ", "+")}'
    methods.go_to_exact_url(url)
    methods.click(*songs_results_filter)
    for ind in range(len(methods.find_elements(*yt_searched_songs))):
        index = ind + 1
        if not methods.is_element_present(
                *methods.get_parametrized_locator(yt_song_by_title, [song['title'].lower()])):
            break
        yt_song_details = {'title': methods.get_text(*methods.get_parametrized_locator(yt_song_title, [index])),
                           'artist': methods.get_text(*methods.get_parametrized_locator(yt_song_artist, [index])),
                           'album': methods.get_text(*methods.get_parametrized_locator(yt_song_album, [index]))}
        if methods.compare_songs(song, yt_song_details):
            methods.hover(*methods.get_parametrized_locator(yt_song_title, [index]))
            methods.click(*methods.get_parametrized_locator(yt_song_option, [index]))
            methods.click(*methods.get_parametrized_locator(yt_add_to_playlist, [index]))
            methods.click(*methods.get_parametrized_locator(yt_google_playlist, [index]))
            if not methods.is_element_visible(*are_you_sure_dialog):
                methods.wait_until_visibility_of_element_located(added_msg)
            found = True
            break

    if found is False:
        not_found_songs.append(song)

with open('not_found_songs.json', 'w') as file:
    file.write(json.dumps(not_found_songs))
driver.quit()
