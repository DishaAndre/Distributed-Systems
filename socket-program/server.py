import socket

HOST = "127.0.0.1"
PORT = 5000

# Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind server to IP and port
server.bind((HOST, PORT))

# Start listening
server.listen(1)

print(" Server Started Successfully")
print(" Waiting for Client...")

# Accept client connection
conn, addr = server.accept()

print(f"Connected to Client: {addr}")

# Receive message
message = conn.recv(1024).decode()

print("Client says:", message)

# Send reply
reply = input("Enter Reply: ")

conn.send(reply.encode())

# Close connection
conn.close()
server.close()
