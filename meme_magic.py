# import taipy library
from taipy.gui import Gui, notify

import requests
import urllib

username = "AbideenTunde"
password = "2nhnUFx@bmbs4Jf"

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

#Fetch the available memes
data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]

meme_template = ""
top_text = ""
bottom_text = ""
meme_download = None
meme_image = None

memes = [(str(ctr), img['name']) for ctr, img in enumerate(images, start=1)]

def generate_meme(state):
    top_text = state.top_text.strip()
    bottom_text = state.bottom_text.strip()

    if not top_text or not bottom_text:
        notify(state, 'error', 'Both top and bottom text must be specified.')
        return

    URL = 'https://api.imgflip.com/caption_image'
    params = {
        'username': username,
        'password': password,
        'template_id': images[int(state.meme_template[0]) - 1]['id'],
        'text0': top_text,
        'text1': bottom_text
    }

    response = requests.request('POST', URL, params=params).json()

    if 'data' in response:
        notify(state, 'success', f'meme successfully generated!')

        # Save the meme URL
        meme_url = response['data']['url']
        state.meme_download = meme_url

        # Display the meme image
        response = requests.get(meme_url)
        state.meme_image = response.content
    else:
        notify(state, 'error', f'Failed to generate meme: {response.get("error_message", "Unknown error")}')

def download_meme(state):
    if state.meme_download:
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', userAgent)
        file_path = images[int(state.meme_template[0]) - 1]['name'] + '.jpg'
        opener.retrieve(state.meme_download, file_path)
        return file_path

# Definition of the page
page="""
<|layout|columns=300px 1|
<|part|render=True|class_name=sidebar|
# Meme **Magic**{: .color-primary}
Select Character Image: <|{meme_template}|selector|lov={memes}|dropdown|>
Top Text: <|{top_text}|input|><br />
Bottom Text: <|{bottom_text}|input|><br />
<|Generate Meme|button|class_name=plain|on_action=generate_meme|> 
|>

<|part|render=True|class_name=p2 align-item-center|
<|{meme_image}|image|active={meme_download is not None}|> <br />
<|{meme_download}|file_download|label=Download Meme|active={meme_download is not None}|>
|>
|>
"""

Gui(page).run(debug=True, dark_mode=False)