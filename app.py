import requests
import csv
import StringIO

try:
    import config
except ImportError:
    print("Config file config.py.tmpl needs to be copied over to config.py")
    sys.exit(1)

class CallLoop(object):

    def __init__(self):
        payload = {'redirect_to': '', 
                   'email': config.EMAIL,
                   'password': config.PASSWORD,
                   'submit': '1'}
        self.session = requests.session()
        r = self.session.post("https://members.callloop.com/login", data=payload)

    def get_csv(self):
        csv_r = self.session.get('https://members.callloop.com/subscribers/search/download_csv',)

        reader = csv.DictReader(StringIO.StringIO(csv_r.content))

        member_list = []
        for row in reader:
            member_list.append(row)
        return member_list

    def add_subscriber_to_group(self, group_id, phone, first, last, email):
        """
        https://callloop.com/r/?eff23656-7e0f-4b68-bd5c-f39s9sk2&first=Mike&last=Jones&email=mike@aol.com&phone=555555555
        phone - REQUIRED
        first - (optional)
        last - (optional)
        email - (optional)
        """
        pass

    def remove_subscriber_from_group(self, group_id, phone):
        """
        https://callloop.com/s/?eff23656-7e0f-4b68-bd5c-f39s9sk2&phone=555555555
        """
        pass


def main():
    cl = CallLoop()

    member_dict = cl.get_csv()
    print member_dict

if __name__ == '__main__':
    main()