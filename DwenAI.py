import tkinter as tk
import requests

# Set the NovaAI API base URL and your API key
novaai_api_base = 'https://api.nova-oss.com/v1'
novaai_api_key = 'nv2-'

# Create the main window
root = tk.Tk()
root.title("DwenAI Chatbot V1.0")

# Create a frame for the chat history
chat_frame = tk.Frame(root)
chat_frame.pack(padx=10, pady=10)

# Create a scrollbar for the chat history
scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a text widget for displaying the chat history
chat_history = tk.Text(chat_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
chat_history.pack(fill=tk.BOTH)
scrollbar.config(command=chat_history.yview)

# Create an entry widget for user input
user_input = tk.Entry(root, font=("Helvetica", 14))
user_input.pack(padx=10, pady=10, fill=tk.BOTH)

def send_message():
    user_message = user_input.get()
    add_message("You", user_message)

    # Prepare the data to send to the API
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_message}]
    }

    # Define the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {novaai_api_key}"
    }

    # Send the POST request to the NovaAI API
    response = requests.post(f"{novaai_api_base}/chat/completions", json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        bot_response = result["choices"][0]["message"]["content"]
        add_message("DwenAI", bot_response)
    else:
        add_message("DwenAI", "Error communicating with the API")

    user_input.delete(0, tk.END)  # Clear the input field

def add_message(sender, message):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"{sender}: {message}\n\n")
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)

# Create a "Send" button
send_button = tk.Button(root, text="Send", command=send_message, font=("Helvetica", 14))
send_button.pack()

# Start the GUI
root.geometry("600x500")  # Set the initial window size
root.mainloop()
