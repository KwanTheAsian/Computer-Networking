from customtkinter import *
import customtkinter as ctk
from CTkTable import CTkTable
import tkinter as tk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import sys
import socket
import os
import logging
import time
import threading
from tqdm import tqdm

def center_window(window, width, height, offset_x=0, offset_y=0):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2)) + offset_x
    y = int((screen_height / 2) - (height / 2)) + offset_y
    window.geometry(f"{width}x{height}+{x}+{y}")

class LoginWindow:
    def __init__(self):
        self.root = CTk()
        self.root.title("Network")
        center_window(self.root, 600, 480)
        self.root.resizable(0, 0)
        side_img_data = Image.open("side-.png")
        username_icon_data = Image.open("email-icon.png")
        password_icon_data = Image.open("password-icon.png")
        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
        username_icon = CTkImage(dark_image=username_icon_data, light_image=username_icon_data, size=(20, 20))
        password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))
        CTkLabel(master=self.root, text="", image=side_img).pack(expand=True, side="left")

        frame = CTkFrame(master=self.root, width=300, height=480, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="right")

        CTkLabel(master=frame, text="Welcome!", text_color="#5766F9", anchor="w", justify="left",
         font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
        CTkLabel(master=frame, text="Please enter your username and password", text_color="#7E7E7E", anchor="w", justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Username:", text_color="#5766F9", anchor="w", justify="left",
         font=("Arial Bold", 14), image=username_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
        self.username_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#5766F9", border_width=1,
                       text_color="#000000")
        self.username_entry.pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Password:", text_color="#5766F9", anchor="w", justify="left",
         font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
        self.password_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#5766F9", border_width=1,
                          text_color="#000000", show="*")
        self.password_entry.pack(anchor="w", padx=(25, 0))

        self.status_label = CTkLabel(master=frame, text="", text_color="#FF0000", anchor="w", justify="left",
                        font=("Arial Bold", 12))
        self.status_label.pack(anchor="w", padx=(25, 0))
        ctk.CTkButton(master=frame, text="Login", fg_color="#5766F9", hover_color="#E44982", font=("Arial Bold", 12),
          text_color="#ffffff", width=225, command= self.login).pack(anchor="w", pady=(40, 0), padx=(25, 0))
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def login(self):
        # Retrieve login credentials
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Construct SQL query to fetch user record
        user = "a"

        if user == username:
            # Compare passwords
            stored_password = "1"
            if password == stored_password:
                # Login successful
                self.status_label.configure(text="Login successful!", text_color="#00FF00")
                self.root.withdraw()
                self.root.quit()
            else:
                # Invalid password
                self.status_label.configure(text="Invalid password!", text_color="#FF0000")

        else:
            # User not found
            self.status_label.configure(text="User not found!", text_color="#FF0000")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, SERVER_PORT))
                logging.info("Connected to server.")

                # Gửi lệnh đến server
                command = "login"  #đăng nhập
                s.sendall(command.encode(FORMAT))

                # Nhận phản hồi từ server
                response = s.recv(1024).decode(FORMAT)
                if response == "SERVER_FULL":
                    self.status_label.configure(text="Server đã đầy. Hãy thử lại sau.", text_color="#FF0000")
                    return  # Thoát nếu server đầy
                elif response == "INVALID_COMMAND":
                    self.status_label.configure(text="Lệnh không hợp lệ, hãy thử lại.", text_color="#FF0000")
                else:
                    # Xử lý các phản hồi khác từ server
                    logging.info(f"Server response: {response}")   
        except ConnectionRefusedError:
            self.status_label.configure(text="Không thể kết nối đến server", text_color="#FF0000")
        except Exception as e:
            self.status_label.configure(text=f"Lỗi khi kết nối đến server: {e}", text_color="#FF0000")
   
    def on_closing(self): 
        self.root.destroy()
        sys.exit()

