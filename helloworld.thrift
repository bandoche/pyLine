const string HELLO_IN_KOREAN = "an-nyoung-ha-se-yo"
const string HELLO_IN_FRENCH = "bonjour!"
const string HELLO_IN_JAPANESE = "konichiwa!"

service HelloWorld {
	void ping(),
	string sayHello(),
	string sayMsg(1:string msg)
}
