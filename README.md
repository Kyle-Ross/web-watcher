# web-watcher
A python script which checks a target URL for a given string at a specified interval, then providing one of a selection of alert types. Useful for watching for stock updates in online stores, or any other html changes that can be detected with a basic string match.

## How-to use

1. Clone this repo
2. Install required libraries. It is recommended to install `pip install playsound==1.2.2` as later versions appear to have issues playing mp3 files.
3. At bottom of `Main.py` script adjust the function call with desired settings:

``` Python
open_and_refresh(
    url=target_url,  # URL to check
    headless_mode=True,  # True or False - False if you want to see the browser window
    success_type='string not found',  # 'string not found' or 'string found'
    refresh_interval=30,  # How often to recheck the page in seconds
    check_string='Stock is empty',  # The string to check the html for
    alert_type='popup',  # 'tts', 'mp3' or 'popup'
    mp3_path=alert_sound_audio)  # path of mp3 audio file to play - OPTIONAL
```

4. Run the script - you will be alerted when either the string is or is not found on the target URL

## Alert Types

All alert types print details to console, but do other actions.

### tts - Text to Speech

Reads out the success message.

### mp3

Plays the chosen mp3 file.

### popup

Shows the success message as a windows popup and plays the generic windows alert sound.