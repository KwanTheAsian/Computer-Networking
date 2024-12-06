import socket
import os
import sys
import logging
import time
import threading
#from tqdm import tqdm

sys.stdout.reconfigure(encoding='utf-8')

# Thiết lập ghi nhật ký
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"
DOWNLOAD_DIR = "./Downloads"  # Thư mục lưu tệp tải xuống
os.makedirs(DOWNLOAD_DIR, exist_ok=True)  # check folder exist

def upload_file(filepath, formatted_name=None):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Kiểm tra path tĩnh hoặc tương đối
        if not os.path.isabs(filepath):
            filepath = os.path.abspath(filepath)  # Chuyển thành path tuyệt đối nếu cần

        if not os.path.isfile(filepath):
            logging.error(f"Tệp không tồn tại: {filepath}")
            return

        # Định dạng tên file nếu chưa có
        if not formatted_name:
            folder_name = os.path.basename(os.path.dirname(filepath))  # Lấy tên thư mục chứa file
            name, ext = os.path.splitext(os.path.basename(filepath))
            formatted_name = f"{name}{ext}"  # Định dạng tên file 

        client.connect((HOST, SERVER_PORT))
        client.sendall(f"upload {formatted_name}".encode(FORMAT))
        response = client.recv(1024).decode(FORMAT)

        if response == "READY":
            logging.info(f"Bắt đầu tải lên tệp '{formatted_name}'...")
            with open(filepath, "rb") as f:
                while chunk := f.read(1024):
                    client.sendall(chunk)
            logging.info(f"Tải lên tệp '{formatted_name}' hoàn tất.")
        else:
            logging.error(f"Lỗi khi chuẩn bị tải lên tệp '{formatted_name}'.")
    except Exception as e:
        logging.error(f"Lỗi khi tải lên tệp '{formatted_name}': {e}")
    except ConnectionResetError:
        logging.error("Server đã đóng kết nối đột ngột.")
    finally:
        client.close()



def download_file(filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, SERVER_PORT))
        client.sendall(f"download {filename}".encode(FORMAT))
        response = client.recv(1024).decode(FORMAT)

        if response.startswith("EXISTS"):
            file_size = int(response.split()[1])
            logging.info(f"Tệp '{filename}' tồn tại với kích thước {file_size} bytes. Bắt đầu tải xuống...")
            received_size = 0
            filepath = os.path.join(DOWNLOAD_DIR, filename)

            if os.path.exists(filepath):
                timestamp = time.strftime("%Y%m%d_%H%M")
                name, ext = os.path.splitext(filename)
                filepath = os.path.join(DOWNLOAD_DIR, f"{name}_{timestamp}{ext}")

            with open(filepath, "wb") as f:
                while received_size < file_size:
                    try:
                        chunk = client.recv(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                        received_size += len(chunk)
                    except (ConnectionResetError, socket.error):
                        logging.error("Kết nối tới server bị đóng đột ngột trong khi tải xuống.")
                        return
            logging.info(f"Tải xuống tệp '{filename}' hoàn tất và lưu tại '{filepath}'.")
        elif response == "NOT_FOUND":
            logging.warning(f"Tệp '{filename}' không tồn tại trên server.")
        else:
            logging.error("Lỗi không xác định từ server.")
    except ConnectionResetError:
        logging.error("Server đã đóng kết nối đột ngột.")
    except Exception as e:
        logging.error(f"Lỗi khi tải xuống tệp '{filename}': {e}")
    finally:
        client.close()

def upload_file_name(client, filepath, formatted_name):
    try:
        client.sendall(f"upload {formatted_name}".encode(FORMAT))
        response = client.recv(1024).decode(FORMAT)
        if response == "READY":
            logging.info(f"Bắt đầu tải lên tệp '{formatted_name}'...")
            with open(filepath, "rb") as f:
                while chunk := f.read(1024):
                    client.sendall(chunk)
            logging.info(f"Tải lên tệp '{formatted_name}' hoàn tất.")
        else:
            logging.error(f"Không thể tải lên tệp '{formatted_name}'.")
    except Exception as e:
        logging.error(f"Lỗi khi tải lên tệp '{formatted_name}': {e}")

def upload_folder(folder_path, mode="sequential"):
    folder_name = os.path.basename(folder_path)
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not files:
        logging.warning("Thư mục không chứa tệp nào để tải lên.")
        return

    if mode == "sequential":
        logging.info(f"Tải lên thư mục '{folder_name}' theo chế độ tuần tự...")
        for file in files:
            filepath = os.path.join(folder_path, file)
            name, ext = os.path.splitext(file)  # Tách tên và định dạng file
            formatted_name = f"{name}_{folder_name}{ext}"  # Giữ nguyên phần mở rộng
            upload_file(filepath, formatted_name)
    elif mode == "parallel":
        logging.info(f"Tải lên thư mục '{folder_name}' theo chế độ song song...")
        threads = []
        for file in files:
            filepath = os.path.join(folder_path, file)
            name, ext = os.path.splitext(file)  # Tách tên và định dạng file
            formatted_name = f"{name}_{folder_name}{ext}"  # Giữ nguyên phần mở rộng
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, SERVER_PORT))
            thread = threading.Thread(target=upload_file_name, args=(client, filepath, formatted_name))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        logging.info("Hoàn thành tải lên thư mục theo chế độ song song.")


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
        command = input("Nhập lệnh (download <tên_tệp>, upload <tên_tệp>, upload_folder <đường_dẫn_thư_mục> <sequential/parallel>, list hoặc 'x' để thoát): ").strip()
        if command.lower() == 'x':
            logging.info("Đã thoát khỏi ứng dụng.")
            break
        elif command.startswith("download"):
            _, filename = command.split(maxsplit=1)
            download_file(filename)
        elif command.startswith("upload_folder"):
            parts = command.split(maxsplit=2)
            folder_path = parts[1]
            mode = parts[2] if len(parts) > 2 else "sequential"
            upload_folder(folder_path, mode)
        elif command.startswith("upload"):
            _, filename = command.split(maxsplit=1)
            upload_file(filename)
        elif command == "list":
            list_files()
        else:
            logging.warning("Lệnh không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    main()