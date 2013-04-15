#!/usr/bin/env python

import sys
sys.path.append('../gen-py')

from line import Line
from line.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.server import THttpServer
from thrift.protocol import TBinaryProtocol
from thrift.protocol import TCompactProtocol
from thrift.server import TServer


import socket


class LineHandler:
  def __init__(self):
    self.log = {}


  def loginWithIdentityCredentialForCertificate(self, str1, str2, rsakey1, rsacipher, b5, ip, comname, i8, str9):
    print "loginWithIdentityCredentialForCertificate() - ", str1, str2, rsakey1, rsacipher, b5, ip, comname, i8, str9

    result = loginWithIdentityCredentialForCertificateResult(key64=None, code=3, line_access=None, verifier='VERIFIERzzzzzzzzzzzzzzzzzzzzzzzz', auth_digit='8190')
    return result


handler = LineHandler()
processor = Line.Processor(handler)
#transport = TSocket.TServerSocket(port=30303)
#tfactory = TTransport.TBufferedTransportFactory()
pfactory = TCompactProtocol.TCompactProtocolFactory()

server = THttpServer.THttpServer(processor, ('', 30303), pfactory)
print "Starting python server..."
server.serve()
print "done!"
