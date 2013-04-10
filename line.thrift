const string HELLO_IN_KOREAN = "an-nyoung-ha-se-yo"
const string HELLO_IN_FRENCH = "bonjour!"
const string HELLO_IN_JAPANESE = "konichiwa!"


struct Unknown {
  1: i32 temp
}

struct loginWithIdentityCredentialForCertificateResult {
  1: bool keepLoggedIn,
  2: i32 systemName,
  3: string certificate 
}

service Line {
	#string loginWithIdentityCredentialForCertificate(1:3:string cr1, 4:string cr2, 5:bool flag1, 6:string ip, 7:string comname, 8: i32 val1 9:string cr5)
	#Unknown testFunc()
	loginWithIdentityCredentialForCertificateResult loginWithIdentityCredentialForCertificate(1:string cr1, 2:string cr2, 3:bool flag1, 4:string ip, 5:string comname, 6: i32 val1 7:string cr5)
}

