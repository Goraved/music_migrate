from selenium.webdriver.common.by import By

to_lower = 'translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")'

# login
email_input = (By.XPATH, '//input[@type="email"]')
email_next_btn = (By.XPATH, '//div[@role="button"][@id="identifierNext"]')
password_input = (By.XPATH, '//input[@type="password"]')
password_next_btn = (By.XPATH, '//div[@role="button"][@id="passwordNext"]')
login_check = (By.XPATH, '//input[@aria-autocomplete="list"]')
# google
songs_table = (By.XPATH, '//tbody')
song_row = (By.XPATH, '//tr[@data-index="{}"]')
song_artist = (By.XPATH, '//tr[@data-index="{}"]/td[@data-col="artist"]/span/a')
song_name = (By.XPATH, '//tr[@data-index="{}"]/td[@data-col="title"]/span')
song_album = (By.XPATH, '//tr[@data-index="{}"]/td[@data-col="album"]/span/a')
# youtube
google_playlist_item = (By.XPATH, '//ytmusic-two-row-item-renderer[contains(.,"Google")]')
create_playlist_btn = (By.XPATH, '//*[contains(@src,"create-playlist")]')
playlist_name_field = (By.XPATH, '//div[@id="labelAndInputContainer"]/iron-input/input')
playlist_desc_field = (By.XPATH, '//div[@id="labelAndInputContainer"]/iron-autogrow-textarea/div/textarea')
submit_playlist_btn = (By.XPATH, '//paper-button[contains(@class,"submit-button")]')
playlist_link = (By.XPATH, '//a[contains(.,"Google music songs")]')
playlist_song_titles = (By.XPATH, '//yt-formatted-string/span[contains(%s,"{}")]' % to_lower)
playlist_songs = (By.XPATH, '//div[@id="contents"]//yt-formatted-string[contains(@class,"title")]/span')
shuffle_play_btn = (By.XPATH, '//span[contains(.,"Shuffle play")]')
spinner = (By.XPATH, '//div[@class="circle style-scope paper-spinner"]')
# YT search
songs_results_filter = (By.XPATH, '//ytmusic-chip-cloud-chip-renderer[contains(.,"Songs")]')
yt_searched_songs = (By.XPATH, '//ytmusic-responsive-list-item-renderer')
yt_song_title = (By.XPATH, '//ytmusic-responsive-list-item-renderer[{}]//*[contains(@class,"title")]/span')
yt_song_artist = (By.XPATH, '//ytmusic-responsive-list-item-renderer[{}]//*[contains(@class,"flex")][1]/a')
yt_song_album = (By.XPATH, '//ytmusic-responsive-list-item-renderer[{}]//*[contains(@class,"flex")][2]/a')
yt_song_option = (By.XPATH, '//ytmusic-responsive-list-item-renderer[{}]//iron-icon')
yt_add_to_playlist = (By.XPATH, '//span[contains(.,"Add to playlist")]')
yt_google_playlist = (By.XPATH, '//span[contains(.,"Google music songs")]')
yt_song_by_title = (By.XPATH,
                    '//ytmusic-responsive-list-item-renderer//*[contains(@class,"title")]/span[contains(%s, "{}")]' % to_lower)
added_msg = (By.XPATH, '//span[contains(.,"Added to Google music songs")]')
are_you_sure_dialog = (By.XPATH, '//span[contains(.,"Are you sure?")]')
