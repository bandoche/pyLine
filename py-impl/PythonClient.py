# -*- coding:utf-8 -*-
#!/usr/bin/env python
import sys
sys.path.append('../gen-py')

from line import Line
from line.ttypes import *
from line.constants import *

from thrift import Thrift
from thrift.transport import TTransport
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol

import httplib2
import json
import rsa
import getpass
import socket

try:
    # Make socket
    # make Reverse proxy for NHN Line (gd2.line.naver.jp) if you want to see the traffic. otherwise, just connect to https://gd2.line.naver.jp
    transport = THttpClient.THttpClient('http://localhost:8080/api/v4/TalkService.do')

    # this is important. Line server won't allow you to connect unless acceptable Line Application. We pretend to Line for OS X
    transport.setCustomHeaders({'User-Agent': 'DESKTOP:MAC:LEOPARD-x64(3.1.4.76)', 'X-Line-Application': 'DESKTOPMAC	3.1.4.76	MAC	LEOPARD-x64'})
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    # NHN Line use thrift / compact protocol
    protocol = TCompactProtocol.TCompactProtocol(transport)

    # Create a client to use the protocol encoder
    client = Line.Client(protocol)

    # Connect!
    transport.open()

    # get json - get public key for rsa
    hc = httplib2.Http()
    resp, content = hc.request('https://gd2.line.naver.jp/authct/v1/keys/naver', "POST")
    get_json = json.loads(content)

    session_key = get_json['session_key']
    rsa_key = get_json['rsa_key'].split(',')
    keyname = rsa_key[0]
    evalue = rsa_key[1]
    nvalue = rsa_key[2]

    # get user account name
    email = raw_input('mail(user id): ')
    password = getpass.getpass('password: ')

    # encryption process
    # todo: unicode? string? - working with str()
    passkey = str(chr(len(session_key)) + session_key + chr(len(email)) + email + chr(len(password)) + password)
    pub_key = rsa.PublicKey(int(evalue, 16), int(nvalue, 16))
    cipher = rsa.encrypt(passkey, pub_key)

    netaddr = socket.gethostbyname(socket.gethostname())
    # comname - your computer name
    comname = "comname"
    #session_key - something be taken after proper login - i think it is not used for initial login. it is retrieved after another authorization
    session_key = "0000000000000000000000000000000000000000000000000000000000000000"

    msg = client.loginWithIdentityCredentialForCertificate(None, None, keyname, cipher.encode("hex"), True, netaddr, comname, 2, '')
    print ("(loginWithIdentityCredentialForCertificate) = ", msg)

    transport.close()

except Thrift.TException, tx:
    print ("%s" % (tx.message))
