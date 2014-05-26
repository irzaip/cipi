from socket import *
import thread

BUFF = 1024
HOST = '127.0.0.1'# must be input parameter @TODO
PORT = 9999 # must be input parameter @TODO
def response(key):
    return 'this_is_the_return_from_the_server'

def handler(clientsock,addr):
    while 1:
        data = clientsock.recv(BUFF)
        #print 'data:' + repr(data)
        try:
            instr = instr + str(repr(data))
            if repr(data) == chr(13):
                instr = instr.split("#")
                instr = instr[len(instr)-1]
                print instr
        except:
            pass
        if not data: break
        clientsock.send(response(''))
        #print 'sent:' + repr(response(''))
        # clientsock.close() # - reports [Errno 9] Bad file descriptor as it looks like that socket is trying to send data when it is already closed

if __name__=='__main__':
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    while 1:
        print 'waiting for connection...'
        clientsock, addr = serversock.accept()
        print '...connected from:', addr
        thread.start_new_thread(handler, (clientsock, addr))