class MainWindow:
    def __init__(self):
        set_appearance_mode("light")
        self.root = CTk()
        center_window(self.root, 600, 480)
        self.root.resizable(0, 0)
        self.root.title("Main Program")
        
        frame = CTkFrame(master=self.root, width=300, height=480, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="top")
    
        self.label_main = ctk.CTkLabel(master=frame, text="SOCKET SERVER", text_color="#5766F9", anchor="w", justify="left",
         font=("Arial Bold", 24))
        self.label_main.pack(anchor="center", pady=(80, 10), padx=(0, 0))
        
        self.file_button = CTkButton(master=frame, font=("Arial Bold", 16), text = 'Upload a file',
                                     command=self.upload_file, fg_color="#5766F9", hover_color="#E44982", width = 255)
        self.file_button.pack(pady = (50, 0))
        
        self.file_button = CTkButton(master=frame, font=("Arial Bold", 16), text = 'Upload a folder',
                                     command=self.upload_folder, fg_color="#5766F9", hover_color="#E44982", width = 255)
        self.file_button.pack(pady = (50, 0))
        
        self.file_button = CTkButton(master=frame, font=("Arial Bold", 16), text = 'Download a file', 
                                     command=self.download_file, fg_color="#5766F9", hover_color="#E44982", width = 255)
        self.file_button.pack(pady = (50, 0))
        
        self.file_popup = None
    
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def upload_file(self):
        Upload = UploadFileWindow()
        
    def download_file(self):
        Download = DownloadFileWindow()
        
    def upload_folder(self):
        Download = UploadFolderWindow()
        
    def on_closing(self): 
        self.root.destroy()
        sys.exit()
        
