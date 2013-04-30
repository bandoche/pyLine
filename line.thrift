#method name :  loginWithIdentityCredentialForCertificate
#@ 0 # 0 - STRUCT
#@ 2 # 1 - STRING ( 88 ) =  DsKeAAAAAAAAAAAAAAAA.AAAAAAAAAAAAAAAAAAAAAA.AAAAAAAAAAA+a/AA+AAAAAAAAAAAAAAAAAAAAAAAAAA=
#@ 92 # 5 - I32 (1) =  2
#@ 94 # 0 - STOP

#at all flow init 
#method name :  loginWithVerifierForCertificate
#@ 0 # 0 - STRUCT
#@ 2 # 1 - STRING ( 88 ) =  DsKeAAAAAAAAAAAAAAAA.AAAAAAAAAAAAAAAAAAAAAA.AAAAAAAAAAA+a/AA+AAAAAAAAAAAAAAAAAAAAAAAAAA=
#@ 92 # 2 - STRING ( 64 ) =  5d7b7BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
#@ 158 # 5 - I32 (1) =  2
#@ 160 # 0 - STOP

#method name :  loginWithIdentityCredentialForCertificate
#@ 0 # 0 - STRUCT
#@ 2 # 3 - STRING ( 32 ) =  rHMIGCCCCCCCCCCCCCCCCCCCCCCCCCCC
#@ 36 # 4 - STRING ( 4 ) =  5210
#@ 42 # 5 - I32 (1) =  6
#@ 44 # 0 - STOP

#@ 0 # 1 - STRUCT
#@ 1 # 2 - I32 (1) =  36
#@ 3 # 3 - STRING ( 38 ) =  Account ID and password does not match
#@ 43 # 0 - STOP
#method name :  loginWithIdentityCredentialForCertificate
#@ 0 # 1 - STRUCT
#@ 1 # 2 - I32 (1) =  40
#@ 3 # 3 - STRING ( 14 ) =  Internal error
#@ 19 # 0 - STOP

struct loginWithIdentityCredentialForCertificateResult {
  1: string certificate, # real X-Line-Access key for communitation. DsKeAAAAAAAAAAAAAAAA.AAAAAAAAAAAAAAAAAAAAAA.AAAAAAAAAAA+a/AA+AAAAAAAAAAAAAAAAAAAAAAAAAA=
  2: string key64, #unknown. only offered when login with verifier for querying certificate at first stage. (need verifier)
  3: string verifier, # aka. verifier. temp, rHMIGCCCCCCCCCCCCCCCCCCCCCCCCCCC
  4: string auth_digit, # 5210
  5: i32 code # 3(6): need auth? 1(2): correct login
}



struct getProfileResult {
  1: string key33, # 33 byte key ( uac06..... )
  2: i32 errcode,
  3: string line_id, # line account
  10: string basekey24, # 24 byte base64ed key
  12: string region, # 2 byte code for country. KR for korea
  20: string name, # name in line profile
  21: string today_message, #not sure. today message seems to
  22: string timecode, #unknown. seemds timestamp but not
  24: string blank2, #unknown2
  31: bool flag1, #??
  32: bool flag2, #??
  33: string profile_url #39 byte (maybe dynamic) url for profile image - gd2.line.naver.jp/[[profile_url]]
}


struct getServerTimeResult {
  1: i64 server_time
}

struct getLastOpRevisionResult {
  1: i64 last_op_rev
}



service Line {
	#string loginWithIdentityCredentialForCertificate(1:3:string cr1, 4:string cr2, 5:bool flag1, 6:string ip, 7:string comname, 8: i32 val1 9:string cr5)



#method name :  loginWithIdentityCredentialForCertificate
#@ 0 # 3 - STRING ( 9 ) =  100007673
#@ 11 # 4 - STRING ( 202 ) =  1dcAAA202AAADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
#@ 216 # 5 - BOOL bool - false
#@ 217 # 6 - STRING ( 13 ) =  172.20.100.30
#@ 232 # 7 - STRING ( 8 ) =  comnames
#@ 242 # 8 - I32 (1) =  4
#@ 244 # 9 - STRING ( 64 ) =  5d7b7BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
#@ 310 # 0 - STOP

#@ 0 # 3 - STRING ( 9 ) =  100007672
#@ 11 # 4 - STRING ( 202 ) =  1dcAAA202AAADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
#@ 216 # 5 - BOOL bool - false
#@ 217 # 6 - STRING ( 11 ) =  172.20.10.3
#@ 230 # 7 - STRING ( 8 ) =  comnames
#@ 240 # 8 - I32 (1) =  4 //
#@ 242 # 9 - STRING (0)

  loginWithIdentityCredentialForCertificateResult loginWithIdentityCredentialForCertificate
  (1:string str1, 
    2:string str2, 
    3:string rsakey1, 
    4:string rsacipher, 
    5:bool b5, 
    6:string ip, 
    7:string comname, # not sure, is it type of login method? (2 or normal, others for qr or else?? )
    8:i32 i8, 
    9:string str9) 
#  loginWithIdentityCredentialForCertificateResult loginWithIdentityCredentialForCertificate(1:string cr1, 2:string cr2, 3:bool flag1, 4:string ip, 5:string comname, 6: i32 val1 7:string cr5)





#method name :  loginWithVerifierForCertificate
#@ 0 # 3 - STRING ( 32 ) =  rHMIGCCCCCCCCCCCCCCCCCCCCCCCCCCC
#@ 34 # 0 - STOP
  loginWithIdentityCredentialForCertificateResult loginWithVerifierForCertificate(3: string verifier)
  getProfileResult getProfile()
  i64 getServerTime()
  i64 getLastOpRevision()
  list<string> getAllContactIds()
}

