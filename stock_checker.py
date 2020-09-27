"""
Dependencies of this solution:
1. Chrome browser and chromedriver all installed
2. Browser can be opened by selenium (otherwise website will block app)
3. Gmail account turns on 2 step verification and genereated App Password
"""


from selenium import webdriver
import smtplib
import ssl
import getpass
import keyring
from datetime import datetime
import time
import argparse
import configparser
import logging

logger = logging.getLogger(__name__)
print = logger.info

def check_stock(url_dict):
    instock_dict = {}
    for product_name, product_url in url_dict.items():
        with webdriver.Chrome() as driver:
            driver.get(product_url)
            in_stock_info = driver.find_element_by_class_name('sellable').text
            print(f"{product_name.capitalize()} stock status at {datetime.now().strftime('%d-%b-%Y (%H:%M:%S)')}:")
            print(in_stock_info)
            instock_dict[product_name] = in_stock_info
    return instock_dict


def obtain_email_credentials():
    email_address = input(">>> Enter your email address here: ")
    email_pass = getpass.getpass(">>> Enter your email password here: ")
    keyring.set_password("email", email_address, email_pass)
    print(">>> Password is Saved")
    return email_address


def email_status(stock_status, product, product_url, sender_address, recipient_address):
    """
    Sending self an email of product stock status
    """
    GMAIL_USERNAME = sender_address
    GMAIL_PASSWORD = keyring.get_password("email", sender_address)
    body_of_email = f"[URL]: {product_url}. \r\n\r\n [Stock Status]: {stock_status}"
    email_subject = f'{product.capitalize()} Product Available Now!!!'
    headers = "\r\n".join([f"from: {GMAIL_USERNAME}", 
                           f"subject: {email_subject}", 
                           f"to: {recipient_address}", 
                           "mime-version: 1.0", 
                           "content-type: text/html"])
    content = f"{headers}\r\n\r\n{body_of_email}" 
    print(">>> Email Composed...")
    # creates SMTP session
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        'smtp.gmail.com', port=465, context=context) as server:
        server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        server.sendmail(sender_address, recipient_address, content)
    print(">>> Email Sent...")


def email_product_status(instock_dict, url_dict, sender_address, recipient_address):
    for product_name, product_status in instock_dict.items():
        if "cart" in product_status.lower():
            print(f">>> Product {product_name.capitalize()} is eligible to place in cart, sending email notice")
            email_status(product_status, product_name, url_dict[product_name],
                         sender_address, recipient_address)
        else:
            print(f">>> Product {product_name.capitalize()} is not eligible to purchase.")


if __name__ == "__main__":
    # loading args
    arg_parser = argparse.ArgumentParser(description='Check website for in stock info and send email to user')
    arg_parser.add_argument('--config_path', metavar='config_path', default='./urls.cfg',
                            type=str, help='Path to the urls config file', required=False)
    arg_parser.add_argument('--interval', '-i', metavar='interval', default=600, type=int,
                            help='Interval (seconds) of stock checking job', required=False)
    args = arg_parser.parse_args()

    # loading config
    config = configparser.ConfigParser()
    config.read(args.config_path)

    # initialize logger
    root_logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s: %(levelname)s:: %(message)s')

    logfile = "./tracker.log"
    file_handler = logging.FileHandler(logfile, mode='a')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    root_logger.setLevel(logging.INFO)
    print = root_logger.info

    # main codes
    url_dict = dict(config['urls'])
    print(">>> Obtaining email credentials...")
    email_address = obtain_email_credentials()

    print(">>> Starting jobs")
    while True:
        print(">>> Tracking stocks...")
        instock_dict = check_stock(url_dict)
        print(">>> Updating status via email (if available)...")
        email_product_status(instock_dict, url_dict,
            'elvin.ouyang@gmail.com', 'rosalynnxin@gmail.com')
        print(f">>> Sleep for {args.interval:,} seconds")
        time.sleep(args.interval)