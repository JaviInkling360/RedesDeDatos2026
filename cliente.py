import socket

# Dirección IP de la computadora Servidor
SERVER_IP = '127.0.0.1'  # <--- CAMBIA ESTO por la IP de tu servidor
PORT = 60000

# Crear el socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conectarse al servidor
    client_socket.connect((SERVER_IP, PORT))
    print("[+] Conectado exitosamente al servidor.")

    while True:
        mensaje = input("Escribe un mensaje para el servidor (o 'salir'): ")
        if mensaje.lower() == 'salir':
            break
        
        # Enviar mensaje al servidor
        client_socket.sendall(mensaje.encode('utf-8'))
        
        # Recibir respuesta del servidor
        respuesta = client_socket.recv(1024)
        print(f"Respuesta del servidor: {respuesta.decode('utf-8')}")

finally:
    client_socket.close()
    print("[-] Desconectado del servidor.")
