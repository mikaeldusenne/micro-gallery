
function onlythebest(){
	var b = document.getElementById("onlythebest").checked;
	var disp = b ? "none" : "flex";
	
	document.querySelectorAll('.element:not(.best)')
		.forEach(e => e.style.display=disp);
}
