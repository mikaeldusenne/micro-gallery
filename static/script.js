
function set_only_best(b){
	var disp = b ? "none" : "flex";
	
	document.querySelectorAll('.element:not(.best)').forEach(function(e){
		e.style.display=disp;
	});
}

function onlythebest(e){
	console.log("best");
	console.log(e);
	set_only_best(e.target.checked);
}
