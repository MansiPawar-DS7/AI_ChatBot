import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar
from Final_ChatBot import get_most_similar_query, response_dict  # Import chatbot logic

# Function to create a bordered message box
def create_message(text, sender="user"):
    # Create a Frame for the message box
    frame = tk.Frame(chat_frame, bd=2, relief="solid", padx=10, pady=5, 
                     bg="#ecf0f1" if sender == "user" else "#34495e")

    # Align messages: Right for user, Left for bot
    frame.pack(fill="none", pady=5, anchor="e" if sender == "user" else "w")

    # Create a Label inside the Frame for displaying the text
    label = tk.Label(frame, text=text, font=("Arial", 12), wraplength=300, justify="left",
                     bg="#ecf0f1" if sender == "user" else "#34495e", 
                     fg="black" if sender == "user" else "white", padx=5, pady=3)
    label.pack()

    # Efficiently update scroll region and auto-scroll
    chat_canvas.update_idletasks()
    chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
    chat_canvas.yview_moveto(1.0)  # Auto-scroll

    return frame  # Return frame for removal of "typing..."

# Function to handle user input and display chatbot response
def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return  # Ignore empty input

    # Create user message
    create_message(f"You: {user_input}", sender="user")
    entry.delete(0, tk.END)  # Clear input field

    # Simulate "typing..." message (without UI freeze)
    typing_label = create_message("ChatBot: typing...", sender="bot")
    root.after(500, lambda: process_response(typing_label, user_input))  # Add delay before response

# Process chatbot response after delay
def process_response(typing_label, user_input):
    # Get chatbot response
    matched_query, similarity = get_most_similar_query(user_input)
    response = response_dict.get(matched_query, "Sorry...I didn't get it.") if similarity > 0.7 else "Sorry...I didn't get it."

    # Remove "typing..." message and insert actual response
    typing_label.destroy()
    create_message(f"ChatBot: {response}", sender="bot")

    # Close chat on exit message
    if response == "Goodbye...Have a great day! :)":
        root.after(2000, root.quit)

# Creating GUI Window
root = tk.Tk()
root.title("ChatBot")
root.geometry("500x600")
root.config(bg="#5e86ad")

# ================= Scrollable Chat Window ================= #
chat_window = tk.Frame(root, bg="#f0f0f0")
chat_window.pack(fill="both", expand=True, padx=10, pady=10)

chat_canvas = Canvas(chat_window, bg="#f0f0f0")
chat_canvas.pack(side="left", fill="both", expand=True)

scrollbar = Scrollbar(chat_window, orient="vertical", command=chat_canvas.yview)
scrollbar.pack(side="right", fill="y")

chat_canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold chat messages
chat_frame = Frame(chat_canvas, bg="#f0f0f0")
chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")

# ================= Input Field & Send Button ================= #
bottom_frame = tk.Frame(root, bg="#5e86ad")
bottom_frame.pack(fill="x", padx=10, pady=5)

entry = tk.Entry(bottom_frame, width=40, font=("Arial", 12), relief="solid", bd=2)
entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")
entry.bind("<Return>", lambda event: send_message())

def on_enter(event):
    send_button.config(bg="#00FF00", fg="white")

def on_leave(event):
    send_button.config(bg="lightgreen", fg="black")

send_button = tk.Button(bottom_frame, text="Send", command=send_message, font=("Arial", 12, "bold"), 
                        bg="#549fb8", relief="solid", width=10, height=2)
send_button.pack(side="right", padx=10, pady=5)
send_button.bind("<Enter>", on_enter)
send_button.bind("<Leave>", on_leave)

# Run the Tkinter event loop
root.mainloop()
