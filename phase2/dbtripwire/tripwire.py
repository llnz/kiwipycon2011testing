

import math
import datetime
from email.mime.text import MIMEText
import smtplib

import model
import settings

def sendEmail(rms, date):
    '''Send an email with the RMS value and date'''
    body = """Database trip wire has been tripped.

RMS value was: %s
""" % rms

    subject = "Tripwire Report %s" % date

    msg = MIMEText(body)
    msg['Subject'] = '[DBTW] %s' % subject
    msg['To'] = ', '.join(settings.TO_ADDRESSES)
    msg['From'] = settings.FROM_ADDRESS

    server = smtplib.SMTP('localhost')
    result = server.sendmail(settings.FROM_ADDRESS, settings.TO_ADDRESSES, msg.as_string())
    if len(result) != 0:
        print "sendmail failures: %s" % result
    server.quit()

def calcRMS(values):
    totalsq = 0.0
    for value in values:
        totalsq += value**2
        
    rms = math.sqrt(totalsq/len(values))
    return rms

def main():
    '''Check the tripwire, email if the latest values have an RMS value over 2'''
    
    session = model.Session()
    
    values = session.query(model.MeasuredValue).order_by(model.MeasuredValue.id.desc()).limit(20).all()
    
    rms = calcRMS([value.value for value in values])
    
    if rms > 2:
        sendEmail(rms, datetime.date.today())
