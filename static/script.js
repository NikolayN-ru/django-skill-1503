let r = document.querySelector('input')
console.log(r.value)

let ShowPassword= document.querySelector('.show-password')

ShowPasswor.onchange = function () {
	if (ShowPasswor.checked){
		r.type='password'
		console.log(4)
	} else {
		r.type='text'
		console.log(5)
	}
}

let p = document.querySelector('p')
p.style.color = 'red'