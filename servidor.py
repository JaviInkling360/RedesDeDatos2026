import socket
from datetime import datetime

HOST = '0.0.0.0'
PORT = 65432 # Pueden cambiar el numero del port si no les deja usarlo

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permite reutilizar la dirección del puerto inmediatamente sin esperar a TIME_WAIT
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"[*] Servidor permanentemente escuchando en el puerto {PORT}...")

while True:
    client_socket, client_address = server_socket.accept()
    ahora = datetime.now()
    fecha_hora = ahora.strftime("%Y/%m/%d;%H:%M:%S")
    ip_cliente = client_address[0]
    print(f"{fecha_hora};Conexión recibida desde {ip_cliente}")
    
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