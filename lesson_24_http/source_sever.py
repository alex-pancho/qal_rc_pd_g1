import socket

server = socket.socket(
    socket.AF_INET, # IPv4
    socket.SOCK_STREAM, # TCP
    # socket.SOCK_DGRAM  # UDP
)

server.bind(("127.0.0.1", 80))

server.listen()

print("Server started")

response = """
HTTP/1.1 200 OK

<body>
<h1>Hello from Python server</h1>
</body>
"""

while True:
# дозвіл вх повідомлень
    client, address = server.accept()
    # 
    message = client.recv(4096)

    print(message.decode())

    client.send(response.encode())
    client.close()
# server.close()

# python -m http.server 8000

# 192.168.0.5 - comp
# 192.168.0.1 - router
