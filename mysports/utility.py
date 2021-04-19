from django.core.mail import send_mail

# import smtplib
# from email.mime.text import MIMEText
# SMTP_SERVER = "smtp.mail.yahoo.com"
# SMTP_PORT = 587
# SMTP_USERNAME = "major_tiwari@yahoo.com"
# SMTP_PASSWORD = "dcidcidci"
# def sendEmail(**kwargs):
#     debuglevel = True
#     mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#     mail.set_debuglevel(debuglevel)
#     mail.starttls()
#     mail.login(SMTP_USERNAME, SMTP_PASSWORD)
#     mail.quit()
#
#     orderId = None
#     final_order = None
#     email = None
#     for key, value in kwargs.items():
#         print("%s == %s" % (key, value))
#         if key=='orderid':
#             orderId = kwargs[key]
#         elif key == 'orderedItems':
#             final_order = kwargs[key]
#         elif key == 'email':
#             email = kwargs
#     subject = f"Order No {orderId} with SportsMart"
#     message = f"Thanks for shopping with us your order details are as below" \
#                f"{final_order}"
#     #mail.sendmail('admin@myblog.com', email, message)
#     mail.sendmail(subject, message, 'admin@myblog.com', email)
#     print('email Sent')

def sendEmail(**kwargs):
    orderId = None
    final_order = None
    email = None
    for key, value in kwargs.items():
        print("%s == %s" % (key, value))
        if key=='orderid':
            orderId = kwargs[key]
        elif key == 'orderedItems':
            final_order = kwargs[key]
        elif key == 'email':
            email = kwargs
    subject = f"Order No {orderId} with SportsMart"
    message = f"Thanks for shopping with us your order details are as below" \
               f"{final_order}"
    send_mail(subject, message, 'admin@myblog.com', email)
    # print('email Sent')

def sendEmailPasswordRecovery(**kwargs):
    email = None
    password = None
    for key, value in kwargs.items():
        print("%s == %s" % (key, value))
        if key=='email':
            email = kwargs[key]
        elif key == 'password':
            password = kwargs[key]
    subject = f"eMail Password Recovery"
    message = f"Your password for the login is {password}"
    send_mail(subject, message, 'admin@myblog.com', [email])
    print('email Sent')