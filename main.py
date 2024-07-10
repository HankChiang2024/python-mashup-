#part1 從維基百科爬取「火影忍者疾風傳」片尾曲資訊

import re, random, requests
from bs4 import BeautifulSoup

##########以下用BeautifulSoup爬取「火影忍者疾風傳」的維基百科網頁

url = 'https://zh.wikipedia.org/wiki/%E7%81%AB%E5%BD%B1%E5%BF%8D%E8%80%85%E7%96%BE%E9%A2%A8%E5%82%B3#%E7%89%87%E9%A0%AD%E6%9B%B2'
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser') #用BeautifulSoup解析原始碼

##########以上用BeautifulSoup爬取「火影忍者疾風傳」的維基百科網頁

##########以下找到片尾曲並印出

song_tables = soup.find_all('table', class_="wikitable", style="text-align: center;font-size:small;") #片頭片尾兩個table
TR_list = song_tables[1].find_all('tr') #找出片尾曲表格中所有的row的資訊
song_name_list = [] #歌單list
for i in range(1,len(TR_list)): #0為目錄
    TR_str = str(TR_list[i]) #轉成str type
    #只有歌名有<b>標籤
    if '<b><span lang="ja"' in TR_str: #歌名有日文
        temp_name1_list = re.findall('<b><span lang="ja">.*</span></b>', TR_str) #一個元素的list
        if '<br/>' in temp_name1_list[0]: #歌名有〜而且換行的話
            song_name = re.findall('"ja">(.*)<br/>', temp_name1_list[0])[0] + \
                        re.findall('<br/>(〜.*〜)', temp_name1_list[0])[0] #str type
        else:
            song_name = re.findall('"ja">(.*)</span>', temp_name1_list[0])[0] #str type
    else: #歌名沒有日文
        song_name = re.findall('<b>(.*)</b>', TR_str)[0] #str type
    song_name_list.append(song_name) #將歌名附加到歌單
song_name_list_copy = song_name_list.copy()
random.shuffle(song_name_list_copy)
print('Test whether you are a really stan of Naruto or not.\n')

for i in range(40): #印出所有歌曲
    print(str(i+1) + '. ' + song_name_list_copy[i])
    if i%10 == 9:
        print()
print('\nThese are all EDs of Naruto in chaotic order.\n')


##########以上找到片尾曲並印出

##########以下找到章節

chapter_table = soup.find_all('table', class_="wikitable", style="font-size:small;")[0]
# print(chapter_table)

chapter_th_list = chapter_table.find_all('th', colspan="10")
chapter_list = []
for i in chapter_th_list:
    chapter_list.append(i.string[:len(i.string)-1])
chapter_list_copy = chapter_list.copy()
random.shuffle(chapter_list_copy)

##########以上找到章節

##########以下列出歌曲對應的章節


chapter_pair_list = [chapter_list[0], chapter_list[0], chapter_list[:2], chapter_list[1],
                      chapter_list[2], chapter_list[2:4], chapter_list[3:5], chapter_list[4],
                      chapter_list[4:6], chapter_list[5], chapter_list[5], chapter_list[5:8],
                      chapter_list[7], chapter_list[7:9], chapter_list[8], chapter_list[8:10],
                      chapter_list[9], chapter_list[9:11], chapter_list[10], chapter_list[11],
                      chapter_list[11], chapter_list[11:13], chapter_list[12:14], chapter_list[14],
                      chapter_list[14], chapter_list[14:16], chapter_list[15], chapter_list[15:17],
                      chapter_list[16:18], chapter_list[17:19], chapter_list[18], chapter_list[19],
                      chapter_list[19:21], chapter_list[20], chapter_list[21], chapter_list[21:23],
                      chapter_list[22:24], chapter_list[23], chapter_list[24:26], chapter_list[26:28]]
chapter_pair_list_copy = chapter_pair_list.copy()

##########以上列出歌曲對應的章節list

##########以下將歌曲和對應章節做成dict

song_chapter_list = []
for i in song_name_list:
    count = 0
    for j in chapter_pair_list_copy:
        song_chapter_list.append((i,j))
        chapter_pair_list_copy.pop(0)
        count += 1
        if count == 1:
            break
song_chapter_dict = dict(song_chapter_list)

##########以上將歌曲和對應章節做成dict


########################################


