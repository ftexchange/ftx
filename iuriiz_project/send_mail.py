import smtplib
import iuriiz_project.data as data


def send_email(message):
    gmail_user = data.gmail_user
    gmail_password = data.gmail_password
    to = data.send_mail_to

    try:
        smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.login(gmail_user, gmail_password)
        smtp_obj.sendmail(gmail_user, to, message)
        smtp_obj.quit()
    except Exception as e:
        print('something went wrong with the mail server: ', e)


def send_funding_email(funding_rates):
    for funding_rate in funding_rates:
        market, funding = funding_rate[0], funding_rate[1]
        subject = f'{market} market'
        text = f'You are loosing money. Last hour funding rate is {funding}%' if funding < 0 else \
            f'All good. Last hour funding rate is {funding}%'
        message = 'Subject: {}\n\n{}'.format(subject, text)
        send_email(message)
