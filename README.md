## Meme Magic 😍: Building a Custom Meme Generator with Python

In this article, we'll create a Meme Generator app, a web-based tool for creating custom memes. The app is built using the Taipy GUI library, which provides a simple and intuitive way to create interactive web interfaces. We'll explore the app's features and functionality, as well as the underlying code and design principles. let's get started!

![meme_gen](https://github.com/jrshittu/build_with_taipy/assets/110542235/baa87481-757d-4eb1-b8cb-e7106f775cc8)

## Contents
[Say Hello Taipy](#hi)

[Create a meme generator with TaipyGUI](#create)

[Bonus Tips: Improve the Layout](#bonus)

[Hosting on Taipy Cloud](#host)

[Conclusion](#conc)



## Say Hello Taipy! <a name="hi"></a>
Taipy is a Python open-source library that makes it simple to create data-driven web applications. It takes care of both the visible part(Frontend) and the behind-the-scenes(Backend) operations. Its goal is to speed up the process of developing applications, from the early design stages to having a fully functional product ready for use.

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k24u6ko4tkjffice6thz.gif)

Source: [Taipy Docs](https://docs.taipy.io/en/latest/)

**Requirement:** Python 3.8 or later on Linux, Windows, and Mac. 

**Installing Taipy:** Open up a terminal and run the following command, which will install Taipy with all its dependencies.

```bash
pip install taipy
```
We're set, let say hello to Taipy...

```python
# import the library
from taipy import Gui

page = "# Hello Taipy!" 

# run the gui
Gui(page).run()
```

Save the code as a Python file: e.g., `hi_taipy.py`. 
Run the code and wait for the client link `http://127.0.0.1:5000` to display and pop up in your browser. 
You can change the port if you want to run multiple servers at the same time with `Gui(...).run(port=xxxx)`.

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/6w2h2jryumg8kumid3ms.PNG)


## Create a meme generator with TaipyGUI: <a name="create"></a>
Since we are familiar with Taipy, Let's get our hands dirty and build our meme generator. 

**Step 1:** Import the required libraries
```python
# Import taipy library
from taipy.gui import Gui, notify
import requests
import urllib
```
**Step 2:** Navigate to [imgflip](https://imgflip.com/) to create an account, set the username and password. After then navigate to [Google](www.google.com) to search for `my user agent`, copy and set your username and password from [imgflip](https://imgflip.com/), then copy and paste your userAgent from the google search result.
```python
username = "your_own_username" 
password = "your_own_password"
userAgent = "your_own_userAgent"
```
**Step 3:** Fetch the available meme templates from the Imgflip API using a GET request and store the relevant information (name, URL, and ID) in a list of dictionaries called 'images'
```python
# Fetch the available memes
data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]
```
**Step 4:** Initialize empty variables for storing the selected meme template, top and bottom text, and the generated meme
```python
meme_template = ""
top_text = ""
bottom_text = ""
meme_download = None
meme_image = None
```
**Step 5**: Create a list of tuples called 'memes' containing the index and name of each meme template for use in the dropdown selector
```python
memes = [(str(ctr), img['name']) for ctr, img in enumerate(images, start=1)]
```
**Step 6**: Define a function called 'generate\_meme' that takes a 'state' object as an argument, which contains the user input for the meme template, top and bottom text. The function uses the Imgflip API to generate a meme using the provided inputs and stores the generated meme URL and image in the 'meme\_download' and 'meme\_image' variables respectively.
```python
def generate_meme(state):
    # Get the top and bottom text entered by the user and remove any leading/trailing whitespace
    top_text = state.top_text.strip()
    bottom_text = state.bottom_text.strip()

    # Check if both top and bottom text are specified
    if not top_text or not bottom_text:
        # Notify the user that both top and bottom text must be specified
        notify(state, 'error', 'Both top and bottom text must be specified.')
        # Return from the function without generating a meme
        return

    # Set up the API endpoint URL for generating a meme
    URL = 'https://api.imgflip.com/caption_image'

    # Set up the parameters for the API request
    params = {
        'username': username,    # The username for the Imgflip account
        'password': password,    # The password for the Imgflip account
        'template_id': images[int(state.meme_template[0]) - 1]['id'],    # The ID of the selected meme template
        'text0': top_text,        # The top text entered by the user
        'text1': bottom_text     # The bottom text entered by the user
    }

    # Send a POST request to the API endpoint with the specified parameters
    response = requests.request('POST', URL, params=params).json()

    # Check if the API response contains a 'data' key, indicating that the meme was successfully generated
    if 'data' in response:
        # Notify the user that the meme was successfully generated
        notify(state, 'success', f'meme successfully generated!')

        # Save the URL of the generated meme
        meme_url = response['data']['url']
        state.meme_download = meme_url

        # Display the generated meme image
        response = requests.get(meme_url)
        state.meme_image = response.content
    else:
        # Notify the user that the meme generation failed and provide an error message if available
        notify(state, 'error', f'Failed to generate meme: {response.get("error_message", "Unknown error")}')
```
**Step 7:** Define a function called 'download\_meme' that takes the 'state' object as an argument and downloads the generated meme image from the 'meme\_download' URL using the urllib library.
```python
def download_meme(state):
    if state.meme_download:
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', userAgent)
        file_path = images[int(state.meme_template[0]) - 1]['name'] + '.jpg'
        opener.retrieve(state.meme_download, file_path)
        return file_path
```
**Step 8:** Define the Taipy GUI page using the page string, which contains the user interface elements such as the dropdown selector, input fields, and buttons. The page string also specifies the event handlers for each UI element, such as the 'on\_action' event for the 'Generate Meme' button, which calls the 'generate\_meme' function.
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
**Step 9:** Run the Taipy GUI application using the 'Gui' object and passing the 'page' string to its constructor. The 'run' method starts the application.
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

## Bonus Tips: Improve the Layout <a name="bonus"></a>
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
## Hosting on Taipy Cloud <a name="host"></a>
Navigate to [Taipy Cloud](https://cloud.taipy.io/) and create a free account.

https://github.com/jrshittu/meme_magic/assets/110542235/8e81eee7-026d-46aa-89e0-8f69e3667899

To deploy the app to [Taipy Cloud](https://cloud.taipy.io/), follow these steps:

1. Connect to Taipy Cloud and sign in to your account.
2. Click on the "Add Machine" button to create a new machine. Fill in the required fields, such as the machine name and the desired size.
3. Select the machine that you just created and click on the "Add App" button to create a new app.
4. Zip the `main.py` and `requirements.txt` files for your app and upload the zip file to the "App Files" field.
5. Fill in the other required fields for the app, such as the app name and the entry point.
6. Press the "Deploy App" button to deploy the app to Taipy Cloud.

## Conclusion <a name="conc"></a>
In this article, we learned how to build a custom meme generator using Python and the Taipy GUI library. We explored the features and functionality of the app and walked through the code and design principles. With Taipy, we were able to create an interactive web interface for our meme generator that is both simple and intuitive. We also discussed how to improve the layout of the app and host it on Taipy Cloud. Overall, Taipy provides a powerful and easy-to-use tool for building data-driven web applications.
