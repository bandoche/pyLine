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
import socks
import sqlite3

try:
    #query in Line.db
    sqconn = sqlite3.connect('Line.db')

    c = sqconn.cursor()

    c.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='version_table' ''')
    table = c.fetchall()
    if len(table) == 0:
        #table is not exist. create at here
        c.execute('''CREATE TABLE IF NOT EXISTS version_table (table_name varchar(100) PRIMARY KEY, version varchar(50))''')
        c.execute('''INSERT INTO version_table (table_name, version) VALUES ('cert', \'1.0\')''')
        sqconn.commit()


    c.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='cert' ''')
    table = c.fetchall()
    if len(table) == 0:
        #table is not exist. create at here
        c.execute('''CREATE TABLE IF NOT EXISTS cert (pid integer primary key autoincrement, userid text, data text)''')
        sqconn.commit()

    #useless but check version
    c.execute('''SELECT * FROM version_table WHERE table_name ='cert' and version='1.0' ''')
    row = c.fetchall()
    if len(row) == 0:
        #version mismatch
        print "db version mismatch! terminate."
        sqconn.close()
        sys.exit()

    # sqconn.close()
    # sys.exit()




    # Make socket
    # make Reverse proxy for NHN Line (gd2.line.naver.jp) if you want to see the traffic. otherwise, just connect to https://gd2.line.naver.jp

    transport = THttpClient.THttpClient('http://localhost:8080/api/v4/TalkService.do')
    # transport = THttpClient.THttpClient('http://localhost:30303/')

    # this is important. Line server won't allow you to connect unless acceptable Line Application. We pretend to Line for OS X
    version_string = "3.1.4.76"
    version_string = "3.1.6.0"
    user_agent = 'DESKTOP:MAC:LEOPARD-x64(' + version_string + ')'
    header_line_application = "DESKTOPMAC\t" + version_string + "\tMAC\tLEOPARD-x64"
    transport.setCustomHeaders({'User-Agent': user_agent, 'X-Line-Application': header_line_application})
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    # NHN Line use thrift / compact protocol
    protocol = TCompactProtocol.TCompactProtocol(transport)

    # Create a client to use the protocol encoder
    client = Line.Client(protocol)

    # Connect!
    transport.open()


    # get user account name
    email = raw_input('mail(user id): ')

    # look up cert for userid in db
    c.execute('''SELECT * FROM cert WHERE userid = ? ''', (email,))
    sq_cert = c.fetchall()
    if len(sq_cert) == 1:
        print "find certificate key in db"
        cert = sq_cert[0][2]
    else:

        # get json - get public key for rsa
        hc = httplib2.Http(proxy_info = httplib2.ProxyInfo(proxy_type=socks.PROXY_TYPE_HTTP, proxy_host='localhost', proxy_port=8080), disable_ssl_certificate_validation=True)
        resp, content = hc.request('https://gd2.line.naver.jp/authct/v1/keys/naver', "POST")
        get_json = json.loads(content)

        session_key = get_json['session_key']
        rsa_key = get_json['rsa_key'].split(',')
        keyname = rsa_key[0]
        evalue = rsa_key[1]
        nvalue = rsa_key[2]

        # fetching keys
        password = getpass.getpass('password: ')

        # encryption process
        # todo: unicode? string? - working with str()
        passkey = str(chr(len(session_key)) + session_key + chr(len(email)) + email + chr(len(password)) + password)
        pub_key = rsa.PublicKey(int(evalue, 16), int(nvalue, 16))
        cipher = rsa.encrypt(passkey, pub_key)

        ip = socket.gethostbyname(socket.gethostname())
        # comname - your computer name
        comname = "pyLine"
        #session_key - something be taken after proper login - i think it is not used for initial login. it is retrieved after another authorization
        # session_key = "0000000000000000000000000000000000000000000000000000000000000000"

        msg = client.loginWithIdentityCredentialForCertificate(str1=None, str2=None, rsakey1=keyname, rsacipher=cipher.encode("hex"), b5=True, ip=ip, comname=comname, i8=2, str9='')
        print ("(loginWithIdentityCredentialForCertificate) = ", msg)

        if msg.code == 3:
            # 4 digit 보여주기
            print ("input ", msg.auth_digit, " from your mobile phone Line app in 2 minutes.")

            # wait until q request
            headers = {'X-Line-Access': msg.verifier, 
                'User-Agent': user_agent, 
                'X-Line-Application': header_line_application,
                }
            resp, content = hc.request('https://gd2.line.naver.jp/Q', "GET", headers=headers)
            get_json = json.loads(content)
            verifier = get_json['result']['verifier']
            print verifier

            # get certificate from verifier

            msg = client.loginWithVerifierForCertificate(verifier=verifier)
            print msg
            cert = msg.certificate

            # add certificate
            c.execute('''INSERT INTO cert (userid, data) VALUES (?, ?)''', (email, msg.certificate))
            sqconn.commit()
            print "saved in db"
        else:
            # sth wrong
            print "something wrong."
            sys.exit(1)

            # query certificate with verifier "loginWithVerifierForCertificate"

    #now we have certificate at here

    #setting header
    headers = {'X-Line-Access': cert, 
        'User-Agent': user_agent, 
        'X-Line-Application': header_line_application,
        }
    transport.close()
    transport = THttpClient.THttpClient('http://localhost:8080/api/v4/TalkService.do')
    transport.setCustomHeaders(headers)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TCompactProtocol.TCompactProtocol(transport)
    client = Line.Client(protocol)
    transport.open()


    #get profile
    profile = client.getProfile()
    print profile
    


    transport.close()

except Thrift.TException, tx:
    print ("%s" % (tx.message))
