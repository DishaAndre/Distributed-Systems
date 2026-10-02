import socket

HOST = "127.0.0.1"
PORT = 5000

# Create client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client.connect((HOST, PORT))

# Send message
message = input("Enter Message: ")

client.send(message.encode())

# Receive reply
reply = client.recv(1024).decode()

print("Server says:", reply)

# Close connection
client.close()