#part2 spotify api 隨機產生五首歌曲，回答對應章節，計算分數；自行輸入歌曲，回答對應章節

import spotipy, json, random
from spotipy.oauth2 import SpotifyClientCredentials

##########以下取得client認證並列出track id

spotify_client_id = 'c86fdce94d8d4feca4204f5e0ea5b065'
spotify_client_secret = 'b1048428034e4d69bc96ab290348e0fe'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = spotify_client_id,
                                                           client_secret = spotify_client_secret))

#手刻，剛好歌曲連結有包含track id
track_id_list = ['0lTk2LRaRNybgkKn4Q8PQz', '2Aq726y1hKsStf9Bmofxjs', '6b7BqSkpIK9Qmt3t57Rvwt',
                 '5PZRgKfH4dPWV9kGjm5J7m', '0JnAMQGCvjyWKGwNm38jAM', '0wDG6p0LEyrGD5mwOtdcw3',
                 '2rx7VAzDuLIRJVHlqwK6Zp', '17oUzgHMjWK2A8LQVlT80d', '2kvvZ9IPqTPjXOXHuaFXdA',
                 '7y4PCLY8zT13RzCvMsYPUh', '6lqjqNdsQ4eymviIu7Qsa9', '3X0CWpuoxmhYOmKL2oVIpZ',
                 '3abl06N92fbHupUhgM8war', '3VbpuVvobZbMJ86p1w3GKK', '4RCJYly0A1qlytafv4Ko6T',
                 '0t4AdmBiRmq8TW8nTX72Aj', '5sFG4DLIXyHtbmvHxo4lW7', '33ehIw586sGwarusJ0YdHi',
                 '1MwsgSI9pajUVZ0vVZEz6j', '64h5a1i13Gil2HrXUf91SQ', '6imL0aJnaP49YVRT9NOFx8',
                 '3A15Rv84GTckeKm2xVKwfM', '5pnfJX8iGITxd2ClIED6Kr', '0xPHALeBb3aLEZrj0T0R2P',
                 '5uub76nICLU6sJURtpe6yq', '1ZDieCqb5nS4KD0XpR0oGp', '6BvZ8MA8aLRexVwpf27bht',
                 '5DR4xKHHxyTp4xLYZMEYFs', '68W6SPPczmrZvOL1aiKYCM', '5NGWulc0W5ctrG8RSDcnoW',
                 '5vTePJBD1sHoBq83ZdIr8m', '1jnrstx3ykM54Xu05Ox7d5', '4OMRC8O4mVOmDMDs9RpgH0',
                 '2aQDpTmWnHAaNIkv1bdSmE', '7kEFyP8uYvvK8gmTnV2WG6', '1RG6wybhwJefFTuyRQxCvI',
                 '5uQzeZ974szlPTiiYUmseG', '55qI03VZEqdVtUVDxUsZwe', '51H9ST2xrFXF68sPQ3JkT9',
                 '1oifj4ZzYNNDvkM9mByhsM']

##########以上取得client認證並列出track id

##########以下為測驗說明

print('There are 5 quentions.\nEach question is a ED and the answer is the corresponding chapter.')
print('Click the song link and listen to the music carefully.\n')
print('Each question has 5 options with at least one answer.\nOnly need to choose one to answer.')
print('P.S.: Maybe there are other answers not in the options.\n')
start_button = input('Please enter "start" to run the test: ')
while start_button != 'start':
    print('Unexpected messages.')
    start_button = input('Please enter again: ')
print()

##########以上為測驗說明

##########以下預設分數0，定出級別，題目(片尾曲之一)和選項隨機出，回答並計分

