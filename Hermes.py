class Hermes():
    '''
        * Hermes is the god of communication, transportation and commerce.

        * Also known as Mercury by the Romans

        About the class:

        Hermes manage all database comunications and data exports.

    '''

    def __init__(self):
        pass
        
    ### Database Specifications #################################################################################################
    def connectDatabaseString(self , kind , string ):
        ''' kind { 'ORACLE' , 'SQL SERVER' , 'MY SQL' , 'POSTGREE'} '''
        self._kindConn = str(kind).upper()
        if self._kindConn == 'ORACLE':
            import cx_Oracle as cx
            try:
                self._conn = cx.Connection(string)
            except Exception as e:
                print e
                raise

    def connectDatabase(self , database_name  , company):
        ''' Visit Harpocrates to see what databases you can work '''
        import Harpocrates
        
        hp = Harpocrates()
        args = hp.getDatabaseInfo(database_name , company)
        self._kindConn = args['kind']
        if self._kindConn == 'ORACLE':
            try:
                dsn = cx.makedsn(args['ip'] , args['port'] , args['sid'])
                self._conn = cx.connect(args['usr'] , args['pasw'] , dsn)
            except Exception as e:
                print(str(e))


    def closeDatabaseConnection(self):
        if self._kindConn == 'ORACLE':
            try:
                self._cursor.close()
            except Exception as e:
                print e
            try:
                self._conn.close()
            except Exception as e:
                print e
                raise
                
    def getDatabaseConnection(self):
        return self._conn
    
    def openCursor(self):
        if self._kindConn == 'ORACLE':
            self._cursor = self._conn.cursor()
    
    def executeSQL(self , qry):
        if self._kindConn == 'ORACLE':
            self._cursor.execute(qry)
        
    def closeCursor(self):
        if self._kindConn
        
        def sendMessage(self):
        pass
    
    def setMessage(self , content):
        self._content = content
    
    def configContentDisplay(self, configDisplay):
        self._configDisplay = configDisplay
    
    def configOutputMode( self , configOutput ):
        self._configOutput = configOutput
        
    def configInputMode(self , configInput):
        self._configInputMode = configInputMode
        
        