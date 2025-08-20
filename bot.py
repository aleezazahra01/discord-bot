from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from tkinter import *
from bs4 import BeautifulSoup
import csv
import tkinter as tk
import datetime
import time
import pandas as pd
from tkinter import filedialog


format_list = ['.csv', '.xlsx']


class AmazonScraper:
    def __init__(self):
        self.url = ''
        self.file_name = ''
        self.driver = ''
        self.GUI()

    def GUI(self):
        self.COLOUR_ONE = "#222831"
        self.text_color = "#EB8007"
        self.frame_color = "#B5B3AF"

        self.root = tk.Tk()
        self.root.geometry('600x600')
        self.root.config(bg=self.COLOUR_ONE)
        self.root.title("AirBnb scraper ")

        self.title = Label(self.root, text='Amazon Scraper', font=('Helvetica', 20, 'bold'), fg=self.text_color, bg=self.COLOUR_ONE)
        self.title.pack(pady=10)
        self.entry_title = Label(self.root, text='Enter the url of the page:', fg=self.text_color, bg=self.COLOUR_ONE)
        self.entry_title.pack(pady=10)
        self.entry_url = Entry(self.root)
        self.entry_url.pack(pady=5)

        # file name
        self.file_label = Label(self.root, text='Enter the file name: ', fg=self.text_color, bg=self.COLOUR_ONE)
        self.file_label.pack(pady=10)
        self.file_var = tk.StringVar()
        Entry(self.root, textvariable=self.file_var).pack(pady=5)

        # create a scrape button
        self.scrape_button = Button(self.root, text="Scrape from this page", command=self.scrape_func).pack(pady=10)

        # creating a path to save the file
        self.save_button = Button(self.root, text='Save As', command=self.save_as).pack(pady=10)

        # creating another frame inside the root to display the current status
        self.status_frame = tk.Frame(
            self.root,
            width=400,
            height=400,
            bg=self.frame_color,
            relief="ridge",
            borderwidth=3
        )
        # printing instructions on the frame
        self.status_frame.pack(pady=10, padx=10, fill='both', expand=True)
        self.instructions = Label(
            self.status_frame,
            text='Instructions: \n1. Enter the URL of the Amazon page you want to scrape.\n2. Enter a name for your output file.\n3. Choose the format (CSV or XLSX).\n4. Click "Scrape from this page" to start scraping.',
            fg=self.COLOUR_ONE, bg=self.frame_color
        )
        self.instructions.pack(pady=5)

        self.root.mainloop()

    # creating a function to scrape data from the url given by the user
    def scrape_func(self):
        self.url = self.entry_url.get()
        self.file_name = self.file_var.get()

        # default filename if left empty (fix)
        if not self.file_name:
            self.file_name = f"amazon_data_{int(time.time())}"

        # driver init with ChromeDriverManager (fix)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(self.url)

        # quick captcha/robot page check (quality-of-life fix)
        page_text = self.driver.page_source.lower()
        if ("not a robot" in page_text) or ("enter the characters you see below" in page_text):
            msg = Label(self.status_frame, text='Amazon robot check detected. Try again later or use a different network.', fg=self.text_color, bg=self.frame_color)
            msg.pack(pady=5)
            return

        # wait for products using robust selector (fix)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
        )

        # Scroll to load contents more reliably (fix)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)

        # save the html
        with open('page.html', 'w', encoding='utf-8') as f:
            f.write(self.driver.page_source)

        # CSV header aligned with row order (fix)
        with open(f'{self.file_name}.csv', mode='w', encoding='utf-8', newline='') as f:
            self.writer = csv.writer(f)
            self.writer.writerow(['title', 'price', 'item sold', 'ratings', 'link to the item', 'image link'])

        # Parse the page
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.products = soup.find_all('div', {'data-component-type': 's-search-result'})
        self.product_found = len(self.products)

        # Show number of products found
        self.display_found = tk.Label(self.status_frame, text=f"Found {self.product_found} products", bg=self.text_color)
        self.display_found.pack(pady=5)

        try:
            for product in self.products:
                # Title
                titles = product.select_one('h2 > span')
                title_names = titles.get_text(strip=True) if titles else 'N/A'

                # Price
                price_tag = product.find('span', class_='a-price-whole')
                price = price_tag.get_text(strip=True) if price_tag else 'N/A'
                price_symbol_tag = product.find('span', class_='a-price-symbol')
                price_symbol = price_symbol_tag.get_text(strip=True) if price_symbol_tag else 'N/A'
                final_price = (price_symbol + price) if price != 'N/A' else 'N/A'

                # Item sold
                item_sold_tag = product.find('span', class_='a-size-base s-underline-text')
                item_sold = item_sold_tag.get_text(strip=True) if item_sold_tag else 'N/A'

                # Ratings
                stars_tag = product.find('span', class_='a-icon-alt')
                stars = stars_tag.get_text(strip=True) if stars_tag else 'N/A'

                # Product link (simplified selector + domain prefix fix)
                prod_link_tag = product.find('a', class_='a-link-normal')
                prod_link = ("https://www.amazon.com" + prod_link_tag['href']) if prod_link_tag and prod_link_tag.get('href') else 'N/A'

                # Image link
                img_link_tag = product.find('img', class_='s-image')
                img_link = img_link_tag['src'] if img_link_tag else 'N/A'

                # Append to CSV
                with open(f'{self.file_name}.csv', mode='a', encoding='utf-8', newline='') as f:
                    self.writer = csv.writer(f)
                    self.writer.writerow([title_names, final_price, item_sold, stars, prod_link, img_link])

            # proper Label creation + pack (fix)
            self.label_success = Label(self.status_frame, text='Scraping completed successfully', fg=self.text_color, bg=self.frame_color)
            self.label_success.pack(pady=5)

        except Exception as e:
            self.exception_label = Label(self.status_frame, text=f"An error occurred: {e}", bg=self.text_color)
            self.exception_label.pack(pady=5)

    def save_as(self):
        self.file_path = filedialog.asksaveasfilename(
            defaultextension='.csv,.xlsx',
            filetypes=[('CSV files', '*.csv'), ('XLSX files', '*.xlsx')],  # fixed pattern
            title="Save your file as "
        )

        # read the working CSV once (fix for undefined df)
        df = pd.read_csv(f"{self.file_name}.csv")

        if self.file_path.endswith('.csv'):
            df.to_csv(self.file_path, index=False)
            self.display_save = tk.Label(self.root, text=f"Saved in {self.file_path} as {self.file_name}.csv")
            self.display_save.pack(pady=4)
        elif self.file_path.endswith('.xlsx'):
            df.to_excel(self.file_path, index=False)
            self.display_save = tk.Label(self.root, text=f"Saved in {self.file_path} as {self.file_name}.xlsx")
            self.display_save.pack(pady=4)
        else:
            self.display_not_saved = Label(self.root, text='Not saved ', fg=self.text_color, bg=self.COLOUR_ONE)
            self.display_not_saved.pack(pady=4)


if __name__ == "__main__":
    AmazonScraper()