score = 0
level_list = ['假粉', '路人', '高手', '大師', '博學家', '全知']
for i in range(5):
    random_song = random.choice(song_name_list_copy)
    print(i+1)
    print('song:', random_song)
    track_id = track_id_list[song_name_list.index(random_song)]
    info = sp.track('spotify:track:' + track_id)
    artists = info['artists'][0]['name']
    album = info['album']['name']
    link = info['external_urls']['spotify']
    print('link: ' + link + '\n')

    #製作選項並印出
    if type(song_chapter_dict[random_song]) == str:
        tmp = song_chapter_dict[random_song]
        if chapter_list_copy.index(tmp) == 0:
            options = chapter_list_copy[26:] + chapter_list_copy[:3]
        elif chapter_list_copy.index(tmp) == 1:
            options = [chapter_list_copy[27]] + chapter_list_copy[:4]
        elif chapter_list_copy.index(tmp) == 26:
            options = chapter_list_copy[24:] + [chapter_list_copy[0]]
        elif chapter_list_copy.index(tmp) == 27:
            options = chapter_list_copy[25:] + chapter_list_copy[:2]
        else:
            options = chapter_list_copy[chapter_list_copy.index(tmp)-2:
                                        chapter_list_copy.index(tmp)+3]
    else:
        tmp = random.choice(song_chapter_dict[random_song])
        if chapter_list_copy.index(tmp) == 0:
            options = chapter_list_copy[26:] + chapter_list_copy[:3]
        elif chapter_list_copy.index(tmp) == 1:
            options = [chapter_list_copy[27]] + chapter_list_copy[:4]
        elif chapter_list_copy.index(tmp) == 26:
            options = chapter_list_copy[24:] + [chapter_list_copy[0]]
        elif chapter_list_copy.index(tmp) == 27:
            options = chapter_list_copy[25:] + chapter_list_copy[:2]
        else:
            options = chapter_list_copy[chapter_list_copy.index(tmp) - 2:
                                        chapter_list_copy.index(tmp) + 3]
    random.shuffle(options)
    for option in options:
        print(options.index(option)+1, option)

    enter_chapter_name = input('\nPlease enter the corresponding chapter: ')

    while True:
        if enter_chapter_name != song_chapter_dict[random_song]:
            if enter_chapter_name not in song_chapter_dict[random_song]:
                print('Wrong answer!\n')
                break
            else:
                print('Correct answer!\n')
                score += 1
                break
        else:
            print('Correct answer!\n')
            score += 1
            break
print('score:', score*20, 'level:', level_list[score])

##########以上預設分數0，定出級別，題目(片尾曲之一)和選項隨機出，回答並計分

##########以下取得所有歌曲的artist和album

artist_list = []
album_list = []
for i in track_id_list:
    info = sp.track('spotify:track:' + i)
    artist_list.append(info['artists'][0]['name'])
    album_list.append(info['album']['name'])
artist_list_copy = artist_list.copy()

artist_list_copy[0] = 'Home-Made-Kazoku'
artist_list_copy[2] = 'Little-by-Little'
artist_list_copy[5] = 'NICO-Touches-the-Walls'
artist_list_copy[8] = 'SUPER-BEAVER'
artist_list_copy[10] = 'Biccurry-Akatsuka'
artist_list_copy[15] = 'Aqua-Timez'
artist_list_copy[16] = 'Home-Made-Kazoku'
artist_list_copy[21] = 'AISHA-feat.-CHEHON'
artist_list_copy[26] = 'Akihisa-Kondo'
artist_list_copy[30] = 'Shiori-Tomita'
artist_list_copy[31] = 'Diana-Garnet'
artist_list_copy[35] = 'Thinking-Dogs'
artist_list_copy[36] = 'Kuroneko-Chelsea'
artist_list_copy[37] = 'Huwie-Ishizaki'

##########以上取得所有歌曲的artist和album

##########以下讓使用者自行搜索歌曲並得到相關資訊

print('\nNow you can enter one of the EDs.\nThen the program will return the details.\n')

#印出所有歌曲
for i in range(40):
    print(str(i+1) + '. ' + song_name_list_copy[i])
    if i%10 == 9:
        print()
print()

enter_song_name = input('Please enter one of them: ')
while True:
    try:
        track_id = track_id_list[song_name_list.index(enter_song_name)]
        print('Click the link and listen to the music carefully.')
        break
    except ValueError:
        enter_song_name = input('Unexpected input!\nEnter again: ')

info = sp.track('spotify:track:' + track_id)
artists = info['artists'][0]['name']
album = info['album']['name']
link = info['external_urls']['spotify']
print('artists:', artists)
print('album:', album)
print('link:', link)
print()

##########以上讓使用者自行搜索歌曲並得到相關資訊

##########以下回答歌曲對應章節

