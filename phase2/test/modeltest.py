

import unittest

from databasetest import DatabaseTestSetup

from dbtripwire import model

class ModelTest(DatabaseTestSetup, unittest.TestCase):
    '''Test the model classes'''
    
    def testMeasuredValueTable(self):
        '''MeasuredValue table test'''
        
        session = model.Session()
        
        self.assertEqual(session.query(model.MeasuredValue).count(), 0)
        
        mv = model.MeasuredValue(5)
        self.assert_(mv)
        
        session.add(mv)
        session.commit()
        
        self.assertEqual(session.query(model.MeasuredValue).count(), 1)
        
        mv1 = session.query(model.MeasuredValue).one()
        self.assertEqual(mv1.id, 1)
        self.assertEqual(mv1.value, 5)
        #don't forget to test the __repr__ string
        self.assertEqual(repr(mv1), "<MeasuredValue(1, 5)>")
        
        session.delete(mv1)
        
        session.commit()
        
        self.assertEqual(session.query(model.MeasuredValue).count(), 0)
        
