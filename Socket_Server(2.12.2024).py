import socket
import threading
import os
import sys
import logging

sys.stdout.reconfigure(encoding='utf-8')

# Set up log
LOG_FILE = "server.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=
    [
        logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8"),  # Ghi log ra file
        logging.StreamHandler(sys.stdout)  # Hiển thị log ra console
    ]
)

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"
STORAGE_DIR = "./ServerCloud"
os.makedirs(STORAGE_DIR, exist_ok=True)

# Xử lý lệnh tải xuống
def handle_download(conn, filename):
    filepath = os.path.join(STORAGE_DIR, filename)
    
    if not os.path.basename(filename) == filename:
        conn.sendall(b"INVALID_FILENAME")
        return

    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath)
        conn.sendall(f"EXISTS {file_size}".encode(FORMAT))
        with open(filepath, "rb") as f:
            while chunk := f.read(1024):
                conn.sendall(chunk)
        conn.sendall(b"END")
        logging.info(f"'{filename}' sent to client.")
    else:
        conn.sendall(b"NOT_FOUND")
        logging.warning(f"File '{filename}' not found for client.")

# Xử lý lệnh upload
def handle_upload(conn, filename):
    filepath = os.path.join(STORAGE_DIR, filename)
    
    if not os.path.basename(filename) == filename:
        conn.sendall(b"INVALID_FILENAME")
        logging.warning(f"Client attempted invalid filename: {filename}")
        return

    conn.sendall(b"READY")
    with open(filepath, "wb") as f:
        logging.info(f"Receiving file '{filename}' from client...")
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            f.write(chunk)
            logging.info(f"Received {len(chunk)} bytes.")

    logging.info(f"File '{filename}' saved to '{filepath}'.")

# Xử lý lệnh liệt kê tệp
def handle_list_files(conn):
    files = os.listdir(STORAGE_DIR)
    if files:
        file_list = "\n".join(files)
        conn.sendall(f"FILES\n{file_list}".encode(FORMAT))
        logging.info(f"Sent file list to client.")
    else:
        conn.sendall(b"NO_FILES")
        logging.info(f"No files available in the storage directory.")

# xử lý client
def handle_client(conn: socket.socket, addr):
    logging.info(f"Connected to client: {addr}")
    try:
        while True:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break
            logging.info(f"Client {addr}: {msg}")

            if msg.startswith("download"):
                _, filename = msg.split(maxsplit=1)
                handle_download(conn, filename)
            elif msg.startswith("upload"):
                _, filename = msg.split(maxsplit=1)
                handle_upload(conn, filename)
            elif msg == "list":
                handle_list_files(conn)
            elif msg == "x":
                logging.info(f"Client {addr} disconnected.")
                break
            else:
                conn.sendall(b"INVALID_COMMAND")
                logging.warning(f"Error command: {msg}")

    except Exception as e:
        logging.error(f"Error while contacting with client {addr}: {e}")
    finally:
        conn.close()
        logging.info(f"Client {addr} closed.")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, SERVER_PORT))
        s.listen()
        logging.info(f"Server running at {HOST}:{SERVER_PORT}")

        while True:
            try:
                conn, addr = s.accept()
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
            except KeyboardInterrupt:
                logging.info("Server is off.")
                break

if __name__ == "__main__":
    main()