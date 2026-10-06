import socket

HOST = '0.0.0.0'
PORT = 65432

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permite reutilizar la dirección del puerto inmediatamente sin esperar a TIME_WAIT
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"[*] Servidor permanentemente escuchando en el puerto {PORT}...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"[+] Cliente conectado desde: {client_address}")
    
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Mensaje recibido: {data.decode('utf-8')}")
            client_socket.sendall(b"Mensaje recibido correctamente")
    except ConnectionResetError:
        print("[-] El cliente se desconectó abruptamente.")
    finally:
        client_socket.close()
        print("[*] Esperando a un nuevo cliente...")