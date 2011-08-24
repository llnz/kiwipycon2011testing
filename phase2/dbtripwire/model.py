
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dbtripwire import settings


#database setup
Base = declarative_base()
    
engine = sqlalchemy.create_engine(settings.DATABASE_URL, pool_recycle=3600)

Session = sessionmaker(bind=engine)

def initDatabase():
    '''Create the database tables'''
    Base.metadata.create_all(engine)
    
    #any other database setup here
    
def dropDatabase():
    '''Drop the database tables'''
    #extra database clean up here
    Base.metadata.drop_all(engine)

#Model here
class MeasuredValue(Base):
    '''Measured Values table data'''
    __tablename__ = 'measuredvalue'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    value = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    
    def __init__(self, value):
        '''Constructor
        
        @param value: the value of this measurement
        '''
        self.value = value
        
    def __repr__(self):
        return "<MeasuredValue(%s, %s)>" % (self.id, self.value)
    

   
