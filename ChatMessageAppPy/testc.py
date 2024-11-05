from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()  # This will send the quit message to the server.

def quit_chat():
    """Gracefully quit the chat."""
    my_msg.set("{quit}")
    send()  # Send the quit message to the server.

# Create the main window
top = tkinter.Tk()
top.title("Chat On!")

# Get user credentials
username = input("Enter username: ")
password = input("Enter password: ")

# Socket part
HOST = input('Enter host: ')  # Enter host of the server without inverted commas 
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

# Send credentials to the server
client_socket.send(bytes(username, "utf8"))
client_socket.send(bytes(password, "utf8"))

# Create the GUI
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To see through previous messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()

send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

# Add a Quit button
quit_button = tkinter.Button(top, text="Quit", command=quit_chat)
quit_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # for start of GUI