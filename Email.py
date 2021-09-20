import smtplib
#import xsmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
#from xsmtplib import SMTP

def send_mail(path1,today):
    sender_email = "putisek.c@thaibev.com"
    #receiver_email = ['kajorn.b@thaibev.com','sittichai.de@thaibev.com','weerayut.k@thaibev.com']
    receiver_email = ['nanthamart.l@thaibev.com']
    #cc_email = ['putisek.c@thaibev.com','tawan.t@thaibev.com']
    cc_email = ['tanyaporn.k@thaibev.com','titinun.p@thaibev.com','pimganyapat.u@thaibev.com','tawan.t@thaibev.com','putisek.c@thaibev.com']
    reciver = receiver_email+cc_email

    msg = MIMEMultipart()
    msg['Subject'] = str(today)+' CovidAlert'
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_email)
    msg['cc'] = ", ".join(cc_email)

    #Text Mail
    #msgText = MIMEText('<b>%s</b>' % (body), 'html')
    msgText = MIMEText("""เรียนทุกท่าน
                           <br/>ขอนำส่งรหัสพนักงานที่เข้าใกล้พื้นที่เสี่ยง รายละเอียดตามไฟล์แนบครับ
                           <br/>
                           <br/>Best regards
                           <br/>Putisek.C""" ,'html')
    msg.attach(msgText)

    #Excel file attach
    #1 TIMELINE
    with open(path1, 'rb') as fp:
        excel = MIMEApplication(fp.read())
        excel.add_header('Content-Disposition', 'attachment', filename=str(today)+" CovidAlert.xlsx")
        msg.attach(excel)

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login("putisek.c@thaibev.com","puc#2204")
            smtpObj.sendmail(sender_email,reciver, msg.as_string())
    except Exception as e:
        print(e)
        
def send_mail2(path2,today):
    sender_email = "putisek.c@thaibev.com"
    #receiver_email = ['kajorn.b@thaibev.com','sittichai.de@thaibev.com','weerayut.k@thaibev.com']
    #receiver_email = ['putisek.c@thaibev.com','tawan.t@thaibev.com']
    receiver_email = ['titinun.p@thaibev.com','nanthamart.l@thaibev.com']
    #cc_email = ['putisek.c@thaibev.com','tawan.t@thaibev.com']
    cc_email = ['tanyaporn.k@thaibev.com','pimganyapat.u@thaibev.com','tawan.t@thaibev.com','putisek.c@thaibev.com']
    reciver = receiver_email+cc_email

    msg = MIMEMultipart()
    msg['Subject'] = str(today)+' CovidAlert_Detail'
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_email)
    msg['cc'] = ", ".join(cc_email)

    #Text Mail
    #msgText = MIMEText('<b>%s</b>' % (body), 'html')
    msgText = MIMEText("""เรียนทุกท่าน
                           <br/>ขอนำส่งรายละเอียดพนักงานที่เข้าใกล้พื้นที่เสี่ยง รายละเอียดตามไฟล์แนบครับ
                           <br/>
                           <br/>Best regards
                           <br/>Putisek.C""" ,'html')
    msg.attach(msgText)

    #Excel file attach
    #1 TIMELINE
    with open(path2, 'rb') as fp:
        excel = MIMEApplication(fp.read())
        excel.add_header('Content-Disposition', 'attachment', filename=str(today)+" CovidAlert_Detail.xlsx")
        msg.attach(excel)

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login("putisek.c@thaibev.com","puc#2204")
            smtpObj.sendmail(sender_email,reciver, msg.as_string())
    except Exception as e:
        print(e)
        
#send_mail("")