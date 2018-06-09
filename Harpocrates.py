import configparser
from Hephaestus import Hephaestus
import datetime as dt
import getpass
import socket


class Harpocrates():
    '''
        * Harpocrates is the god of silence and secrets.

         Also known as Horus.

        * Harpocrates manage all database logins by reading a config file.

    '''
    def __init__(self):
        self._user = getpass.getuser()
        self._machine = socket.gethostname()
        self._log = Hephaestus()
        self._log.createSelfLog()
        self._log.specEventLog(
                               function='Harpocrates' , 
                               process='init_function' , 
                               machine=self._machine , 
                               user=self._user
        )
        self._config = configparser.ConfigParser()
        self._pathConfig = '.'
        
    def getDatabaseInfo(self , section='MAIN' , company='HOME' , domain=False):
        self._log.specEventLog(
                               function='Harpocrates' , 
                               process='getDatabaseInfo' , 
                               observation='AMBIENTE: {amb} - COMPANIA {cmp}'.format(section , company)
                               machine=self._machine , 
                               user=self._user
        )
        self._config.read('{}\\{}'.format(self._pathConfig , self._configFileName))
        p_user = 'USR'
        p_pswd = 'PSR'
        
        user  = self._config.get(section , p_user)
        pasw  = self._config.get(section , p_pswd)
        ip    = self._config.get(section , 'IP')
        porta = self._config.get(section , 'PORTA')
        sid   = self._config.get(section , 'SID')
        kind  = self._config.get(section , 'TECNOLGIA')
        
        return {'usr':user , 'pasw':pasw , 'ip':ip , 'port':porta , 'sid':sid , 'kind':kind}
    
    def setDirectory(self , path='.'):
        self._pathConfig = path
        
    def setConfigFileName(self , name='database.ini'):
        set._configFileName = name
        
    def getDirectory(self):
        return self._pathConfig
    
    def getConfigFileName(self):
        return self._configFileName
    
    
        
        
        
    
        
    