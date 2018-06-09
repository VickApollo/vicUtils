import datetime as dt



class Chronus():
    '''
        Chronus is the god of time, many times misconfused with Cronos, the Titan.
        
        Chronus manage all date and time handling
    '''
    
    def __init__(self):
        pass
        
    def getNow(self):
        '''
         Method that returns now (system calendar) date and time
         
         return Datetime : Current Date and Time
        '''
        return dt.datetime.now()
        
    def dateToString(self , date , format='%d/%m/%Y'):
        '''
        Method to parse a datetime to an string 
        
        return String: default format = Day / Month / Year
        '''
        return date.strftime(format)
    
    def checkIsDate(self , date):
        '''
            Method to validate if the date is in datetime type
            
            return Boolean: True | False
        '''
        
        if type(date) == datetime.datetime:
            return True
        else:
            return False
        
    def stringToDate(self , str='19000101' , format='%y%m%d'):
        '''
            Method to parse string to a date
            
            return Date : default format (Year month day)
        '''
        
        return datetime.datetime.strptime(str, format).date()
