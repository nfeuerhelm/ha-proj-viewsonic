import socket
import time

CMD_LIST = {
    "on": b'\x06\x14\x00\x04\x00\x34\x11\x00\x00\x5D',
    "off": b'\x06\x14\x00\x04\x00\x34\x11\x01\x00\x5E',
    "pwr?": b'\x07\x14\x00\x05\x00\x34\x00\x00\x11\x00\x5E',
}
STATUS_LIST = {
    b'\x03\x14\x00\x00\x00\x14': 'cmd_ack',
    b'\x05\x14\x00\x03\x00\x00\x00\x01\x18': 'pwr_on',
    b'\x05\x14\x00\x03\x00\x00\x00\x00\x17': 'pwr_off',
    b'\x05\x14\x00\x03\x00\x00\x00\x02\x19': 'pwr_warming',
    b'\x05\x14\x00\x03\x00\x00\x00\x03\x1A': 'pwr_cooling'
}

# def tcp_client(host: str, port: int, message: bytes, buffer_size: int = 1024, timeout: float = 2.0):
#     """
#     Establishes a TCP connection, sends a message, receives a response, and prints it.
    
#     :param host: The target server address.
#     :param port: The target server port.
#     :param message: The message to send as a byte string.
#     :param buffer_size: The size of the buffer for receiving data.
#     """
#     try:
#         with socket.create_connection((host, port), timeout=timeout) as sock:
#             print(f"Connected to {host}:{port}")
#             sock.sendall(message)
#             response = sock.recv(buffer_size)
#             output = STATUS_LIST.get(response, response)
#             print(f"Response: {output}")
#     except Exception as e:
#         print(f"Error: {e}")

def connect(host: str, port: int, timeout: float = 2.0):
    """
    Establishes a TCP connection.
    
    :param host: The target server address.
    :param port: The target server port.
    :param timeout: The timeout for the connection in seconds.
    :return: The connected socket object.
    """
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        print(f"Connected to {host}:{port}")
        return sock
    except Exception as e:
        print(f"Error connecting: {e}")
        return None

def send_message(sock: socket.socket, message: bytes, buffer_size: int = 1024):
    """
    Sends a message and receives a response.
    
    :param sock: The connected socket object.
    :param message: The message to send as a byte string.
    :param buffer_size: The size of the buffer for receiving data.
    """
    try:
        sock.sendall(message)
        response = sock.recv(buffer_size)
        output = STATUS_LIST.get(response, response)
        print(f"Response: {output}")
        return output
    except Exception as e:
        print(f"Error sending message: {e}")

def disconnect(sock: socket.socket):
    """
    Closes the TCP connection.
    
    :param sock: The connected socket object.
    """
    try:
        sock.close()
        print("Disconnected")
    except Exception as e:
        print(f"Error disconnecting: {e}")

def check_pwr_status(sock):
    print('Power Status...')
    rtn = send_message(sock, CMD_LIST['pwr?'])
    time.sleep(2)
    return rtn

def pwr_on(sock):
    print('Powering On...')
    send_message(sock, CMD_LIST['on'])

def pwr_off(sock):
    print('Powering Off...')
    send_message(sock, CMD_LIST['off'])

if __name__ == "__main__":
    HOST = "192.168.2.117"  # Change to target IP
    PORT = 4661  # Change to target port
    
    sock = connect(HOST, PORT, timeout=30)

    if sock:
        check_pwr_status(sock)

        pwr_on(sock)

        for i in range(30):
            print(f'Checking: {i}')
            out = check_pwr_status(sock)
            if out == 'pwr_on':
                break

        pwr_off(sock)

        for i in range(30):
            print(f'Checking: {i}')
            out = check_pwr_status(sock)
            if out == 'pwr_off':
                break

        disconnect(sock)
