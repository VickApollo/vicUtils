import Chronus
import zipfile
import zlib
import getpass
import socket

class Hephaestus():
    '''
    * Hephaestus is the god of forge and art of sculpture.
    
    Also known as Vulcan.
    
    Hephaestus execute all IO operations and manage LOGS from anothers Classes (GODS).
    
    Class to speed up development
    Hefestus was created to help with util functions, improving code speed
    
    Created: Jul, 12, 2017
    Adjust:
        16/05/2018 - Included Harpocrates support for database connection
    '''
    def __init__(self):
        self._chronus = Chronus.Chronus()
        self.createSelfLog()
        self._user = getpass.getuser()
        self._machine = socket.gethostname()
    
    ### Inner Log - Hefestus Self Management ###################################################################################
    def createSelfLog(self):
        import sqlite3 as sl
        self._logDB = sl.connect('database.db')
        self._logCursor = self._logDB.cursor()
        qry = "CREATE TABLE IF NOT EXISTS HIS_LOG (FUNCTION STRING , PROCESS STRING , MESSAGE STRING , STEP STRING , OBSERVATION STRING , ERROR_NUMBER INT , ERROR_MESSAGE STRING , MACHINE STRING , USER STRING , DATE STRING) "
        self._logCursor.execute(qry)
        qry = 'CREATE TABLE IF NOT EXISTS LOG_INIT (CREATION STRING)'
        self._logCursor.execute(qry)
        
    
    def specEventLog(self , function=None , process=None , message=None , step=None , observation=None , error_number=None , error_message=None , machine=None , user=None , date=None):
        regx = 'INSERT INTO HIS_LOG (FUNCTION , PROCESS , MESSAGE , STEP , OBSERVATION , ERROR_NUMBER , ERROR_MESSAGE , MACHINE , USER , DATE) '
        regx = regx + "VALUES ('{fun}', '{proc}','{msg}','{step}','{obs}','{e_num}','{e_msg}','{mach}','{usr}','{dta}')"
        qry = regx.format(fun= function ,
                    proc= process ,
                    msg= message ,
                    step= step ,
                    obs= observation ,
                    e_num= error_number ,
                    e_msg= error_message ,
                    mach= machine ,
                    usr= user ,
                    dta = self._chronus.dateToString(self._chronus.getDate()) if date == None else date
                    )
        self._logCursor.execute(qry)
        self._logDB.commit()
        
    ### ETL functions ############################################################################################################
    
    def getPandasDataFrame(self , inputConfig=None , outputConfig=None):
        
        ''' Mount in memory Data Frame using Pandas Module
            Function Params:
            1 - InputConfig (Dictionary)
                See pandas documentation for more details about input formats and parameters
                e.g.: 
                       * pd.io.sql.read_sql - For sql sources
                       * pd.read_csv        - For csv sources
                       ...
                
            2 - outputConfig (Dictionary)
                See pandas documentation for more details about output formats and parameters   
                e.g.: 
                       * to_sql      - export to database
                       * to_csv      - export to csv
                       ...
        '''
        
        if output['kind'] == 'sql':
            try:
                import pandas as pd
                base = pd.io.sql.read_sql(**inputConfig)
                base.to_sql(**outputConfig)
                del base
                specEventLog(function='Hephaestus' , process='getPandasDataFrame' , step='sql' , mach=self._machine , usr=self._user )
                return True
            except Exception as e:
                print (e)
                specEventLog(function='Hephaestus' , process='getPandasDataFrame' , step='sql' , 
                             error_message=str(e) , error_number=1 ,
                             machine=self._machine , usr=self._user )
                return False
        elif output['kind'] == 'csv':
            try:
                import pandas as pd
                base = pd.io.sql.read_sql(**inputConfig)
                base.to_csv(**outputConfig)
                del base
                specEventLog(function='Hephaestus' , process='getPandasDataFrame' , step='sql' , mach=self._machine , usr=self._user )
                return True
            except Exception as e:
                print(str(e))
                specEventLog(function='Hephaestus' , process='getPandasDataFrame' , step='sql' , 
                             error_message=str(e) , error_number=1 ,
                             machine=self._machine , usr=self._user )
            
    def readFile(self , file , kind='r'):
        try:
            self._fileReaded = open(file , kind).read()
        except Exception as e:
            print(str(e))
    
    def getFileToString(self):
        '''
            Return the file readed (in-memmory storage)
        '''
        return self._fileReaded
    
    def createFileFromString(filename , content):
        try:
            f = open(filename , 'w')
            f.write(content)
            f.close()
        except Exception as e:
            print(str(e))
        
    
    def createZipFile(self , filename , file_to_zip):
        ''' 
            Method that compress files into Zip files
        '''
        
        try:
            compression = zipfile.ZIP_DEFLATED
        except:
            compression = zipfile.ZIP_STORED

        modes = { zipfile.ZIP_DEFLATED: 'deflated',
                  zipfile.ZIP_STORED:   'stored',
                  }

        zf = zipfile.ZipFile(filename, mode='w')
        
        if len(file_to_zip) == 1 or type(file_to_zip) == str:
            if type(file_to_zip) == str:
                file = file_to_zip
            else:
                file = file_to_zip[0]

            if not zipfile.is_zipfile(file):
                try:
                    print ('compressing {}'.format(file))
                    zf.write(file , compress_type=compression)
                except Exception as e:
                    print(str(e))
                finally:
                    print('Fechando arquivo')
                    zf.close()
        elif len(file_to_zip) > 1:
            for file in file_to_zip:
                if not zipfile.is_zipfile(file):
                    try:
                        print ('compressing {}'.format(file))
                        zf.write(file , compress_type=compression)
                    except Exception as e:
                        print(str(e))
            zf.close()
                    
            
            
    def checkFilesInZip(self , filename):
        zf = zipfile.ZipFile(filename, 'r')
        return zf.namelist()
    
    def zipFileInfo(self , filename):        
        zf = zipfile.ZipFile(filename)
        for info in zf.infolist():
            print (info.filename)
            print ('\tComment:\t', info.comment)
            print ('\tModified:\t', self._chronus.getDateTime(info.date_time))
            print ('\tSystem:\t\t', info.create_system, '(0 = Windows, 3 = Unix)')
            print ('\tZIP version:\t', info.create_version)
            print ('\tCompressed:\t', info.compress_size, 'bytes')
            print ('\tUncompressed:\t', info.file_size, 'bytes')
            print ('\n')
