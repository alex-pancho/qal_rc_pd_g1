import socket

client = socket.socket(
    socket.AF_INET,
    #socket.SOCK_STREAM
    socket.SOCK_DGRAM  # UDP
)

client.connect(("127.0.0.1", 5000))

msg = "Привіт, сервер"

client.send(
    msg.encode("utf-8")
)

response = client.recv(1024)

print(response.decode())

client.close()