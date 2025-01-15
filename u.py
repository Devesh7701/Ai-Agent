import pyautogui
import time

# Function to send message on WhatsApp Desktop
def send_whatsapp_message(contact_name, message, repeat=1):
    time.sleep(5)
    
    # Open the WhatsApp search bar (assumes WhatsApp is in focus)
    # pyautogui.hotkey('command', 'f')  # Mac shortcut to search in WhatsApp

    # Type the contact's name
    # pyautogui.typewrite(contact_name)
    # time.sleep(1)  # Wait for search results to appear

    # Press Enter to select the contact
    # pyautogui.press('enter')
    # time.sleep(2)  # Wait for the chat to open

    # Type and send the message
    for _ in range(repeat):
        pyautogui.typewrite(message)
        pyautogui.press('enter')
        time.sleep(0.0001)  # Wait between messages

# Example usage
contact_name = ""  # The contact's name in your WhatsApp
message = "hi"
send_whatsapp_message(contact_name, message, repeat=100)
