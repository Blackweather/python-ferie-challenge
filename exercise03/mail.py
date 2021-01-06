import sys
import csv
import xlrd

class User:
    def __init__(self, email, first_name, last_name):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

def get_users_from_csv():
    users = []
    with open('data/emails.csv', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=",")
        for row in csvreader:
            first_name = row['name'].split(" ")[0]
            last_name = row['name'].split(" ")[1]
            # TODO: add email validation
            users.append(User(row['email'], first_name, last_name))
    return users

def get_users_from_xls():
    users = []
    loc = ("data/emails.xls")
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    for i in range(1, sheet.nrows):
        first_name = sheet.cell_value(i, 1).split(" ")[0]
        last_name = sheet.cell_value(i, 1).split(" ")[1]
        # TODO: add email validation
        users.append(User(sheet.cell_value(i, 0), first_name, last_name))
    return users

def main():
    users = []
    if len(sys.argv) == 2 and sys.argv[1].lower() == "csv":
        users = get_users_from_csv()
    else:
        users = get_users_from_xls()

    print("Sending emails to:")
    for user in users:
        print(f"{user.first_name} {user.last_name} - {user.email}")

if __name__ == "__main__":
    main()