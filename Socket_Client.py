import socket
import os
import sys
import logging

sys.stdout.reconfigure(encoding='utf-8')

# Thiết lập ghi nhật ký
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"
DOWNLOAD_DIR = "./Downloads"  # Thư mục lưu tệp tải xuống
os.makedirs(DOWNLOAD_DIR, exist_ok=True)  # Đảm bảo thư mục tồn tại

def upload_file(filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, SERVER_PORT))

    try:
        # Gửi lệnh upload
        client.sendall(f"upload {filename}".encode(FORMAT))

        # Chờ phản hồi từ server
        response = client.recv(1024).decode(FORMAT)
        if response == "READY":
            logging.info(f"Bắt đầu tải lên tệp '{filename}'...")
            with open(filename, "rb") as f:
                while chunk := f.read(1024):
                    client.sendall(chunk)
            logging.info(f"Tải lên tệp '{filename}' hoàn tất.")
        else:
            logging.error("Lỗi khi chuẩn bị tải lên tệp.")
    except Exception as e:
        logging.error(f"Lỗi khi tải lên tệp: {e}")
    finally:
        client.close()

def download_file(filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, SERVER_PORT))

    try:
        # Gửi lệnh tải xuống
        client.sendall(f"download {filename}".encode(FORMAT))

        # Nhận phản hồi từ server
        response = client.recv(1024).decode(FORMAT)

        if response.startswith("EXISTS"):
            file_size = int(response.split()[1])
            logging.info(f"Tệp '{filename}' tồn tại với kích thước {file_size} bytes. Bắt đầu tải xuống...")
            received_size = 0

            # Tạo đường dẫn tệp để lưu vào thư mục Downloads
            filepath = os.path.join(DOWNLOAD_DIR, filename)

            with open(filepath, "wb") as f:
                while received_size < file_size:
                    chunk = client.recv(1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    received_size += len(chunk)

                    # Cập nhật tiến độ tải xuống
                    #percent_complete = (received_size / file_size) * 100
                    #logging.info(f"Đã nhận {received_size} bytes ({percent_complete:.2f}%).")

            logging.info(f"Tải xuống tệp '{filename}' hoàn tất và lưu tại '{filepath}'.")
        elif response == "NOT_FOUND":
            logging.warning(f"Tệp '{filename}' không tồn tại trên server.")
        elif response == "INVALID_FILENAME":
            logging.error("Tên tệp không hợp lệ.")
        else:
            logging.error("Lỗi không xác định từ server.")

    except Exception as e:
        logging.error(f"Lỗi khi tải xuống tệp: {e}")
    finally:
        client.close()

def list_files():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, SERVER_PORT))

    try:
        # Gửi lệnh liệt kê tệp
        client.sendall(b"list")

        # Nhận phản hồi từ server
        response = client.recv(1024).decode(FORMAT)
        if response.startswith("FILES"):
            files = response.split("\n")[1:]  
            logging.info("Danh sách các tệp trên server:")
            for file in files:
                logging.info(file)
        elif response == "NO_FILES":
            logging.info("Không có tệp nào trên server.")
    except Exception as e:
        logging.error(f"Lỗi khi liệt kê tệp: {e}")
    finally:
        client.close()

def main():
    while True:
        command = input("Nhập lệnh (download <tên_tệp>, upload <tên_tệp>, list hoặc 'x' để thoát): ").strip()
        if command.lower() == 'x':
            logging.info("Đã thoát khỏi ứng dụng.")
            break
        elif command.startswith("download"):
            _, filename = command.split(maxsplit=1)
            download_file(filename)
        elif command .startswith("upload"):
            _, filename = command.split(maxsplit=1)
            upload_file(filename)
        elif command == "list":
            list_files()
        else:
            logging.warning("Lệnh không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    main()