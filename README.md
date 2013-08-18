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

##Progress
* Most thrift function defined (Login, Profile, Room List, Send Message, Long Polling)
* Basic login script (.py)
* Login packet encrypted
* Just discoverd how protocol designed


##TODO
* Everything
* More thrift function definition (Sticker, Make group chat, etc)
