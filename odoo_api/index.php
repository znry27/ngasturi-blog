<?php 
	require_once('ripcord-master/ripcord.php');

	$url = 'http://localhost:8069';
	$db = 'tutorial_dua';
	$email = 'agus@gmail.com';
	$password = '123';

	$common = ripcord::client("$url/xmlrpc/2/common");
	$uid = $common->authenticate($db, $email, $password, []);
	
	if(!empty($uid)){
		// echo "Berhasil login dengan User ID : " . $uid . '</br>';

		$models = ripcord::client("$url/xmlrpc/2/object");

		// contoh memanggil method public search
		// $partners = $models->execute_kw($db, $uid, $password, 'res.partner', 'search', [[]]);

		// contoh memanggil method private _search, seharusnya akan muncul pesan error
		// $partners = $models->execute_kw($db, $uid, $password, 'res.partner', '_search', [[]]);


		// Contoh memanggil method dengan decorator @api.multi 
		// dengan record_ids berupa array
		// $partner_record_ids = [9,10];
		// $partner_value = [
		// 	'street' => 'Jl. Rajawali 12',
		// 	'city' => 'Surabaya'
		// ];
		// $values = [$partner_record_ids, $partner_value];

		// $partners = $models->execute_kw($db, $uid, $password, 'res.partner', 'write', $values);

		// contoh memanggil method menggunakan positional argument
		// $partners = $models->execute_kw($db, $uid, $password, 'res.partner', 'search', [[],0,2]);

		// contoh memanggil method menggunakan keyword argument
		// $partners = $models->execute_kw($db, $uid, $password, 'res.partner', 'search', [[]], ['order' => 'name desc','limit' => 2]);

		// contoh memanggil method create pada model res.partner
		// $values = [
		// 	'name' => 'Ngasturi',
		// 	'street' => 'Jl. Semolowaru 12',
		// 	'city' => 'Surabaya'
		// ];
		// $partners = $models->execute_kw($db, $uid, $password, 'res.partner', 'create', [$values]);

		// contoh memanggil method copy
		// $partners = $models->execute_kw($db, $uid, $password, 'res.partner', 'copy', [[14]], ['default' => ['street' => 'Jl. Ahamad Yani 14']]);

		// contoh memanggil method unlink
		// $partners = $models->execute_kw($db, $uid, $password, 'res.partner', 'unlink', [[14]]);

		// contoh memanggil method search dengan domain
		// $domain = [
		// 	['email', 'ilike', 'gmail'],
		// 	['city', '=', 'Surabaya']
		// ];
		// $kwargs = ['order' => 'name desc, street asc', 'limit' => 2];
		// $partners = $models->execute_kw($db, $uid, $password, 'res.partner', 'search', [$domain], $kwargs);

		// $partners = $models->execute_kw($db, $uid, $password, 'res.partner', 'search_count', [$domain]);


		// contoh memanggil method search_read
		$domain = [
			['email', 'ilike', 'gmail'],
			['city', '=', 'Surabaya']
		];
		$kwargs = ['order' => 'name desc, street asc', 'domain' => $domain, 'fields' => ['name', 'city', 'street', 'email']];
		$partners = $models->execute_kw($db, $uid, $password, 'res.partner', 'search_read', [], $kwargs);

		echo "<pre>" . print_r($partners, true) . "</pre>";

	}else{
		echo "Gagal login";
	}
?>