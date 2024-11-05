from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# A dictionary to store usernames and passwords (for demonstration purposes)
user_credentials = {
    "user1": "password1",
    "user2": "password2",
}

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    """Handles a single client connection."""
    
    # Authentication loop
    while True:
        client.send(bytes("Enter username: ", "utf8"))
        username = client.recv(BUFSIZ).decode("utf8")
        client.send(bytes("Enter password: ", "utf8"))
        password = client.recv(BUFSIZ).decode("utf8")

        # Check credentials
        if username in user_credentials and user_credentials[username] == password:
            break
        else:
            client.send(bytes("Invalid credentials, please try again.", "utf8"))

    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % username
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % username
    broadcast(bytes(msg, "utf8"))
    clients[client] = username

    while True:
        try:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, username + ": ")
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                broadcast(bytes("%s has left the chat." % username, "utf8"))
                break
        except Exception as e:
            print(f"Error handling client: {e}")
            break

def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients."""
    for sock in clients:
        try:
            sock.send(bytes(prefix, "utf8") + msg)
        except Exception as e:
            print(f"Error broadcasting message: {e}")

clients = {}
HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()