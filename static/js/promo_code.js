var updateBtnsPromo = document.getElementsByClassName('update-promo')

for (i = 0; i < updateBtnsPromo.length; i++) {
	updateBtnsPromo[i].addEventListener('click', function(){
        var code = document.getElementsByClassName('input-code').code.value;
        var action = this.dataset.action
        
		if (user == 'AnonymousUser'){
			addCookieCode(code, action)
		}
	})
}

function addCookieCode(code, action){

	if (action == 'code-add'){
		if (code[code] == undefined){
		code[code] = code

		}else{
			code[code] = code
		}
	}

	document.cookie ='code=' + JSON.stringify(code) + ";domain=;path=/"
	
	location.reload()
}

