from .connections import *
from .scans import *

class alerts:

    @staticmethod
    def send_email(subject, message):

        '''
        Sends an email from a gmail account to the emails configured at input_files/email_details.txt
        The email_details.txt file should have three lines:
        1st Line: Sender gmail address
        2nd Line: Gmail app paswword - See: https://support.google.com/mail/answer/185833?hl=en
        3rd Line: Recipients (can be any email address)
        
        '''

        with open("input_files/email_details.txt") as file:
            details = [line.rstrip() for line in file]
            email = details[0]
            password = details[1]
            send_to = details[2]

        smtp_object = smtplib.SMTP('smtp.gmail.com',587)
        smtp_object.ehlo()
        smtp_object.starttls()
        smtp_object.login(email,password)

        msg = "Subject: "+subject+'\n'+message
        smtp_object.sendmail(email, send_to, msg)


        return None
    

    @staticmethod
    def critical_vulns(*args):

        tio = connect_io()

        if len(args) == 0:
            print("You did not specified a scan or group os scans for the alerts")
            return "Could not complete report operation"
        
        else:

            with open('output_files/io_critical_vulns_report.csv', 'ab') as reportobj:

                for id in args:
                    
                    try:
                        tio.scans.export(id,('severity', 'eq', 'Critical'), fobj=reportobj, format='csv')
                        print("Done with scan id:"+str(id))

                    except Exception:
                        print("Could not work with Scan:"+str(id))
                        continue
            
            row_num = 0
            with open ('output_files/io_critical_vulns_report.csv') as csvfile:
                rowreader = csv.reader(csvfile, delimiter=',')
                for row in rowreader:
                    row_num += 1

            my_alerts = alerts()

            if row_num < 2:
                my_alerts.send_email("[Automatic Report] No Critical Vulns Found", "We did not found any critical vulnerabilities")

            else:
                my_alerts.send_email("[Automatic Report] Critical Vulns Found", 
                                     "We found critical vulnerabilities, please check the critical vulns report")

            return "Email Report Sent"
