import socket
import threading
import os
import sys
import logging
import time

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
    basename = os.path.basename(filename)
    filepath = os.path.join(STORAGE_DIR, basename)
    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath)
        conn.sendall(f"EXISTS {file_size}".encode(FORMAT))
        with open(filepath, "rb") as f:
            while chunk := f.read(1024):
                try:
                    conn.sendall(chunk)
                except socket.error:
                    logging.error(f"Mất kết nối từ client khi gửi tệp '{filename}'.")
                    return
        logging.info(f"Tệp '{filename}' đã được gửi tới client.")
    else:
        conn.sendall(b"NOT_FOUND")


# Xử lý lệnh upload
def handle_upload(conn, filename):
    basename = os.path.basename(filename)
    original_filepath = os.path.join(STORAGE_DIR, basename)
    if os.path.exists(original_filepath):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(basename)
        filename = f"{name}_{timestamp}{ext}"
        logging.info(f"File already exists. Renaming to '{filename}'.")

    conn.sendall(b"READY")
    filepath = os.path.join(STORAGE_DIR, filename)
    with open(filepath, "wb") as f:
        while True:
            try:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
            except socket.error:
                logging.error(f"Mất kết nối từ client khi tải lên '{filename}'.")
                return
    logging.info(f"Tệp '{filename}' đã được lưu tại '{filepath}'.")

def handle_client(conn: socket.socket, addr):
    logging.info(f"Connected to client: {addr}")
    try:
        while True:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break
            logging.info(f"Client {addr}: {msg}")

            if msg.startswith ("upload"):
                _, filename = msg.split(maxsplit=1)
                handle_upload(conn, filename)
            elif msg.startswith("download"):
                _, filename = msg.split(maxsplit=1)
                handle_download(conn, filename)
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


# Xử lý lệnh liệt kê tệp
def handle_list_files(conn):
    try:
        files = os.listdir(STORAGE_DIR)
        if not files:
            conn.sendall(b"NO_FILES")
            logging.info(f"Không có tệp nào trong thư mục lưu trữ.")
            return

        # Gửi file theo từng chunk
        conn.sendall(b"FILES_START")  # Báo hiệu bắt đầu gửi danh sách file
        for file in files:
            conn.sendall(f"{file}\n".encode(FORMAT))  # Gửi từng tên file
        conn.sendall(b"END")  # Báo hiệu kết thúc danh sách

        logging.info(f"Đã gửi danh sách {len(files)} tệp tới client.")
    except Exception as e:
        logging.error(f"Lỗi khi gửi danh sách tệp: {e}")



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