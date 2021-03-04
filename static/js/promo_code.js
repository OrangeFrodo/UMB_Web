var updateBtnsPromo = document.getElementsByClassName('update-promo')

for (i = 0; i < updateBtnsPromo.length; i++) {
	updateBtnsPromo[i].addEventListener('click', function(){
        var code = document.getElementsByClassName('input-code').code.value;
        var action = this.dataset.action

        console.log('code:', code, 'Action:', action)
        console.log('USER:', user)
        
		if (user == 'AnonymousUser'){
			addCookieCode(code, action)
		}
	})
}

function addCookieCode(code, action){
	console.log('User is not authenticated')

	if (action == 'code-add'){
		if (code[code] == undefined){
		code[code] = code

		}else{
			code[code] = code
		}
	}

	console.log('CODE:', code)
	document.cookie ='code=' + JSON.stringify(code) + ";domain=;path=/"
	
	location.reload()
}

