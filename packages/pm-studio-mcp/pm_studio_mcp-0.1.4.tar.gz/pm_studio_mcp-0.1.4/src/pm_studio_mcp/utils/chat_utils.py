import requests
from .auth import AuthUtils

class ChatUtils:
    """Utilities for accessing Microsoft Teams chat data via MS Graph API"""

    @staticmethod
    def get_group_chat_id_by_name(topic: str):
        """
        Get the group chat ID by filtering the topic. 
        
        Args:
            topic (str): The topic to filter the chat.
        
        Returns:
            str: The chat ID if found, otherwise None.
        """
        print("Retrieving group chat ID...")
            
        access_token = AuthUtils.login()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Get the list of chats
        chats_url = "https://graph.microsoft.com/v1.0/me/chats"
        chats_response = requests.get(chats_url, headers=headers)
        
        if chats_response.status_code != 200:
            print(f"Error retrieving chats: {chats_response.text}")
            return False
        
        # Check if the chat topic matches the provided topic
        for chat in chats_response.json().get("value", []):
            if  chat.get("topic") and topic in chat.get("topic", ""):
                chat_id = chat.get("id")
                print(chat_id)
                return chat_id
        
        return None

    def send_message_to_chat(chat_id: str, message: str):
        """
        Send a message to a chat in Microsoft Teams using MS Graph API.
        
        Args:
            chat_id (str): The ID of the chat to send the message to. If sending to myself, use "self".
            message (str): The message to send.
        
        Returns:
            dict: Dictionary containing status and response data
        """
        print("Sending message to chat...")
        
        # Ensure user is authenticated
        access_token = AuthUtils.login()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Create the chat message payload
        payload = {
            "body": {
                "content": "[PM Studio] " + message
                # to add "[PM Studio] " as a prefix to the note
            }
        }
        
        if chat_id is "sefl":
            endpoint = "https://graph.microsoft.com/v1.0/me/chats/48:notes/messages"
        else:
            endpoint = f"https://graph.microsoft.com/v1.0/me/chats/{chat_id}/messages"
        
        try:
            response = requests.post(url=endpoint, headers=headers, json=payload)
            
            if response.status_code == 201:
                return {
                    "status": "success",
                    "message": "Note sent successfully."
                }
            else:
                return {
                    "status": "error",
                    "message": f"Error sending note: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Error sending note: {str(e)}"
            }


    @staticmethod
    def send_to_myself(message: str):
        """
        Send a note to myself in Microsoft Teams using MS Graph API.
        
        Args:
            notes (str): The note to send.
        
        Returns:
            dict: Dictionary containing status and response data"""
        

        print("Sending note to myself in Microsoft Teams...")
        
        
        ChatUtils.send_message_to_chat("self", message)

    @staticmethod
    def send_to_group_chat(topic: str, message: str):
        """
        Send a note to a group chat in Microsoft Teams using MS Graph API.
        
        Args:
            topc (str): The topic to filter the chat.
            message (str): The note to send.
        
        Returns:
            dict: Dictionary containing status and response data
        """
        
        print("Sending note to group chat in Microsoft Teams...")
        
        chat_id = ChatUtils.get_group_chat_id_by_name(topic)
        
        if chat_id is None:
            print(f"Chat with topic '{topic}' not found.")
            return False
        
        # Send the message to the group chat
        response = ChatUtils.send_message_to_chat(chat_id, message)
        return response 