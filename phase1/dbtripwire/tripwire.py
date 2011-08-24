

import math
import datetime
from email.mime.text import MIMEText
import smtplib

import model
import settings

def main():
    '''Check the tripwire, email if the latest values have an RMS value over 2'''
    
    session = model.Session()
    
    values = session.query(model.MeasuredValue).order_by(model.MeasuredValue.desc()).limit(20).all()
    
    totalsq = 0
    for value in values:
        totalsq += value.value**2
        
    rms = math.sqrt(totalsq)
    
    if rms > 2:
        body = """Database trip wire has been tripped

RMS value was: %s
"""
        subject = "Tripwire report %s" % datetime.date.today()
    
        msg = MIMEText(body)
        msg['Subject'] = '[DBTW] %s' % subject
        msg['To'] = ', '.join(settings.TO_ADDRESSES)
        msg['From'] = settings.FROM_ADDRESS
    
        server = smtplib.SMTP('localhost')
        result = server.sendmail(settings.FROM_ADDRESS, settings.TO_ADDRESSES, msg.as_string())
        if len(result) != 0:
            print "sendmail failures: %s" % result
        server.quit()
