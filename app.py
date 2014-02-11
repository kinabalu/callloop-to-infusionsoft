import requests
import csv
import StringIO
import argparse

from InfusionsoftLibrary import Infusionsoft

try:
    import config
except ImportError:
    print("Config file config.py.tmpl needs to be copied over to config.py")
    sys.exit(1)

class CallLoop(object):

    def __init__(self):
        self.infusion = Infusionsoft(config.INFUSIONSOFT_APP_NAME,
                                config.INFUSIONSOFT_API_KEY)

        payload = {'redirect_to': '', 
                   'email': config.EMAIL,
                   'password': config.PASSWORD,
                   'submit': '1'}
        self.session = requests.session()
        r = self.session.post("https://members.callloop.com/login", data=payload)

    def sync_with_infusionsoft(self, member_list):
        infusion_list = self.infusion.DataService('query', 'Contact', 10, 0, 
                                                 {config.FIELD_IMPORTSOURCE: 'CallLoop'},
                                                 ['Id', 'FirstName', 'LastName', 'Email', config.FIELD_CALLLOOPID])        

        member_add = 0
        for member in member_list:
            found = False
            for infusion_member in infusion_list:
                if member['Id'] == infusion_member[config.FIELD_CALLLOOPID]:
                    found = True
                    break
            if not found:
                member_add += 1
                contact = {'FirstName': member['First'],
                           'LastName': member['Last'],
                           'Email': member['Email'],
                           'Phone1': member['Phone'],
                           config.FIELD_CALLLOOPID: member['Id'],
                           config.FIELD_IMPORTSOURCE: 'CallLoop'
                }
                contact_id = self.infusion.ContactService('add', contact)
                print("[%s] - Adding %s %s" % (member['Id'], member['First'], member['Last'],))
        print("Contacts added - %d" % (member_add,))

    def get_memberlist(self):
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
    parser = argparse.ArgumentParser(prog='callloop-to-infusionsoft')

    parser.add_argument(
        "--sync",
        dest="sync",
        action="store_true",
        help="Sync with InfusionSoft"
    )

    cl = CallLoop()

    args = parser.parse_args()

    if args.sync:
        member_list = cl.get_memberlist()
        cl.sync_with_infusionsoft(member_list)

if __name__ == '__main__':
    main()