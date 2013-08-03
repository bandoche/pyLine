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


#@ 3 # 8 - STRING ( 33 ) =  ua5...
#@ 38 # 9 - I64 (1) =  1349...
#@ 45 # 17 - I32 (1) =  0
#@ 47 # 18 - I32 (1) =  2
#@ 49 # 28 - I32 (1) =  2
#@ 51 # 29 - STRING ( 9 ) =  name
#@ 62 # 31 - STRING ( 13 ) =  1349...
#@ 77 # 33 - STRING (0)
#@ 79 # 35 - I64 (1) =  0
#@ 81 # 38 - BOOL bool - false
#@ 82 # 39 - BOOL bool - false
#@ 83 # 40 - BOOL bool - false
#@ 84 # 41 - BOOL bool - false
#@ 85 # 42 - I32 (1) =  0
#@ 87 # 43 - I64 (1) =  0
#@ 89 # 44 - STRING ( 39 ) =  /os/p/ua5...

struct contact {
  1: string key33, # 33 byte key (uac06...)
  2: i64 timecode2, # not sure (1349...)
  10: i32 flag1, # 0, 3, 4
  11: i32 flag2, #??
  21: i32 flag3, #??
  22: string name, #name in line profile
  24: string timecode, # not sure but little diff. is it last update?
  26: string today_message, # today message
  28: i64 flag4, #??
  31: bool flag5,
  32: bool flag6,
  33: bool flag7,
  34: bool flag8,
  35: i32 flag9,
  36: i64 flag10,
  37: string profile_url
}

#@ 5 # 5 - STRING ( 33 ) =  r49...
#@ 40 # 9 - I64 (1) =  0
#@ 42 # 10 - I64 (1) =  0
#@ 44 # 11 - I64 (1) =  1365...
#@ 51 # 12 - I32 (1) =  0
#@ 53 # 13 - I32 (1) =  2
#@ 55 # 14 - LIST
#@ 56 # 15 - STRUCT
#@ 57 # 16 - STRING ( 33 ) =  uac...
#@ 92 # 17 - STRING ( 33 ) =  r49...
#@ 127 # 18 - I32 (1) =  2
#@ 129 # 19 - STRING ( 12 ) =  278...
#@ 143 # 20 - I64 (1) =  1365...
#@ 150 # 21 - I64 (1) =  0
#@ 152 # 25 - STRING ( 130 ) =  msg
#@ 285 # 29 - BOOL bool - false
#@ 286 # 30 - I32 (1) =  0
#@ 288 # 33 - MAP


struct unknown_struct2 {
  1: string key33, # room title or room master
  2: string key33_2, # me. so it seems list for joined member
  3: i32 var1, #0x02
  4: string stamp12, #278....
  5: i64 stamp_2, #1365...
  6: i64 var2, #0x00
  7: string msg, #what message i send(?)
  11: bool flag1, #??
  12: i32 var3, #0x00
  15: map<string, string> seq, #seq, 4013
}

struct unknown_struct3 {
  1: string key33, 
  2: i64 var1,
  5: bool flag1,
  6: bool flag2,
  7: bool flag3,
  8: bool flag4,
  9: i32 var2,
  10: i64 var3
}

struct msgbox_item_str {
  1: string room_key33, #if 1:1 user chat room, it takes user_key33, else it takes room_key33
  5: i64 var1, #0
  6: i64 unread_count, #0x06 = 3? - unread msg count(?)
  7: i64 var3, #1365...
  8: i32 var4, #0x00
  9: i32 msgbox_type, # 0 for user, 1 for room (group)
  10: list<unknown_struct2> key33s, #??
  11: string var6, #null
  12: list<unknown_struct3> unknown_list4 #four structure in here
}

struct msgbox_str {
  1: msgbox_item_str msgbox_item,
}

struct unknown_struct_back {
  1: string key33, #r49...
  5: i64 var1, #0
  6: i64 var2, #0
  7: i64 var3, #1365...
  8: i32 var4, #0x00
  9: i32 var5, #0x02
  10: list<unknown_struct2> key33s, #??
  11: string var6, #null
  12: list<unknown_struct3> unknown_list4 #four structure in here
}




struct getMessageBoxCompactWrapUpListResult {
  1: list<msgbox_str> msgbox_list #it has two items in list
}


struct sendMessageResult {
  1: string user_key33,
  4: string stamp_12,
  5: i64 var1,
  6: i64 code, #0x00
  14: bool flag1, #false
  15: i32 code2
}

struct getNextMessagesResult {
  1: list<string> user_key33s,
  2: string room_key33,
  3: i32 var1,
  4: string timecode,
  5: i64 timecode2,
  6: i64 code, #0x00
  10: string msg,
  14: bool flag1,
  15: i32 var2,
  18: map<string, string> seq
}

struct fetch_struct {
  1: i64 var1,
  2: i64 var2,
  3: i32 var3,
  4: i32 var4,
  10: string user_key33,
  11: string timecode,
  12: i64 var5,
  13: i64 var6,
  14: i32 var7,
  15: i32 var8
}

struct fetchOperationsResult {
  # two structures in one list
  1: list<string> item1,  
  2: fetch_struct item2
}

struct send_msg_str {
  1: string my_key33, 
  2: string room_key33, 
  10: string msg, 
  15: i32 code
}


struct getRoomResult {
  1: string room_key33,
  2: i64 var1,
  10: list<contact> room_member
}

struct msg_str {
  1: string user_key33,
  2: string room_key33,
  3: i32 param1,
  4: string msg_seq, # unique msg sequence - it needs for original image download in https://os.line.naver.jp/os/m/{msg_seq}
  5: i64 timestamp, # unixtime * 100 for microsecond
  6: i64 param3,
  10: string message,
  14: bool flag1,
  15: i32 flag_file,
  17: string file_content,
  18: map<string, string> seq
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
  list<contact> getContacts(2: list<string> contact_ids)

  getMessageBoxCompactWrapUpListResult getMessageBoxCompactWrapUpList(2:i32 param1, 3:i32 param2)

  sendMessageResult sendMessage(1: i32 var1, 2: send_msg_str msgs)
#  sendMessageResult sendMessage(1: i32 var1, 2: string my_key33, 3: string room_key33, 11: string msg, 16: i32 code)
  getNextMessagesResult getNextMessages(2: string room_key33, 3: i64 timecode)
  fetchOperationsResult fetchOperations(2:i64 param1, 3: i32 param2)
  void sendChatChecked(1: i32 param1, 2: string room_key33, 3: string timecode)
  getRoomResult getRoom(2: string room_key33)
  list<msg_str> getRecentMessages(2:string room_key33, 3:i32 param1)
}

