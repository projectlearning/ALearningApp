var pattern = {
	mobile: /^1\d{10}$/,
  	email: /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/,
}

var encrypt = function (str){
	return hex_md5(str);
}