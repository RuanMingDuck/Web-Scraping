import requests
import os
import zipfile
import tkinter as tk
from tkinter import ttk
from ttkbootstrap.dialogs import Messagebox
import threading
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import os

window = tk.Tk()
window.title('Image Scraper')
window.geometry('400x240')

label_url = tk.Label(text="URL: ")
label_url.pack()
entry_url = tk.Entry(window)
entry_url.pack(pady=3,ipadx=60)

label_amount = tk.Label(text="Number of Pages: ")
label_amount.pack()
entry_amount = tk.Entry(window)
entry_amount.pack(pady=8,ipadx=5)

# Create a StringVar to hold the label text
label_text = tk.StringVar()

# Create a label to display the status
status_label = ttk.Label(window, textvariable=label_text)
status_label.pack(pady=10)

def download_images():
    # Get the URL and the number of images from the entry fields
    base_url = entry_url.get()
    try:
        image_amount = int(entry_amount.get())
    except ValueError:
        Messagebox.error("Invalid Input", "Please enter a valid number for the image amount.")
        return
    # Check if the URL is valid
    if not base_url.startswith('http'):
        Messagebox.error("Invalid URL", "Please enter a valid URL.")
        return  
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tag = soup.find("img",{"class": "lazy"})
    if img_tag:
        data_src = img_tag.get("data-src")
        title_url_raw = img_tag.get("alt")
        title_url = title_url_raw[:-6]
        parsed_url = urlparse(data_src)
        pic_url = os.path.dirname(data_src) +"/"
        print("data_src: ",data_src)
        print("title_url: ",title_url)
        print("pic_url: ",pic_url)  
        base_url = pic_url
        print("base_url: ",base_url)
        # Create a directory to save images if it doesn't exist
        if not os.path.exists(title_url):
            os.makedirs(title_url)
        for img_number in range(1, image_amount + 1):       
            img_url = f"{base_url}{img_number}.jpg"
            print("img_url: ",img_url)
            try:
                response = requests.get(img_url)
                response.raise_for_status()  # Raise an exception if the request failed
                
                # Update the label text with the download status
                label_text.set(f"Download {img_url} Completed !")
                window.update_idletasks()  # Update the GUI to reflect the change

                # Save the image
                with open(f'images/{img_number}.jpg', 'wb') as f:
                    f.write(response.content)
            except requests.exceptions.RequestException as e:
                Messagebox.error("Download Error", f"Could not download image {img_number}: {e}")
                return
        # Create a .cbz file
        label_text.set(f'Download {title_url} Complete !')
        with zipfile.ZipFile(f'{title_url}.cbz', 'w') as cbz:
            for img_number in range(1, image_amount +   1):
                img_file = f'images/{img_number}.jpg'
                if os.path.exists(img_file):
                    cbz.write(img_file, f'{img_number}t.jpg')
                else:
                    print(f"Warning: {img_file} not found.")
        print("Compression completed.")
        label_text.set(f'Compress {title_url} Complete !')
        

def start_download():
    # Start the download process in a separate thread
    download_thread = threading.Thread(target=download_images)
    download_thread.start()

button_url = tk.Button(text="Download", command=start_download)
button_url.pack()

window.mainloop()
