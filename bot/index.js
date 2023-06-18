let tg = window.Telegram.WebApp; //получаем объект webapp телеграма 
tg.expand(); //расширяем на все окно  
tg.MainButton.text = "Готово"; //изменяем текст кнопки 
function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}
nekopic = document.getElementById("nekopic");
item1 = document.getElementById("item1");
item2 = document.getElementById("item2");
but_img1 = document.getElementById("but_img1");
but_img2 = document.getElementById("but_img2");
testo = document.getElementById("testo");
item = item1;
var req = new XMLHttpRequest();
req.open("POST", 'https://peaceful-bastion-85893.herokuapp.com/get_data/' + tg.initDataUnsafe.user.id, false);
req.send(null);
{
    data = JSON.parse(req.responseText);
    console.log(data)
    if (data.success == true) {
        phot = data.phot;
        item_one = data.item1;
		item_two = data.item2;
		nekopic.src = "https://peaceful-bastion-85893.herokuapp.com/photo/"+phot;
		//nekopic.height = nekopic.height*0.5;
		item1.src = "https://peaceful-bastion-85893.herokuapp.com/items/"+item_one+".png";
		but_img1.src = "https://peaceful-bastion-85893.herokuapp.com/items/"+item_one+".png"
		//item1.height = item1.height*0.5;
		item2.src = "https://peaceful-bastion-85893.herokuapp.com/items/"+item_two+".png"
		but_img2.src = "https://peaceful-bastion-85893.herokuapp.com/items/"+item_two+".png"
		//item2.height = item2.height*0.5;
		tg.MainButton.show();
    }
    else { 
	    a = {
			message: "У твоей некодевочки нет одежды. Пошел нахуй крч"
		};
        tg.showPopup(a);
		Telegram.WebApp.onEvent('popupClosed', function(){
			tg.close();
		});
    }
}




testo.addEventListener("click",function(e){
    if (item.style.display != "none") {
		let ClientRect = this.getBoundingClientRect();
		itemx = e.clientX - ClientRect.left;
		itemy = e.clientY - ClientRect.top;
		if (itemx < nekopic.width && itemy < nekopic.height) {
			item.style.left = Math.round(itemx - item.width/2) + "px";
			item.style.top = Math.round(itemy - item.height/2) + "px";
			if (item == item1) {
				item1.style["z-index"] = 2;
				item2.style["z-index"] = 1;
			} else {
			    item2.style["z-index"] = 2;
				item1.style["z-index"] = 1;
			}
		}
		
	}
});




let plus = document.getElementById("plus");
plus.addEventListener("click",function(e){
    if (item.style.display != "none") {
		item.height = Math.ceil(item.height*1.1);
		if (item.height > 600) {
			item.height = 600;
		}
	}
		
});




let minus = document.getElementById("minus");
minus.addEventListener("click",function(e){
	if (item.style.display != "none") {
		item.height = Math.ceil(item.height*0.9);
		if (item.height < 50) {
			item.height = 50;
		}
	}
});



let rotation1 = 0;
let rotation2 = 0;


let rot_right = document.getElementById("rot_right");
rot_right.addEventListener("click",function(e){
	if (item.style.display != "none") {
		if (item == item1) {
			rotation1 = rotation1 - 10;
			item.style.transform = "rotate(" + rotation1 + "deg)";
		}
		else {
			rotation2 = rotation2 - 10;
			item.style.transform = "rotate(" + rotation2 + "deg)";
		}
	}
});

Telegram.WebApp.onEvent('mainButtonClicked', function(){
	try {
		tg.MainButton.hide();
        settings = {
				user_id: tg.initDataUnsafe.user.id,
				dis1: item1.style.display,
				dis2: item2.style.display,
				rot1: rotation1,
				rot2: rotation2,
				x1: item1.style.left,
				y1: item1.style.top,
				x2: item2.style.left,
				y2: item2.style.top,
				h1: item1.height,
				h2: item2.height,
				z1: item1.style["z-index"],
				z2: item2.style["z-index"]
		};
		console.log(settings);
		data = JSON.stringify(settings);
		console.log(data);
		let response = $.ajax({
			method: 'POST',
			url: "https://peaceful-bastion-85893.herokuapp.com/set_data",
			data: data,
			headers:{ "Content-Type": "application/json"}
		})
		sleep(1000);
		tg.close();
	}
	catch(err) {
		tg.MainButton.text = err.message;
	}
	
});



let rot_left = document.getElementById("rot_left");
rot_left.addEventListener("click",function(e){
	if (item.style.display != "none"){
		if (item == item1) {
			rotation1 = rotation1 + 10;
			item.style.transform = "rotate(" + rotation1 + "deg)";
		}
		else {
			rotation2 = rotation2 + 10;
			item.style.transform = "rotate(" + rotation2 + "deg)";
		}
	}

});


let show = document.getElementById("show");
let show_img = document.getElementById("show_img");
item1.style.display = "none";
item2.style.display = "none";


show.addEventListener("click",function(e){

	if (item.style.display != "none"){
		item.style.display = "none";
		show_img.src = "https://peaceful-bastion-85893.herokuapp.com/items/but5.png";
	} else {
		item.style.display = "block";
		show_img.src = "https://peaceful-bastion-85893.herokuapp.com/items/but6.png";
	}
});
 
let select_one = document.getElementById("select_one");
let select_two = document.getElementById("select_two");




select_one.addEventListener("click",function(e){
	item = item1;
	if (item.style.display != "none"){
		show_img.src = "https://peaceful-bastion-85893.herokuapp.com/items/but6.png";
	} else {
		show_img.src = "https://peaceful-bastion-85893.herokuapp.com/items/but5.png";
	}
	select_two.style["background-color"] = '#dd2e44';
	select_one.style["background-color"] = '#78b159';
});		

select_two.addEventListener("click",function(e){
	item = item2;
	if (item.style.display != "none"){
		show_img.src = "https://peaceful-bastion-85893.herokuapp.com/items/but6.png";
	} else {
		show_img.src = "https://peaceful-bastion-85893.herokuapp.com/items/but5.png";
	}
	select_two.style["background-color"] = '#78b159';
	select_one.style["background-color"] = '#dd2e44';
});



      
