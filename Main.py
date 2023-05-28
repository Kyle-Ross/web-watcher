from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from playsound import playsound
import time
import pyttsx3
import sys
import os
import ctypes
import winsound


# Returns true if file path exists
def is_valid_path(path):
    return os.path.exists(path)


# Check file path and exit with message if invalid
def invalid_path_exit(path):
    if not is_valid_path(path):
        print(f"'{path}' is invalid, ending script")
        sys.exit()


# Function for generating text-to-speech
def text_to_speech(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Convert text to speech
    engine.say(text)
    engine.runAndWait()


# Function for generating a windows popup
def show_popup(text):
    # Get the file name of the script
    script_file = os.path.basename(__file__)
    # Generate the popup
    ctypes.windll.user32.MessageBoxW(0, text, script_file, 0)


# Checks a target url for a string at a given interval and runs specified alert behaviour
def open_and_refresh(url, headless_mode, success_type, refresh_interval, check_string, alert_type, mp3_path=''):
    # Prep webdriver
    if headless_mode:  # Don't show the browser window
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Make the browser run in headless mode
        driver = webdriver.Chrome(options=chrome_options)  # Pass the options when creating the webdriver
    else:  # Do show the browser window
        driver = webdriver.Chrome()

    driver.get(url)

    # Core loop
    while True:
        # Wait and print message per second to console based on refresh interval
        for i in range(refresh_interval, 0, -1):
            print(f"Refreshing in {i} seconds...")
            time.sleep(1)
        print("Refreshing now!")
        driver.refresh()

        # Get the page source as a string
        html = driver.page_source

        # Function to run conditional alert behaviour
        def alert(append_string):
            # Function to make string for messages
            def message_string(message_type):
                output_string = f"Target URL: '{url}'\n" \
                                f"Check string: '{check_string}'\n" \
                                f"Success Type: {success_type}\n" \
                                f"Alert Type: '{message_type}'\n" \
                                f"Result / Action: '{append_string}"
                return output_string

            # Generate that string
            alert_message_string = message_string(alert_type)

            # For text to speech
            if alert_type == 'tts':
                print(alert_message_string)
                text_to_speech(alert_message_string)
            # For mp3
            elif alert_type == 'mp3':
                print(alert_message_string)
                invalid_path_exit(mp3_path)
                playsound(mp3_path)
            elif alert_type == 'popup':
                print(alert_message_string)
                winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)
                show_popup(alert_message_string)
            # If no valid option was selected
            else:
                print("Choose 'tts' or 'mps' for var alert_type")
                sys.exit()

        # Actions to take if success_type is 'not in'. i.e. script ends if string is NOT found
        if success_type == 'string not found':
            if check_string in html:
                print(f"'{check_string}' string still found - repeating loop")
            else:
                alert('SUCCESS: string not found - breaking loop')
                break

        # Actions to take if success_type is 'in'. i.e. script ends if string IS found
        if success_type == 'string found':
            if check_string in html:
                alert('SUCCESS: string found - breaking loop')
                break
            else:
                print(f"'{check_string}' string not found - repeating loop")


# Path definition
target_url = "https://example.com.au/collections/product-in-stock"
alert_sound_audio = r"C:\Users\kylec\Audio\alert_sound.mp3"

# Running the function
open_and_refresh(
    url=target_url,  # URL to check
    headless_mode=True,  # True or False - False if you want to see the browser window
    success_type='string not found',  # 'string not found' or 'string found'
    refresh_interval=30,  # How often to recheck the page in seconds
    check_string='Stock is empty',  # The string to check the html for
    alert_type='popup',  # 'tts', 'mp3' or 'popup'
    mp3_path=alert_sound_audio)  # path of mp3 audio file to play - OPTIONAL
