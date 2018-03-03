import subprocess
from os.path import expanduser
import sqlite3
import datetime


class Helpers():
    def __init__(self):
        pass

        
class iMessageConnector():
    def __init__(self): 
        self.helpers_library = Helpers()
        self.local_path_to_db = "/Library/Messages/chat.db"
        self.local_home_path = expanduser("~")
        self.phone_to_id = self.get_recipient_matching()
        self.OSX_EPOCH = 978307200

    def get_imsg_db(self):
        imsg_path = '{}{}'.format(self.local_home_path, self.local_path_to_db)
        return sqlite3.connect(imsg_path)

    def get_local_db(self):
        local_path = './chat.db'
        return sqlite3.connect(local_path)

    def imessage_send(self,user,message):
        cmd = """osascript -e 'tell application "Messages"' -e 'set targetService to 1st service whose service type = iMessage'  -e 'set targetBuddy to buddy "{recipient}" of targetService' -e 'send "{message}" to targetBuddy' -e 'end tell'""".format(recipient=user,message=message)        
        subprocess.check_output(cmd, shell=True)

    def get_recipient_matching(self):
        imsg_connect = self.get_imsg_db()
        # imsg_connect = self.get_local_db()

        c = imsg_connect.cursor()
        c.execute("SELECT * FROM `handle`")
        recipients = {}
        for row in c:
            if '+' in row[1]:
                recipients[row[1]] = row[0]

        imsg_connect.close()

        return recipients

    def get_messages_for_recipient(self,phone_number):
        id = self.phone_to_id[phone_number]

        connection = self.get_imsg_db()
        c = connection.cursor()

        c.execute("SELECT * FROM `message` WHERE handle_id=" + str(id))
        messages = []
        for row in c:
            text = ''
            if row[2] is not None:
                text = row[2].replace('\n','')

            date = datetime.datetime.fromtimestamp(row[15] + self.OSX_EPOCH).strftime('%Y-%m-%d %H:%m:%S')
            if row[21] == 1:
                user = 'Me'
            else:
                user = phone_number
            encoded_text = text.encode('ascii', 'ignore')
            print '{}: {} - {}'.format(date,user,encoded_text)
            msg_data_type = {
                'date': date,
                'user': user,
                'message': encoded_text
            }
            messages.append(msg_data_type)
        connection.close()

        return messages

    def get_imsg_recipients(self):
        imsg_connect = self.get_imsg_db()
        #imsg_connect = self.get_local_db()

        c = imsg_connect.cursor()
        c.execute("SELECT * FROM `handle`")
        recipients = []
        for row in c:

            if '+' in row[1]:
                recipients.append(row[1])
        imsg_connect.close()
        return recipients
