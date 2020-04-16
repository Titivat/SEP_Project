
#use for test run for the project
#deleate when needed 

from ServerConnector import ServerConnector
from Package import Package

if __name__ == '__main__':
    serverConnector = ServerConnector()

    data = Mon( )
    dataSend = Package( 12, data)

    serverConnector.sendData( dataSend )

    reply = serverConnector.getMessage()

    reply.getData( ).setData( 100 )  
    print( reply.getData().getData() )