class UploadFileWindow:
    def __init__(self):
        self.filename = None
        self.root = CTk()
        center_window(self.root, 600, 480, 40, 40)
        self.root.resizable(0, 0)
        self.root.title("Upload")
    
        self.frame = CTkFrame(master=self.root, width=300, height=480, fg_color="#ffffff")
        self.frame.pack_propagate(0)
        self.frame.pack(expand=True, side="top")

        CTkLabel(master=self.frame, text="Upload A File", text_color="#5766F9", anchor="w", justify="left",
         font=("Arial Bold", 24)).pack(anchor="center", pady=(50, 5), padx=(0, 0))
        CTkLabel(master=self.frame, text="Please enter your file name", text_color="#7E7E7E", anchor="w", justify="left",
         font=("Arial Bold", 12)).pack(anchor="center", padx=(0, 0), pady=(20, 5))
        
        self.file_entry = CTkEntry(master=self.frame, width=225, fg_color="#EEEEEE", border_color="#5766F9", border_width=1,
                       text_color="#000000")
        self.file_entry.pack(anchor="center", padx=(0, 0))
        self.status_label = CTkLabel(master=self.frame, text="", text_color="#FF0000", anchor="w", justify="left",
                        font=("Arial Bold", 12))
        self.status_label.pack(anchor="center")
        self.file_open = CTkButton(self.frame, text = 'Open file', command=self.open_file, font=("Arial Bold", 12))
        self.file_open.pack(anchor="center", padx=(0, 0), pady=(10,0))
        
        self.file_dir = CTkButton(self.frame, text = 'Open a file directory', command=self.select_file, font=("Arial Bold", 12))
        self.file_dir.pack(anchor="center", padx=(0, 0), pady=(10,0))
        
        self.upload_status_label = CTkLabel(master=self.frame, text="", text_color="#FF0000", anchor="w", justify="left",
                        font=("Arial Bold", 12))
        self.upload_status_label.pack(anchor="center", pady = (50, 0))
        self.progress = CTkProgressBar(master=self.frame, orientation="horizontal", progress_color="blue")
        self.yes_btn = None
    
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def open_file(self):
        filename = self.file_entry.get()
        if os.path.exists(filename):
            self.status_label.configure(text = f"Found '{filename}'")
            self.filename = filename
            self.AskUpload()
        else:
            self.status_label.configure(text = f"'{filename}' does not exist!")
        
    def select_file(self):
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(
            title='Choose file for upload',
            initialdir='/',
            filetypes=filetypes
        )
        self.filename = filename
        self.root.focus()
        if self.filename != "":
            self.AskUpload()
        
    def AskUpload(self):
        self.upload_status_label.configure(text = f"Do you want to upload '{self.filename}' ?")
        self.yes_btn = CTkButton(self.frame, text = 'YES', command=self.UploadFile, font=("Arial Bold", 12))
        self.progress.set(0)
        self.progress.pack(pady=(10, 10))
        self.yes_btn.pack(anchor="center", padx=(0, 0), pady=(10,0))
        
    def UploadFile(self, formatted_name=None):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Kiểm tra path tĩnh hoặc tương đối
            if not os.path.isabs(self.filename):
                self.filename = os.path.abspath(self.filename)  # Chuyển thành path tuyệt đối nếu cần

            if not os.path.isfile(self.filename):
                logging.error(f"Tệp không tồn tại: {self.filename}")
                return

            # Định dạng tên file nếu chưa có
            if not formatted_name:
                name, ext = os.path.splitext(os.path.basename(self.filename))
                formatted_name = f"{name}{ext}"  # Định dạng tên file 

            client.connect((HOST, SERVER_PORT))
            client.sendall(f"upload {formatted_name}".encode(FORMAT))
            response = client.recv(1024).decode(FORMAT)

            if response == "READY":
                logging.info(f"Bắt đầu tải lên tệp '{formatted_name}'...")
                file_size = os.path.getsize(self.filename)
                
                # Set progressbar
                total_received = 0 # Byte đã nhận
                self.progress.set(0) 
                self.root.update_idletasks()
                
                with open(self.filename, "rb") as f, tqdm(
                    total=file_size, unit="B", unit_scale=True, desc="Uploading", ncols=80
                ) as progress:
                    while chunk := f.read(1024):
                        client.sendall(chunk)
                        progress.update(len(chunk)) # tqdm
                        total_received += len(chunk) # UI
                        self.progress.set(float(total_received / file_size)) # UI
                        self.root.update_idletasks() # UI
                logging.info(f"Tải lên tệp '{formatted_name}' hoàn tất.")
                # Hiện thông báo (UI)
                showinfo(title = 'Done', message="File uploaded successfully!")
            else:
                logging.error(f"Lỗi khi chuẩn bị tải lên tệp '{formatted_name}'.")
        except Exception as e:
            logging.error(f"Lỗi khi tải lên tệp '{formatted_name}': {e}")
        except ConnectionResetError:
            logging.error("Server đã đóng kết nối đột ngột.")
        finally:
            client.close()
        self.yes_btn.pack_forget()
        self.progress.pack_forget()
        self.upload_status_label.configure(text = "")
        
    def on_closing(self): 
        self.root.destroy()

