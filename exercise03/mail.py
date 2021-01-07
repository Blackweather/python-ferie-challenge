import csv
import os
import re
import shutil
import smtplib
import sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import xlrd

BOT_EMAIL_ADDR = "mysupersender@gmail.com"

class User:
    def __init__(self, email, first_name, last_name):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

class Image:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.filename = f"{first_name}_{last_name}_image.png"
        self.filepath = f"img/{self.filename}"

    def create(self):
        shutil.copy("img/image.png", self.filepath)

    def delete(self):
        os.remove(self.filepath)

def is_email_valid(email):
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    pattern = re.compile(regex)

    if pattern.match(email):
        return True

    return False

def get_users_from_csv():
    users = []
    with open('data/emails.csv', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=",")
        for row in csvreader:
            first_name = row['name'].split(" ")[0]
            last_name = row['name'].split(" ")[1]
            email = row['email']
            if is_email_valid(email):
                users.append(User(email, first_name, last_name))
            else:
                print(f"Invalid email for user {first_name} {last_name}")

    return users

def get_users_from_xls():
    users = []
    loc = ("data/emails.xls")
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    for i in range(1, sheet.nrows):
        first_name = sheet.cell_value(i, 1).split(" ")[0]
        last_name = sheet.cell_value(i, 1).split(" ")[1]
        email = sheet.cell_value(i, 0)
        if is_email_valid(email):
            users.append(User(email, first_name, last_name))
        else:
            print(f"Invalid email for user {first_name} {last_name}")
    return users

def compose_message(user, img_path, img_filename):
    #TODO: format as html
    mail_content = f'''
    Hi {user.first_name}! It's a file generated for you.
    '''
    # Set up MIME
    message = MIMEMultipart()
    message['From'] = BOT_EMAIL_ADDR
    message['To'] = user.email
    message['Subject'] = "Your image"
    # Attach message
    message.attach(MIMEText(mail_content, 'plain'))
    # Attach image
    with open(img_path, "rb") as img:
        part =  MIMEApplication(img.read(), Name=img_filename)
    part['Content-Disposition'] = f'attachment; filename="{img_filename}"'
    message.attach(part)
    return message

def send_email(user):
    # create attached image
    image = Image(user.first_name, user.last_name)
    image.create()
    message = compose_message(user, image.filepath, image.filename)

    sender_addr = BOT_EMAIL_ADDR
    sender_pass = os.getenv('EMAIL_PASS')
    receiver_addr = user.email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_addr, sender_pass)
        smtp.send_message(message)

    # delete attached image
    image.delete()

def main():
    users = []
    if len(sys.argv) == 2 and sys.argv[1].lower() == "csv":
        users = get_users_from_csv()
    else:
        users = get_users_from_xls()

    print("\nSending emails to:")
    for user in users:
        print(f"{user.first_name} {user.last_name} - {user.email}")
        send_email(user)

if __name__ == "__main__":
    main()
