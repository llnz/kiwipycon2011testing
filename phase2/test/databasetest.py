import unittest

from sqlalchemy import MetaData

#override database setting
from dbtripwire import settings
settings.DATABASE_URL = 'sqlite:///:memory:'

from dbtripwire.model import initDatabase, dropDatabase, engine, Base

class TestCreateDB(unittest.TestCase):
    '''Test database level functions'''

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testCreateDatabase(self):
        '''Test the database is created and deleted'''
        metadata = MetaData(engine)
        metadata.reflect()
        tablenames = [t.name for t in metadata.sorted_tables]
        self.assertEqual(len(tablenames), 0)
        
        initDatabase()
        metadata = MetaData(engine)
        metadata.reflect()
        tablenames = [t.name for t in metadata.sorted_tables]
        self.assertNotEqual(len(tablenames), 0)

        dropDatabase()
        metadata = MetaData(engine)
        metadata.reflect()
        tablenames = [t.name for t in metadata.sorted_tables]
        self.assertEqual(len(tablenames), 0)
        
class DatabaseTestSetup(object):
    '''Create the database in the setUp, and drop it in tearDown
    
    Used to abstract this away from all the unittests that use the Database.
    
    Must be the first class inherited from, or TestCase will override these 
    methods, not the other way around.
    '''
    
    def setUp(self):
        '''Initialise the database with the tables'''
        initDatabase()


    def tearDown(self):
        '''Drop the tables'''
        dropDatabase()

if __name__ == "__main__":
    unittest.main()