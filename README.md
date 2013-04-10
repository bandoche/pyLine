pyLine
======

NHN Line protocol with Python and thrift [warning: dirty]

##Tech/Protocol
* HTTPS Server
* Apache Thrift (TCompactProtocol)
* RSA for login

[Server] - [Thrift] - (HTTPS) - [Client]

##How to discover
* Modified Host for Line domain to a lazy server
* Lazy Server running HTTPS (nginx)
* dirty PHP Code to redirect request to mitmproxy
* MITMProxy with Reversed proxy to original domain (pip install mitmproxy)
* Line application

##TODO
* Everything
* Just discoverd how protocol designed
* And how Login packet encrypted
