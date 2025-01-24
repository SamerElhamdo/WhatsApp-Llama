import json
import os
import sys

def remove_placeholders(message):
    # Skip messages with these placeholders
    skip_list = ['<This message was edited>', 'This message was deleted.', ' omitted\n', '‎audio omitted', '‎image omitted', '‎video omitted', 'Contact card omitted', '‎Missed video call']
    for phrase in skip_list:
        if phrase in message:
            return True
    return False

def replace_users(message, contact_name, friend_name, bot_name, your_contact_name):
    # Replace names in the message
    message = message.replace(your_contact_name, bot_name)
    message = message.replace(contact_name, friend_name)
    return message

def remove_links(message):
    # Remove links from the message
    while "http" in message:
        start = message.find("http")
        end = message.find(" ", start)
        if end == -1:
            message = message[:start]
        else:
            message = message[:start] + message[end:]
    return message

def get_user_text(message):
    # Extract user and message text
    if ': ' not in message:
        return None, message
    user, text = message.split(": ", 1)
    return user, text

def clean_text(text):
    # Clean any leading/trailing spaces from the text
    return text.strip()

def collate_messages(messages, user_name, bot_name, friend_name):
    conversations = []
    snippet = ''

    for message in messages:
        user, text = get_user_text(message)
        if user is None:
            continue
        cleaned_text = clean_text(text)
        if user == user_name:
            conversations.append({friend_name: cleaned_text})
        elif user == bot_name:
            conversations.append({bot_name: cleaned_text})

    return conversations

def remove_timestamp(message):
    # Remove timestamp (split based on ']' character and return message part after it)
    parts = message.split("]")  # Split at the timestamp ending (i.e., ']')
    if len(parts) > 1:
        return parts[1].strip()  # Return the part after the timestamp
    return message.strip()

def should_ignore_message(message):
    # Skip messages containing "Voice call" or "Missed voice call"
    ignore_phrases = ["Voice call", "Missed voice call"]
    for phrase in ignore_phrases:
        if phrase in message:
            return True
    return False

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: preprocessing.py <your_name> <your_contact_name> <friend_name> <friend_contact_name> <input_folder_path> <output_folder_path>")
        sys.exit(1)

    bot_name = sys.argv[1]
    your_contact_name = sys.argv[2]
    friend_name = sys.argv[3]
    contact_name = sys.argv[4]
    input_folder_path = sys.argv[5]
    output_folder_path = sys.argv[6]

    # Load file and print some sample lines to ensure correct loading
    with open(input_folder_path + '/' + friend_name + 'Chat.txt', encoding="utf-8") as f:
        lines = f.readlines()

    dataset = []

    # Process the lines and remove timestamps, placeholders, replace names, and ignore specific messages
    for line in lines:
        message = remove_timestamp(line)  # Remove timestamp

        if remove_placeholders(message):  # Skip placeholder messages
            continue

        if should_ignore_message(message):  # Skip messages containing "Voice call" or "Missed voice call"
            continue

        message = remove_links(message)  # Remove links
        message = replace_users(message, contact_name, friend_name, bot_name, your_contact_name)  # Replace names

        dataset.append(message)

    # Collate messages into a structured format
    dataset = collate_messages(dataset, friend_name, bot_name, friend_name)

    # Write the final data to a JSON file
    with open(output_folder_path + '/' + friend_name + 'Chat.json', 'w') as file:
        json.dump(dataset, file, ensure_ascii=False, indent=4)
        print(f"Data successfully written to {output_folder_path + '/' + friend_name + 'Chat.json'}")
