# IMPORTANTE: Desactivar Firewall antes de correr el script de servidor (Por lo menos en Windows, script no probado en Linux)

import socket
from datetime import datetime

HOST = '0.0.0.0'
PORT = 65432 # Pueden cambiar el numero del port si no les deja usarlo
LOG_FILE = 'servidor_conexiones.log'

def registrar_log(mensaje):
    """Escribe un mensaje en la consola y en el archivo log con el formato YYYY/MM/DD;HH:MM:SS;Mensaje"""
    ahora = datetime.now()
    fecha_hora = ahora.strftime("%Y/%m/%d;%H:%M:%S")
    registro = f"{fecha_hora};{mensaje}"
    
    # Imprimir en consola
    print(registro)
    
    # Guardar en el archivo .log (modo 'a' para agregar al final sin sobrescribir)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(registro + '\n')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea el socket del servidor para la comunicación TCP

# Permite reutilizar la dirección del puerto inmediatamente sin esperar a TIME_WAIT
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen()

# Permite al servidor finalizar su operación con CTRL + C (1)
server_socket.settimeout(1.0)

registrar_log(f"Servidor permanentemente escuchando en el puerto {PORT}")

try:
    while True:
        try: 
            client_socket, client_address = server_socket.accept()
        except socket.timeout: # Permite al servidor finalizar su operación con CTRL + C (2)
            continue
        client_socket.settimeout(None)
        
        ip_cliente = client_address[0]
        
        # Registro de conexión establecida
        registrar_log(f"Conexión recibida desde {ip_cliente}")
        
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    # El cliente cerró la conexión ordenadamente
                    registrar_log(f"El cliente {ip_cliente} cerró la conexión")
                    break
                
                mensaje = data.decode('utf-8')
                registrar_log(f"Mensaje recibido de {ip_cliente}: {mensaje}")
                
                # Responder al cliente
                client_socket.sendall(b"Mensaje recibido correctamente")
                
        except ConnectionResetError:
            registrar_log(f"El cliente {ip_cliente} se desconectó abruptamente")
            
        finally:
            client_socket.close()
            registrar_log(f"Conexión finalizada con {ip_cliente}. Esperando a un nuevo cliente...")

except KeyboardInterrupt:
    registrar_log("Servidor detenido manualmente con Ctrl+C")
finally:
    server_socket.close()
    registrar_log("Socket principal del servidor cerrado")