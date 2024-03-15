## Meme Magic 😍: Building a Custom Meme Generator with Python

In this article, we'll create a Meme Generator app, a web-based tool for creating custom memes. The app is built using the Taipy GUI library, which provides a simple and intuitive way to create interactive web interfaces. We'll explore the app's features and functionality, as well as the underlying code and design principles. let's get started!

![meme_gen](https://github.com/jrshittu/build_with_taipy/assets/110542235/baa87481-757d-4eb1-b8cb-e7106f775cc8)

Step 1: Import the required libraries
```python
# Import taipy library
from taipy.gui import Gui, notify
import requests
import urllib
```
Step 2: Navigate to [imgflip](https://imgflip.com/) to create an account, set the username and password. After then navigate to [Google](www.google.com) to search for `my user agent`, copy and set the variables.
```python
username = "AbideenTunde"
password = "2nhnUFx@bmbs4Jf"
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
```
Step 3: Fetch the available meme templates from the Imgflip API using a GET request and store the relevant information (name, URL, and ID) in a list of dictionaries called 'images'
```python
# Fetch the available memes
data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]
```
Step 4: Initialize empty variables for storing the selected meme template, top and bottom text, and the generated meme
```python
meme_template = ""
top_text = ""
bottom_text = ""
meme_download = None
meme_image = None
```
Step 5: Create a list of tuples called 'memes' containing the index and name of each meme template for use in the dropdown selector
```python
memes = [(str(ctr), img['name']) for ctr, img in enumerate(images, start=1)]
```
Step 6: Define a function called 'generate\_meme' that takes a 'state' object as an argument, which contains the user input for the meme template, top and bottom text. The function uses the Imgflip API to generate a meme using the provided inputs and stores the generated meme URL and image in the 'meme\_download' and 'meme\_image' variables respectively.
```python
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
```
Step 7: Define a function called 'download\_meme' that takes the 'state' object as an argument and downloads the generated meme image from the 'meme\_download' URL using the urllib library.
```python
def download_meme(state):
    if state.meme_download:
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', userAgent)
        file_path = images[int(state.meme_template[0]) - 1]['name'] + '.jpg'
        opener.retrieve(state.meme_download, file_path)
        return file_path
```
Step 8: Define the Taipy GUI page using the page string, which contains the user interface elements such as the dropdown selector, input fields, and buttons. The page string also specifies the event handlers for each UI element, such as the 'on\_action' event for the 'Generate Meme' button, which calls the 'generate\_meme' function.
```python
# Definition of the page
page = """
# Meme Generator! {: .color-primary}
Select Character Image: <|{meme_template}|selector|lov={memes}|dropdown|>
Top Text: <|{top_text}|input|><br />
Bottom Text: <|{bottom_text}|input|><br />
<|Generate Meme|button|class_name=plain|on_action=generate_meme|> 
<|{meme_download}|file_download|label=Download Meme|active={meme_download is not None}|><br />
<|{meme_image}|image|active={meme_download is not None}|>
"""
```
Step 9: Run the Taipy GUI application using the 'Gui' object and passing the 'page' string to its constructor. The 'run' method starts the application.
```python
Gui(page).run(debug=True)
```

**Full Code**
```python
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
page = """
# Meme Generator! {: .color-primary}
Select Character Image: <|{meme_template}|selector|lov={memes}|dropdown|>
Top Text: <|{top_text}|input|><br />
Bottom Text: <|{bottom_text}|input|><br />
<|Generate Meme|button|class_name=plain|on_action=generate_meme|> 
<|{meme_download}|file_download|label=Download Meme|active={meme_download is not None}|><br />
<|{meme_image}|image|active={meme_download is not None}|>
"""

Gui(page).run(debug=True)
```

## Bonus Tips: Improve the Layout
![meme magic](https://github.com/jrshittu/build_with_taipy/assets/110542235/6a494f75-6134-49e5-a0c3-5282a7337f6a)

Click [here](https://tunde.taipy.cloud/) to try the app.

Define the layout of the user interface for the Meme Generator app. Now we have two columns: a sidebar with a width of 300 pixels, and a main content area.

```python
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
```
### Hosting on Taipy Cloud
Navigate to [Taipy Cloud](https://cloud.taipy.io/) and create a free account. Then follow the instructions in the clip below to host your app.

https://github.com/jrshittu/meme_magic/assets/110542235/8e81eee7-026d-46aa-89e0-8f69e3667899
