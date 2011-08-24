import unittest
import minimock

from databasetest import DatabaseTestSetup

from dbtripwire import model

from dbtripwire import tripwire

#needed to create mock
import smtplib #@UnusedImport
import datetime

class RMSTest(unittest.TestCase):
    '''Test the RMS calculations'''
    
    def testRMSCalc(self):
        testvalues = [
                      ([0], 0),
                      ([1], 1),
                      ([2], 2),
                      ([0, 0], 0),
                      ([1, 1], 1),
                      ([0] * 20, 0),
                      ([1] * 20, 1),
                      ([0, 0, 0, 1], 0.5),
                      ([3, 1, 3, 0, 1], 2),
                      ]
        
        for values, expected in testvalues:
            result = tripwire.calcRMS(values)
            self.assertAlmostEqual(result, expected, msg='rmsCalc(%s) gave %s, expected %s' % (values, result, expected))
            

class SendEmailTest(unittest.TestCase):
    '''Test sending email'''
    
    def testSendEmail(self):
        tt = minimock.TraceTracker()
        smtpconn = minimock.Mock('smtplib.SMTP', tracker=tt)
        minimock.mock('smtplib.SMTP', mock_obj=smtpconn)
        smtpconn.mock_returns = smtpconn
        smtpconn.sendmail.mock_returns = {}
        
        tripwire.sendEmail(2.5, datetime.date(2011, 8, 16))
        expected = r"""Called smtplib.SMTP('localhost')
Called smtplib.SMTP.sendmail(
    'lee@beggdigital.co.nz',
    ['lee@beggdigital.co.nz', 'llnz@paradise.net.nz'],
    'Content-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\nSubject: [DBTW] Tripwire Report 2011-08-16\nTo: lee@beggdigital.co.nz, llnz@paradise.net.nz\nFrom: lee@beggdigital.co.nz\n\nDatabase trip wire has been tripped.\n\nRMS value was: 2.5\n')
Called smtplib.SMTP.quit()"""
        self.assertTrue(tt.check(expected), tt.diff(expected))
        
        minimock.restore()
        
    def testSendEmailFailure(self):
        tt = minimock.TraceTracker()
        smtpconn = minimock.Mock('smtplib.SMTP', tracker=tt)
        minimock.mock('smtplib.SMTP', mock_obj=smtpconn)
        smtpconn.mock_returns = smtpconn
        smtpconn.sendmail.mock_returns = {'lee@beggdigital.co.nz': ( 550 ,"User unknown" )}
        
        tripwire.sendEmail(2.5, datetime.date(2011, 8, 16))
        
        expected = r"""Called smtplib.SMTP('localhost')
Called smtplib.SMTP.sendmail(
    'lee@beggdigital.co.nz',
    ['lee@beggdigital.co.nz', 'llnz@paradise.net.nz'],
    'Content-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\nSubject: [DBTW] Tripwire Report 2011-08-16\nTo: lee@beggdigital.co.nz, llnz@paradise.net.nz\nFrom: lee@beggdigital.co.nz\n\nDatabase trip wire has been tripped.\n\nRMS value was: 2.5\n')
Called smtplib.SMTP.quit()"""
        self.assertTrue(tt.check(expected), tt.diff(expected))
        
        minimock.restore()
    
class TripwireTest(DatabaseTestSetup, unittest.TestCase):
    '''Test the main tripwire function'''
    
    def setUp(self):
        #setup the database
        super(TripwireTest, self).setUp()
        
        #setup the data
        
        self.session = model.Session()
        self.session.add(model.MeasuredValue(1))
        self.session.add(model.MeasuredValue(2))
        self.session.add(model.MeasuredValue(0))
        self.session.add(model.MeasuredValue(2))
        
        self.session.commit()
        
    #The default tearDown takes care of the data
    
    def testTripwireNormal(self):
        '''Tripwire test, not tripped'''
        tt = minimock.TraceTracker()
        minimock.mock('tripwire.sendEmail', tracker=tt)
        
        tripwire.main()
        
        self.assertTrue(tt.check(''), tt.diff(''))
        
        minimock.restore()
        
    def testTripwireTripped(self):
        '''Tripwire test, tripped'''
        tt = minimock.TraceTracker()
        minimock.mock('tripwire.sendEmail', tracker=tt)
        
        datevalue = datetime.date(2011, 8, 16)
        
        dtmock = minimock.Mock('datetime.date')
        minimock.mock('datetime.date', mock_obj=dtmock)
        dtmock.mock_returns = dtmock
        dtmock.today.mock_returns = datevalue
        dtmock.today.mock_tracker = tt
        #can't just do minimock.mock('datetime.date.today', returns=datevalue, tracker=tt)
        #because datetime.date is in an extension (ie, not native python)
        
        #Add another value to make the tripwire trip
        self.session.add(model.MeasuredValue(6))
        self.session.commit()
        
        tripwire.main()
        expected = r'''Called datetime.date.today()
Called tripwire.sendEmail(3.0, datetime.date(2011, 8, 16))'''
        self.assertTrue(tt.check(expected), tt.diff(expected))
        
        minimock.restore()
        