class DownloadFileWindow:
    def __init__(self):
        self.filename = None
        self.root = CTk()
        center_window(self.root, 600, 480, 40, 40)
        self.root.resizable(0, 0)
        self.root.title("Download")
    
        self.frame = CTkFrame(master=self.root, width=600, height=480, fg_color="#ffffff")
        self.frame.pack_propagate(0)
        self.frame.pack(expand=True, side="top")

        CTkLabel(master=self.frame, text="Download a file", text_color="#5766F9", anchor="w", justify="left",
         font=("Arial Bold", 24)).pack(anchor="center", pady=(20, 5), padx=(0, 0))
        CTkLabel(master=self.frame, text="Please enter your file name", text_color="#7E7E7E", anchor="w", justify="left",
         font=("Arial Bold", 12)).pack(anchor="center", padx=(0, 0), pady=(20, 5))
        
        self.file_entry = CTkEntry(master=self.frame, width=225, fg_color="#EEEEEE", border_color="#5766F9", border_width=1,
                       text_color="#000000")
        self.file_entry.pack(anchor="center", padx=(0, 0))
        self.status_label = CTkLabel(master=self.frame, text="", text_color="#FF0000", anchor="w", justify="left",
                        font=("Arial Bold", 12))
        self.status_label.pack(anchor="center")
        self.progress = CTkProgressBar(master=self.frame, orientation="horizontal", progress_color="blue")
        self.file_download = CTkButton(self.frame, text = 'Download file', command=self.on_select, font=("Arial Bold", 12))
        self.file_download.pack(anchor="center", padx=(0, 0), pady=(20,0))
        
        listfiles = list_files()  
        if isinstance(listfiles, list):  
            #listfiles = listfiles.split("\n")  
            data_list = [["Filename"]]  
            data_list.extend([[file] for file in listfiles if file.strip()])  # Tạo danh sách 2D
            table_frame = CTkScrollableFrame(master=self.frame, fg_color="transparent")
            table_frame.pack(expand=True, fill="x", padx=40, pady=10)
            self.table = CTkTable(master=table_frame, values=data_list,colors=["#E6E6E6","#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4")
            self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
            self.table.pack(expand=True, fill="x")
    
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_select(self):
        self.filename = self.file_entry.get()
        self.progress.set(0)
        self.progress.place(anchor = "center", rely = 0.35, relx = 0.5)
        result = self.download_file()
        if result == "error":
            showinfo(
                title = 'Error',
                message="An error occured!"
            )
            self.status_label.configure(text = f"An error occured!")
        elif result == "warning":
            showinfo(
                title = 'Warning',
                message="File does not exist on server!"
            )
            self.status_label.configure(text = f"File does not exist on server!")
        elif result == "success":
            showinfo(
                title = 'Done',
                message="File downloaded successfully"
            )
            self.status_label.configure(text = f"File downloaded successfully")
        self.progress.place_forget()
    
    def download_file(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((HOST, SERVER_PORT))
            client.sendall(f"download {self.filename}".encode(FORMAT))
            response = client.recv(1024).decode(FORMAT)

            if response.startswith("EXISTS"):
                file_size = int(response.split()[1])
                logging.info(f"Tệp '{self.filename}' tồn tại với kích thước {file_size} bytes. Bắt đầu tải xuống...")
                received_size = 0
                filepath = os.path.join(DOWNLOAD_DIR, self.filename)

                # Handle duplicate filenames
                if os.path.exists(filepath):
                    timestamp = time.strftime("%Y%m%d_%H%M")
                    name, ext = os.path.splitext(self.filename)
                    filepath = os.path.join(DOWNLOAD_DIR, f"{name}_{timestamp}{ext}")

                os.makedirs(DOWNLOAD_DIR, exist_ok=True)  # Ensure download directory exists

                with open(filepath, "wb") as f, tqdm(
                    total=file_size, unit="B", unit_scale=True, desc="Downloading", ncols=80
                ) as progress:
                    while received_size < file_size:
                        try:
                            chunk = client.recv(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                            received_size += len(chunk)
                            progress.update(len(chunk))
                            self.progress.set(float(received_size / file_size)) # UI
                            self.root.update_idletasks() # UI
                        except (ConnectionResetError, socket.error):
                            logging.error("Kết nối tới server bị đóng đột ngột trong khi tải xuống.")
                            return "error"
                logging.info(f"Tải xuống tệp '{self.filename}' hoàn tất và lưu tại '{filepath}'.")
                return "success"
            elif response == "NOT_FOUND":
                logging.warning(f"Tệp '{self.filename}' không tồn tại trên server.")
                return "warning"
            else:
                logging.error("Lỗi không xác định từ server.")
                return "error"
        except ConnectionResetError:
            logging.error("Server đã đóng kết nối đột ngột.")
            return "error"
        except Exception as e:
            logging.error(f"Lỗi khi tải xuống tệp '{self.filename}': {e}")
            return "error"
        finally:
            client.close()  
        
    def on_closing(self): 
        self.root.quit()
        self.root.destroy()

class UploadFolderWindow:
    def __init__(self):
        self.dir = None
        self.root = CTk()
        center_window(self.root, 600, 480, 40, 40)
        self.root.resizable(0, 0)
        self.root.title("Upload")
    
        self.frame = CTkFrame(master=self.root, width=300, height=480, fg_color="#ffffff")
        self.frame.pack_propagate(0)
        self.frame.pack(expand=True, side="top")

        CTkLabel(master=self.frame, text="Upload Folder", text_color="#5766F9", anchor="w", justify="left",
         font=("Arial Bold", 24)).pack(anchor="center", pady=(50, 5), padx=(0, 0))
        CTkLabel(master=self.frame, text="Please enter your folder directory", text_color="#7E7E7E", anchor="w", justify="left",
         font=("Arial Bold", 12)).pack(anchor="center", padx=(0, 0), pady=(20, 5))
        
        self.dir_entry = CTkEntry(master=self.frame, width=225, fg_color="#EEEEEE", border_color="#5766F9", border_width=1,
                       text_color="#000000")
        self.dir_entry.pack(anchor="center", padx=(0, 0))
        self.status_label = CTkLabel(master=self.frame, text="", text_color="#FF0000", anchor="w", justify="left",
                        font=("Arial Bold", 12))
        self.status_label.pack(anchor="center")
        self.file_open = CTkButton(self.frame, text = 'Open file', command=self.open_file, font=("Arial Bold", 12))
        self.file_open.pack(anchor="center", padx=(0, 0), pady=(10,0))
        
        self.file_dir = CTkButton(self.frame, text = 'Open a file directory', command=self.select_file, font=("Arial Bold", 12))
        self.file_dir.pack(anchor="center", padx=(0, 0), pady=(10,0))
        
        self.upload_status_label = CTkLabel(master=self.frame, text="", text_color="#FF0000", anchor="w", justify="left",
                        font=("Arial Bold", 12))
        self.upload_status_label.pack(anchor="center", pady = (50, 0))
    
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def open_file(self):
        dir = self.dir_entry.get()
        if os.path.exists(dir):
            self.status_label.configure(text = f"Found '{dir}'")
            self.dir = dir
            self.AskUpload()
        else:
            self.status_label.configure(text = f"'{dir}' does not exist!")
        
    def select_file(self):
        dir = filedialog.askdirectory(
            title='Choose a directory',
            mustexist=True
        )
        self.dir = dir
        self.root.focus_force()
        self.AskUpload()
        
    def AskUpload(self):
        self.upload_status_label.configure(text = f"Do you want to upload in parallel mode?")
        CTkButton(self.frame, text = 'YES', command=self.UploadFolder, font=("Arial Bold", 12)).pack(anchor="center", padx=(0, 0), pady=(10,0))
        CTkButton(self.frame, text = 'NO', command=self.UploadFolderParallel, font=("Arial Bold", 12)).pack(anchor="center", padx=(0, 0), pady=(10,0))
        
    def UploadFolder(self):
        upload_folder(self.dir)
        showinfo(
            title = 'Done',
            message="File uploaded successfully!"
        )
        self.root.quit()
        self.root.destroy()
        
    def UploadFolderParallel(self):
        upload_folder(self.dir, "parallel")
        showinfo(
            title = 'Done',
            message="File uploaded successfully!"
        )
        self.root.quit()
        self.root.destroy()
        
    def on_closing(self): 
        self.root.destroy()        
        
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
        # Ensure absolute file path
        if not os.path.isabs(filepath):
            filepath = os.path.abspath(filepath)

        if not os.path.isfile(filepath):
            logging.error(f"Tệp không tồn tại: {filepath}")
            return

        # Generate formatted file name if not provided
        if not formatted_name:
            name, ext = os.path.splitext(os.path.basename(filepath))
            formatted_name = f"{name}{ext}"

        client.connect((HOST, SERVER_PORT))
        client.sendall(f"upload {formatted_name}".encode(FORMAT))
        response = client.recv(1024).decode(FORMAT)

        if response == "READY":
            logging.info(f"Bắt đầu tải lên tệp '{formatted_name}'...")

            # Get file size for progress tracking
            file_size = os.path.getsize(filepath)

            with open(filepath, "rb") as f, tqdm(
                total=file_size, unit="B", unit_scale=True, desc="Uploading", ncols=80
            ) as progress:
                while chunk := f.read(1024):
                    client.sendall(chunk)
                    progress.update(len(chunk))

            logging.info(f"Tải lên tệp '{formatted_name}' hoàn tất.")
        else:
            logging.error(f"Lỗi khi chuẩn bị tải lên tệp '{formatted_name}'.")
    except Exception as e:
        logging.error(f"Lỗi khi tải lên tệp '{formatted_name}': {e}")
    except ConnectionResetError:
        logging.error("Server đã đóng kết nối đột ngột.")
    finally:
        client.close()
    
def upload_file_name(client, filepath, formatted_name):
    try:
        file_size = os.path.getsize(filepath)  # Get the file size
        client.sendall(f"upload {formatted_name}".encode(FORMAT))
        response = client.recv(1024).decode(FORMAT)

        if response == "READY":
            logging.info(f"Bắt đầu tải lên tệp '{formatted_name}'...")
            progress = tqdm(total=file_size, unit="B", unit_scale=True, desc=f"Uploading {formatted_name}")
            with open(filepath, "rb") as f:
                while chunk := f.read(1024):
                    client.sendall(chunk)
                    progress.update(len(chunk))  # Update the progress bar
            progress.close()
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

        def parallel_upload(client, filepath, formatted_name):
            upload_file_name(client, filepath, formatted_name)

        for file in files:
            filepath = os.path.join(folder_path, file)
            name, ext = os.path.splitext(file)  # Tách tên và định dạng file
            formatted_name = f"{name}_{folder_name}{ext}"  # Giữ nguyên phần mở rộng
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, SERVER_PORT))
            thread = threading.Thread(target=parallel_upload, args=(client, filepath, formatted_name))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        logging.info("Hoàn thành tải lên thư mục theo chế độ song song.")


def list_files():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(1)  # Timeout 10 giây
    try:
        client.connect((HOST, SERVER_PORT))
        client.sendall(b"list")

        response = client.recv(11).decode(FORMAT)
        if response == "NO_FILES---":
            logging.info("Không có tệp nào trên server.")
            return []
        elif response == "FILES_START":
            logging.info("Danh sách các tệp trên server:")
            file_list = []
            data = ""
            while True:
                try:
                    chunk = client.recv(1024).decode(FORMAT)
                    data = data + chunk
                    data_temp = data.splitlines()
                    end_str = data_temp[-1]
                    if end_str == "END":
                        for filename in data_temp:
                            if filename == "END":
                                break
                            logging.info(filename)
                            file_list.append(filename)
                        break
                except socket.timeout:
                    logging.error("Quá thời gian chờ khi nhận danh sách tệp từ server.")
                    break
            return file_list
        else:
            logging.error("Lỗi không xác định từ server.")
            return []
    except Exception as e:
        logging.error(f"Lỗi khi liệt kê tệp: {e}")
        return []
    finally:
        client.close()

def main():
    # while True:
    #     command = input("Nhập lệnh (download <tên_tệp>, upload <tên_tệp>, upload_folder <đường_dẫn_thư_mục> <sequential/parallel>, list hoặc 'x' để thoát): ").strip()
    #     if command.lower() == 'x':
    #         logging.info("Đã thoát khỏi ứng dụng.")
    #         break
    #     elif command.startswith("download"):
    #         _, filename = command.split(maxsplit=1)
    #         download_file(filename)
    #     elif command.startswith("upload_folder"):
    #         parts = command.split(maxsplit=2)
    #         folder_path = parts[1]
    #         mode = parts[2] if len(parts) > 2 else "sequential"
    #         upload_folder(folder_path, mode)
    #     elif command.startswith("upload"):
    #         _, filename = command.split(maxsplit=1)
    #         upload_file(filename)
    #     elif command == "list":
    #         list_files()
    #     else:
    #         logging.warning("Lệnh không hợp lệ. Vui lòng thử lại.")
    app_login = LoginWindow()
    app_main = MainWindow()

if __name__ == "__main__":
    main()