if type(song_chapter_dict[enter_song_name]) == str:
    tmp = song_chapter_dict[enter_song_name]
    if chapter_list_copy.index(tmp) == 0:
        options = chapter_list_copy[26:] + chapter_list_copy[:3]
    elif chapter_list_copy.index(tmp) == 1:
        options = [chapter_list_copy[27]] + chapter_list_copy[:4]
    elif chapter_list_copy.index(tmp) == 26:
        options = chapter_list_copy[24:] + [chapter_list_copy[0]]
    elif chapter_list_copy.index(tmp) == 27:
        options = chapter_list_copy[25:] + chapter_list_copy[:2]
    else:
        options = chapter_list_copy[chapter_list_copy.index(tmp)-2:
                                    chapter_list_copy.index(tmp)+3]

else:
    tmp = random.choice(song_chapter_dict[enter_song_name])
    if chapter_list_copy.index(tmp) == 0:
        options = chapter_list_copy[26:] + chapter_list_copy[:3]
    elif chapter_list_copy.index(tmp) == 1:
        options = [chapter_list_copy[27]] + chapter_list_copy[:4]
    elif chapter_list_copy.index(tmp) == 26:
        options = chapter_list_copy[24:] + [chapter_list_copy[0]]
    elif chapter_list_copy.index(tmp) == 27:
        options = chapter_list_copy[25:] + chapter_list_copy[:2]
    else:
        options = chapter_list_copy[chapter_list_copy.index(tmp) - 2:
                                    chapter_list_copy.index(tmp) + 3]

random.shuffle(options)
for option in options:
    print(options.index(option)+1, option)
print()
enter_chapter_name = input('Please enter the corresponding chapter: ')
#猜到對為止
while True:
    if enter_chapter_name != song_chapter_dict[enter_song_name]:
        if enter_chapter_name not in song_chapter_dict[enter_song_name]:
            print('Wrong answer!')
            enter_chapter_name = input('Guess again: ')
        else:
            print('Correct answer!\n')
            break
    else:
        print('Correct answer!\n')
        break

##########以上回答歌曲對應章節


########################################


#part3 kkbox api 以輸入歌曲的artist做為關鍵字搜索，產生最多前score+1筆相關歌曲

import requests, re, http.client

##########以下重要參數

key_words = artist_list_copy[song_name_list.index(enter_song_name)]
CLIENT_ID = '2765c256cad71bcd288cc3f3f84fe7c5'
CLIENT_SECRET = '6caf61e8866744bb06b57749dc765110'

##########以上重要參數


##########以下取得Token
def get_access_token():
    # API網址
    url = "https://account.kkbox.com/oauth2/token"
    # 標頭
    headers = {
		"Content-Type": "application/x-www-form-urlencoded",
		"Host": "account.kkbox.com"
	}
    # 參數
    data = {
		"grant_type": "client_credentials",
		"client_id": CLIENT_ID,
		"client_secret": CLIENT_SECRET
	}
    access_token = requests.post(url, headers=headers, data=data)
    #return access_token
    return access_token.json()["access_token"]
access_token = get_access_token()

##########以上取得Token

##########以下取得以歌手名搜索後前score+1筆結果的track id

conn = http.client.HTTPSConnection("api.kkbox.com")
headers = {
    'accept': "application/json",
    'authorization': "Bearer " + access_token
    }
conn.request("GET", "/v1.1/search?q=" + key_words + "&type=track&territory=TW&offset=0&limit=" + str(score+1),
             headers=headers)
res = conn.getresponse()
data = res.read() #data.decode("utf-8") 為str
top_score_track_id_list = re.findall('id":.([^"]*)', data.decode("utf-8"))

#以上取得以歌手名搜索後前score+1筆結果的track id

##########以下取得token 第三方平台(sdk)格式

from kkbox_developer_sdk.auth_flow import KKBOXOAuth
auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
token = auth.fetch_access_token_by_client_credentials()
from kkbox_developer_sdk.api import KKBOXAPI
kkboxapi = KKBOXAPI(token)

##########以上取得token 第三方平台(sdk)格式

##########以下取得相關歌曲的詳細資訊並印出 by kkbox_developer_sdk

print('Here are the most related songs with the artist corresponding to the song.\n')
for i in range(0, len(top_score_track_id_list)-1, 3):
    track_id = top_score_track_id_list[i]
    track = kkboxapi.track_fetcher.fetch_track(track_id)
    print(int(i/3)+1)
    print('song:', track['name'])
    print('artist:', track['album']['artist']['name'])
    print('album:', track['album']['name'])
    print('link:', track['url'])
    print()

##########以下取得相關歌曲的詳細資訊並印出 by kkbox_developer_sdk

print('Have fun!')
