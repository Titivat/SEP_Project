
class Package:
    def __init__( self , userId = None, data = ''):
        self.HEADER_LENGTH = 5 
        self.id = userId
        self.data = data

    def setId(self, userId ):
        self.id = userId 

    def setMessage( self, message ):
        self.message = message 

    def setHeaderLength( self, length ):
        self.HEADER_LENGTH = length

    def getData( self ):
        return self.data

    def getId( self ):
        return self.id

    def getHeaderLength(self):
        return self.HEADER_LENGTH

    def getPackage( self ):
        package = f'{ self.id :<{self.HEADER_LENGTH}}' + str(self.message)
        return package