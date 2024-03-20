import requests
import os
import zipfile
import tkinter as tk
from ttkbootstrap import ttk
from ttkbootstrap.dialogs import Messagebox
import threading
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import os
from pathvalidate import sanitize_filepath
import re

window = tk.Tk()
window.title('Image Scraper')
window.geometry('400x240')

label_url = tk.Label(text="URL: ")
label_url.pack()
entry_url = tk.Entry(window)
entry_url.pack(pady=3,ipadx=60)





# Create a StringVar to hold the label text
label_text = tk.StringVar()

# Create a label to display the status
status_label = ttk.Label(window, textvariable=label_text)
status_label.pack(pady=10)

def download_images():
    base_url = entry_url.get()
    if not base_url.startswith('http'):
        label_text.set("Invalid URL", "Please enter a valid URL.")
        return  
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tag = soup.find("img",{"class": "lazy"})
    number_tag = soup.find("button",{"id":"pages_btn"})
    
    if number_tag:
        number_src = number_tag.text
        number = re.findall(r'\d+', number_src)[0]
        print("number_tag: ",number_src)
        print("number pages: ",number)
        image_amount=int(number) +1
        label_text.set(image_amount)
        
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
        path = title_url
        print("base_url: ",base_url)
        # Create a directory to save images if it doesn't exist
        base_path = "E:\\Code\\Python\\scrape"
        sanitized_path = sanitize_filepath(path)
        full_path = os.path.join(base_path, sanitized_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            
        for img_number in range(1, image_amount):       
            img_url = f"{base_url}{img_number}.jpg"
            print("img_url: ", img_url)
            try:
                response = requests.get(img_url)
                response.raise_for_status() # Raise an exception if the request failed
                
                # Update the label text with the download status
                label_text.set(f"Download {img_number}/{image_amount} Completed !")
                window.update_idletasks() # Update the GUI to reflect the change

                # Save the image
                with open(f'{full_path}/{img_number}.jpg', 'wb') as f:
                    f.write(response.content)
            except requests.exceptions.RequestException as e:
                # Log the error and continue with the next image
                print(f"Download Error: Could not download image {img_number}: {e}")
                continue

        # Create a .cbz file
        label_text.set(f'Download {title_url} Complete !')
        with zipfile.ZipFile(f'{full_path}.cbz', 'w') as cbz:
            for img_number in range(1, image_amount):
                img_file = f'{full_path}/{img_number}.jpg'
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
