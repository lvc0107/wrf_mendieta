 /*Obtenemos la fecha corriente*/
var currentdate = new Date(); 
var mm = (currentdate.getMonth()+1)
var dd = currentdate.getDate();
if(dd<10){dd='0'+dd} if(mm<10){mm='0'+mm}
var today = currentdate.getFullYear() + "-" + mm + "-" + dd;


/*Arreglo con el numero de hora utc*/
hours_utc  = new Array()
for (var i = 0 ; i < 73; i++) {
	hours_utc[i] = i
	
}


/*Funcion para recolectar los datos de los meteogramas por defecto*/
function met_default(archivo){
	
	var dat = []

	//Hacer esto de forma dinamica
	if (archivo == "./A_Thompson_MYJ/meteogramas/Temperatura_ALEJO_LEDESMA_A.txt"){		
		dat =  [95.1074, 
				94.7887, 
				92.2935, 
				91.7588, 
				89.4158, 
				86.2718, 
				85.0768, 
				89.698, 
				87.2754, 
				83.0629, 
				82.2933, 
				81.8236, 
				80.2435, 
				83.0235, 
				91.5466, 
				91.7353, 
				92.2057, 
				89.0219, 
				92.9578, 
				95.3623, 
				93.6713, 
				92.4649, 
				93.795, 
				93.8902 
			]}
	
	if (archivo == "./B_Marrison_MYJ_sf_sfclay_physics/meteogramas/Temperatura_ALEJO_LEDESMA_A.txt"){		
	//if (archivo == "B"){
		dat =   [75.1074, 
				74.7887, 
				72.2935, 
				71.7588, 
				69.4158, 
				66.2718, 
				65.0768, 
				69.698, 
				67.2754, 
				63.0629, 
				62.2933, 
				61.8236, 
				60.2435, 
				63.0235, 
				61.5466, 
				71.7353, 
				72.2057, 
				69.0219, 
				72.9578, 
				57.3623, 
				77.6713, 
				72.4649, 
				73.795, 
				73.8902 ]

		
		}
	if (archivo == "./C_WDM6_QNSE_sf_sfclay_physics/meteogramas/Temperatura_ALEJO_LEDESMA_A.txt"){		
		dat = [65.1074, 
				64.7887, 
				62.2935, 
				65.7588, 
				59.4158, 
				56.2718, 
				55.0768, 
				59.698, 
				57.2754, 
				53.0629, 
				52.2933, 
				51.8236, 
				50.2435, 
				53.0235, 
				61.5466, 
				61.7353, 
				62.2057, 
				59.0219, 
				52.9578, 
				65.3623, 
				63.6713, 
				62.4649, 
				63.795, 
				63.8902 ]
	}
	if (archivo == "./D_WRF6_MYJ_sf_sfclay_physics/meteogramas/Temperatura_ALEJO_LEDESMA_A.txt"){		
		dat = [55.1074, 
				54.7887, 
				55.2935, 
				51.7588, 
				49.4158, 
				46.2718, 
				45.0768, 
				49.698, 
				47.2754, 
				34.0629, 
				42.2933, 
				41.8236, 
				40.2435, 
				43.0235, 
				41.5466, 
				41.7353, 
				52.2057, 
				49.0219, 
				52.9578, 
				35.3623, 
				43.6713, 
				42.4649, 
				33.795, 
				33.8902 ]
		
		
	}
	if (archivo == "./E_WDM6_MYNN3/meteogramas/Temperatura_ALEJO_LEDESMA_A.txt"){		
		dat =  [95.1074, 
				84.7887, 
				82.2935, 
				81.7588, 
				89.4158, 
				76.2718, 
				75.0768, 
				79.698, 
				77.2754, 
				73.0629, 
				72.2933, 
				71.8236, 
				70.2435, 
				73.0235, 
				71.5466, 
				81.7353, 
				82.2057, 
				79.0219, 
				82.9578, 
				85.3623, 
				83.6713, 
				82.4649, 
				83.795, 
				83.8902 
	]}
	
	return dat
	
	
	/*
	var req = new XMLHttpRequest() 

	req.open("GET", archivo, false);	
	//req.send(null)
	var str = req.responseText;
	var dat_str = new Array()
	dat_str = str.split("\n")



	var dat = new Array()
	for (var i = 0 ; i < dat_str.length; i++) {
		dat[i] = Number(Number(dat_str[i]).toFixed(4))
	}

	dat.pop()

	return dat;
	/// Esta es otra prueba
	var datos = $.get(archivo, function(data) {
      var items = data.split('\n');
	});
	return datos; 
	*/
};


/*Funcion para promediar datos en caso de usar el selector*/
function promediar_array(array){
	res = new Array()
	for (var i = 0 ; i < 72; i++) {
		res[i] = Number(((array[0][i] + array[1][i] + array[2][i] + array[3][i])/4.0).toFixed(4))
	}
	return res
}


/*Funcion para pasar el archivo de coordenadass a un arreglo*/
function coord_set(archivo){
	var req = new XMLHttpRequest(); 
	req.open("GET", archivo, false); 
	req.send(null);
	var str = req.responseText;


	var dat_str = new Array();
	dat_str = str.split("\n");		        

	var dat = new Array();
	for (var i = 0 ; i < dat_str.length; i++) {
		dat[i] = dat_str[i].split(",");
	};

	return dat; 

};


/*Funcion que busca el indice en donde se encuantra lat y lon requerida*/
function indice(lat, lon, array){
	var n = array.length;
	index = -1;
	for (var i = 0 ; i < n; i++) {
		if (Number(array[i][0]) == lat && Number(array[i][1]) == lon){
			index = i;
			return index;
		}
	}
	return index;	
		
};


/*Funcion para extraer los datos de una coordenada de cierta variable ambiental*/
function data_set(archivo, index){
var req = new XMLHttpRequest(); 
	req.open("GET", archivo, false)
	req.send(null)
	var str = req.responseText


	var dat_str = new Array()
	dat_str = str.split("\n")		        

	var dat = new Array()

	dat = dat_str[index].split("   ")

	dat.pop()

	for (var i = 0; i < dat.length; i++) {
		dat[i] = Number(dat[i])	
	}

	return dat

}


/*funcion para graficar mapa */
function print_map(lat,lon){
		var map
		var myLatlng =  new google.maps.LatLng(lat,lon)
		google.maps.event.addDomListener(window, 'load', $(function initialize() {
			  var mapOptions = {
			    zoom: 9,
			    center: myLatlng
			  }
			  map = new google.maps.Map(document.getElementById('mapa'),mapOptions);

			  var marker = new google.maps.Marker({
		      position: myLatlng,
		      map: map,
		      title: myLatlng.toString()
			})
		})
	)
}


function print_meteo(div, serie_x, scenarios, unidad, tipo, color, titulo){

	//TODO : do this better please

	$(div).highcharts({
		chart: {
            type: tipo
        },

		title: {
			text: titulo,
			x: -20 //center
		},
		subtitle: {
            text: 'Fuente: CAEARTE - WRF' +"<br>"+'Fecha de Inicio: ' + today + " 00:00 UTC",
            x: -20
        },

		xAxis: {
			categories:serie_x
		},
		yAxis: {
			title: {
			text: titulo + " " + unidad
		},
		plotLines: [{
			value: 0,
			width: 1,
			color: '#808080'
			}]
		},
		tooltip: {
			shared: true,
            useHTML: true,
            headerFormat: '<small>{point.key}</small><table>',
            pointFormat: '<tr><td style="color: {series.color}">{series.name}: </td>' +
                '<td style="text-align: right"><b>{point.y}</b></td></tr>',
            footerFormat: '</table>',
            valueDecimals: 1,
			valueSuffix: unidad
		},
		legend: {
			layout: 'vertical',
			align: 'right',
			verticalAlign: 'middle',
			borderWidth: 0
		},
		series: [{
			name: scenarios[0]['name'],
			data: scenarios[0]['datos'],
			color: "red"
			},
			{
			name: scenarios[1]['name'],
			data: scenarios[1]['datos'],
			color: "blue"
			},
			{
			name: scenarios[2]['name'],
			data: scenarios[2]['datos'],
			color: "green"
			},
			{
			name: scenarios[3]['name'],
			data: scenarios[3]['datos'],
			color: "purple"
			},
			{
			name: scenarios[4]['name'],
			data: scenarios[4]['datos'],
			color: "black"
			}
		
			]
		});
};


/*Ocultamos las alertas*/
$(function(){
	$("#alerta1").hide();
});


$(function(){
	$("#alerta2").hide();
});



//Funcion para cargar las provincias dinamicamente
$( document ).ready(function() {
	$.ajax({
		type:"GET",
		url: "prov.php",
		data: {},
		success:function(data){
			var a = data
			a = a.split('\n')
			var response = '<option value="">--Seleccione Provincia--</option>'
			$.each(a, function(i, val){
				try{
					var val_aux = val.split('+')
					response += '<option value="'+val_aux[0]+'">'+val_aux[1].toUpperCase()+'</option>'
				}catch(err){

				}
				
			})
			$('#provincia').html(response)
		}
	})
})	


//Funcion para cargar las provincias dinamicamente
function selector_departamento(selected) {
	if(selected.value != ''){
		//var provincia = $('#provincia').val()
		$.ajax({
			type:"GET",
			url: "depto.php",
			data: {'provincia': selected.value,},
			success:function(data){
				var a = data
				a = a.split('\n')
				var response = '<option value="">--Seleccione Departamento--</option>'
				$.each(a, function(i, val){
					try{
						var val_aux = val.split('+')
						response += '<option value="'+val_aux[0]+'">'+val_aux[1]+'</option>'
					}catch(err){

					}
					
				})
				$('#departamentos').html(response)
			}
		})
	}
}


//Funcion para cargar las localidades dinamicamente
function selector_localidad(selected) {
	if(selected.value != ''){
		var provincia = $('#provincia').val()
		$.ajax({
			type:"GET",
			url: "loc.php",
			data: {
				'departamento': selected.value,
				'provincia': provincia,
			},
			success:function(data){
				var a = data
				a = a.split('\n')
				var response = '<option value="">--Seleccione Localidad--</option>'
				$.each(a, function(i, val){
					try{
						var val_aux = val.split('+')
						response += '<option value="'+val_aux[0]+'">'+val_aux[1]+'</option>'
					}catch(err){

					}
					
				})
				$('#localidad').html(response)
			}
		})
	}
}


//Funcion para obtener la localidad seleccionada
function posicion_geo(localidad){
	if(localidad != ''){
		var provincia = $('#provincia').val()
		var departamento = $('#departamentos').val()
		var localidad = localidad.value

		$.ajax({
			type:"GET",
			url: "pos.php",
			data: {
				'provincia': provincia,
				'departamento': departamento,
				'localidad': localidad,
			},
			success:function(data){
				var datos = data
				alert("El procesamiento de los datos puede demorar unos segundos. Por favor espere")		
				graficar_con_selects(datos,1)
			}
		})
	}
}


//Funcion para obtener los cuatros puntos mas cercanos de una coordenada
function coord_interpolacion(){

		var latitud = $('#lat').val()
		var longitud = $('#lon').val()

		$.ajax({
			type:"GET",
			url: "din.php",
			data: {
				'latitud': latitud,
				'longitud': longitud,

			},
			success:function(data){
				var datos = data
				alert("El procesamiento de los datos puede demorar unos segundos. Por favor espere")	
				graficar_con_selects(datos,0)

			}	
		})
}



/*Funcion para graficar meteogramas y mapa por defecto*/

$(function(){
	var datos = new Array()
	var datos_prec = new Array()

	// Esta funcion deberia recibir la localidad por parametro
	
	//Hacer un loop por SCENARIO y obtener localidad   dinamicamente
	var data_to_print = new Array();
	datos = met_default("./A_Thompson_MYJ/meteogramas/Temperatura_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name':'Scenario A: Thompson[8] (mp) + MYJ[2] (plb) + sf_sfclay_physics', 'datos':datos})
	datos = met_default("./B_Marrison_MYJ_sf_sfclay_physics/meteogramas/Temperatura_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name':'Scenario B: Morrison2[10] (mp) + MYJ[2] + sf_sclay_physics [2]', 'datos':datos})
	datos = met_default("./C_WDM6_QNSE_sf_sfclay_physics/meteogramas/Temperatura_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name':'Scenario C: WDM6[16] (mp) + QNSE[4] (pbl) + sf_sfclay_physics [4]', 'datos':datos})
	datos = met_default("./D_WRF6_MYJ_sf_sfclay_physics/meteogramas/Temperatura_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name':'Scenario D: WRF6[6] (mp) + MYJ[2] + sf_sclay_physics [2]', 'datos':datos})
	datos = met_default("./E_WDM6_MYNN3/meteogramas/Temperatura_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name':'Scenario E: WDM6[16] (mp) + MYNN3[6] (pbl) + sf_sfclay_physics [5]', 'datos':datos})

	print_meteo("#chart_div1", hours_utc, data_to_print, "°C", "", "red", "Temperatura")

	
	datos = met_default("./A_Thompson_MYJ/meteogramas/rain_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name':'Scenario A: Thompson[8] (mp) + MYJ[2] (plb) + sf_sfclay_physics', 'datos':datos})
	datos = met_default("./B_Marrison_MYJ_sf_sfclay_physics/meteogramas/rain_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name':'Scenario B: Morrison2[10] (mp) + MYJ[2] + sf_sclay_physics [2]', 'datos':datos})
	datos = met_default("./C_WDM6_QNSE_sf_sfclay_physics/meteogramas/rain_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name':'Scenario C: WDM6[16] (mp) + QNSE[4] (pbl) + sf_sfclay_physics [4]', 'datos':datos})
	datos = met_default("./D_WRF6_MYJ_sf_sfclay_physics/meteogramas/rain_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name':'Scenario D: WRF6[6] (mp) + MYJ[2] + sf_sclay_physics [2]', 'datos':datos})
	datos = met_default("./E_WDM6_MYNN3/meteogramas/rain_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name':'Scenario E: WDM6[16] (mp) + MYNN3[6] (pbl) + sf_sfclay_physics [5]', 'datos':datos})

	print_meteo("#chart_div2", hours_utc, data_to_print, "mm", "", "blue", "Precipitación")

	
	
	datos = met_default("./A_Thompson_MYJ/meteogramas/ws10_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name': 'Scenario A: Thompson[8] (mp) + MYJ[2] (plb) + sf_sfclay_physics', 'datos':datos})
	datos = met_default("./B_Marrison_MYJ_sf_sfclay_physics/meteogramas/ws10_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name':'Scenario B: Morrison2[10] (mp) + MYJ[2] + sf_sclay_physics [2]', 'datos':datos})
	datos = met_default("./C_WDM6_QNSE_sf_sfclay_physics/meteogramas/ws10_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name':'Scenario C: WDM6[16] (mp) + QNSE[4] (pbl) + sf_sfclay_physics [4]', 'datos':datos})
	datos = met_default("./D_WRF6_MYJ_sf_sfclay_physics/meteogramas/ws10_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name':'Scenario D: WRF6[6] (mp) + MYJ[2] + sf_sclay_physics [2]', 'datos':datos})
	datos = met_default("./E_WDM6_MYNN3/meteogramas/ws10_ALEJO_LEDESMA_A.txt")
	data_to_print.push({ 'name':'Scenario E: WDM6[16] (mp) + MYNN3[6] (pbl) + sf_sfclay_physics [5]', 'datos':datos})

	print_meteo("#chart_div3", hours_utc, data_to_print, "mm", "", "green", "Intensidad del Viento")
	
	datos = met_default("./A/meteogramas/wd10_ALEJO_LEDESMA_A.txt")
	data_to_print.push({'name': 'Scenario A: Thompson[8] (mp) + MYJ[2] (plb) + sf_sfclay_physics', 'datos':datos})
	datos = met_default("./B/meteogramas/wd10_ALEJO_LEDESMA_A.txt")
	data_to_print.push({'name': 'Scenario B: Morrison2[10] (mp) + MYJ[2] + sf_sclay_physics [2]', 'datos':datos})
	datos = met_default("./C/meteogramas/wd10_ALEJO_LEDESMA_A.txt")
	data_to_print.push({'name': 'Scenario C: WDM6[16] (mp) + QNSE[4] (pbl) + sf_sfclay_physics [4]', 'datos':datos})
	datos = met_default("./D/meteogramas/wd10_ALEJO_LEDESMA_A.txt")
	data_to_print.push({'name': 'Scenario D: WRF6[6] (mp) + MYJ[2] + sf_sclay_physics [2]', 'datos':datos})
	datos = met_default("./E/meteogramas/wd10_ALEJO_LEDESMA_A.txt")
	data_to_print.push({'name': 'Scenario E: WDM6[16] (mp) + MYNN3[6] (pbl) + sf_sfclay_physics [5]', 'datos':datos})

	print_meteo("#chart_div4", hours_utc, data_to_print, "mm", "", "yellow", "Dirección del Viento")

	
	datos = met_default("./A/meteogramas/Humedad_ALEJO_LEDESMA_A.txt")
	data_to_print.push({'name': 'Scenario A: Thompson[8] (mp) + MYJ[2] (plb) + sf_sfclay_physics', 'datos':datos})
	datos = met_default("./B/meteogramas/Humedad_ALEJO_LEDESMA_A.txt")
	data_to_print.push({'name': 'Scenario B: Morrison2[10] (mp) + MYJ[2] + sf_sclay_physics [2]', 'datos':datos})
	datos = met_default("./C/meteogramas/Humedad_ALEJO_LEDESMA_A.txt")
	data_to_print.push({'name': 'Scenario C: WDM6[16] (mp) + QNSE[4] (pbl) + sf_sfclay_physics [4]', 'datos':datos})
	datos = met_default("./D/meteogramas/Humedad_ALEJO_LEDESMA_A.txt")
	data_to_print.push({'name': 'Scenario D: WRF6[6] (mp) + MYJ[2] + sf_sclay_physics [2]', 'datos':datos})
	datos = met_default("./E/meteogramas/Humedad_ALEJO_LEDESMA_A.txt")
	data_to_print.push({'name': 'Scenario E: WDM6[16] (mp) + MYNN3[6] (pbl) + sf_sfclay_physics [5]', 'datos':datos})

	print_meteo("#chart_div5", hours_utc, data_to_print, "mm", "", "orange", "Humedad")

	

	print_map(-31.1784,-64.1659)

	
})



/*Funcion para graficar meteogramas y mapa luego de haber ingresado las coordenas*/
$(function() {
	    $("#boton").click(function() {


	    	var lat = Number(document.getElementById('lat').value);
			var lon = Number(document.getElementById('lon').value);
	    		
			if(-16.55>lat>-57.35 && -58.51>lon>-76.23 && lat<0 && lon<0 ){

	    		var coord = coord_set("datos/meteogramas/lista_de_coord.txt");
	    		var index = indice(lat,lon,coord);


		    	if(index == -1) {
		    		print_map(lat,lon)
					coord_interpolacion()
		    	}else{
		    		/*Ubicacion de la coordenada en el mapa*/
					print_map(lat, lon)

					/*Meteogramas*/
					var data = new Array()

					/*Meteograma de Temperatura*/
					data = data_set("datos/meteogramas/t2.txt", index)
					print_meteo("#chart_div1",hours_utc, data, "Temperatura", "°C","","red")

					/*Meteograma Precipitacion*/
					data = data_set("datos/meteogramas/rain.txt", index)
					print_meteo("#chart_div2",hours_utc, data,"Precipitación", "mm","column","blue")

					/*Meteograma de Nubosidad*/
					data = data_set("datos/meteogramas/cl.txt", index)
					print_meteo("#chart_div3",hours_utc, data, "Nubosidad", "%","","grey")

					/*Meteograma de Intensidad del Viento*/
					data = data_set("datos/meteogramas/ws.txt", index)
					print_meteo("#chart_div4",hours_utc, data, "Intensidad del Viento", "m/s","","purple")

					/*Meteograma de Direccion del Viento*/
					data = data_set("datos/meteogramas/wd.txt", index)
					print_meteo("#chart_div5",hours_utc, data, "Dirección del Viento", "","","black")

					/*Meteograma de RH*/
					data = data_set("datos/meteogramas/rh.txt", index)
					print_meteo("#chart_div6",hours_utc, data, "RH", "%","","green")
				
				}
			}else{
				$("#alerta2").show();
		    	$("#alerta2").delay(10000).hide(0);

			}

		})
})



//Funcion para graficar los meteogramas con el selector
function graficar_con_selects(datos, inter){

	
	datos = datos.split('++')
	var i = 0
	var j = 0
	var lats = new Array()
	var longs = new Array()
	if(inter==1){
		var str = (datos[10].toLowerCase()).split(" ")
		var aux1 = ""
		for (var n = 0; n < str.length; n++) {
			var aux2 = (str[n]).substr(1)
			var aux3 = (str[n][0]).toUpperCase() + aux2 
			aux1 = aux1 + " " + aux3
		}
		$("#title").html("<br><br><br><br>Meteogramas<br>Localidad de " + aux1)
	}

	

	while(j < 10){
		lats[i] = Number(datos[j]).toFixed(4)
		longs[i] = Number(datos[j+1]).toFixed(4)
		i++
		j+=2

	}


	var cl = new Array()
	var rain = new Array()
	var rain_acum = new Array()
	var rh = new Array()
	var temp = new Array()
	var wd = new Array()
	var ws = new Array()

	for (var k = 0; k <=3; k++){

		var lat = lats[k]
		var lon = longs[k]		
		var coord = coord_set("datos/meteogramas/lista_de_coord.txt")
		var index = indice(lat,lon,coord)


		
		if(index == -1) {
			$("#alerta2").show()
			$("#alerta2").delay(10000).hide(0)
		}else{
			
			var datos_temp = new Array()
			datos_temp = data_set("datos/meteogramas/t2.txt", index)
			temp[k] = datos_temp


			var datos_cl = new Array()
			datos_cl = data_set("datos/meteogramas/cl.txt", index)
			cl[k] = datos_cl
			

			var datos_rain = new Array()			
			datos_rain = data_set("datos/meteogramas/rain.txt", index)
			rain[k] = datos_rain

			
			var datos_rain_acum = new Array()
			datos_rain_acum = data_set("datos/meteogramas/rain_acum.txt", index)
			rain_acum[k] = datos_rain_acum


			var datos_wd= new Array()
			datos_wd = data_set("datos/meteogramas/wd.txt", index)
			wd[k] = datos_wd


			var datos_ws = new Array()
			datos_ws = data_set("datos/meteogramas/ws.txt", index)
			ws[k] = datos_ws


			var datos_rh = new Array()
			datos_rh = data_set("datos/meteogramas/rh.txt", index)
			rh[k] = datos_rh

		}
		
	}


	temp = promediar_array(temp)
	print_meteo("#chart_div1",hours_utc, temp, "Temperatura", "°C","","red")

	rain = promediar_array(rain)
	rain_acum = promediar_array(rain_acum)
	print_prec("#chart_div2",hours_utc, rain_acum, rain, "Precipitación", "mm","column","blue")

	cl = promediar_array(cl)
	print_meteo("#chart_div3",hours_utc, cl, "Nubosidad", "%","","grey")

	ws = promediar_array(ws)
	print_meteo("#chart_div4",hours_utc, ws, "Intensidad del Viento", "m/s","","purple")

	wd = promediar_array(wd)
	print_meteo("#chart_div5",hours_utc, wd, "Dirección del Viento", "","","black")
	
	rh = promediar_array(rh)
	print_meteo("#chart_div6",hours_utc, rh, "RH", "%","","green")


	if(inter == 1){
		var x = Number(lats[4])
		var y = Number(longs[4])
		print_map(x,y)
	}

	$("#alerta2").hide()
	$("#alerta1").show()
	$("#alerta1").delay(25000).hide(0)


	
}



/*Funcion para abrir y cerrar meteogramas*/
$(function(){
	var visible1 = 1;
	$("#toogle1").click(function(){
		$("#chart_div1").toggle(function(){			
			if(visible1 == 1){
				$("#toogle1").html("&#9660; Abrir &#9660;");//Cambio botón
				visible1 = 0;
			}else{
				$("#toogle1").html("&#9650; Cerrar &#9650;");
				visible1 = 1;
			}
		});

	});

	var visible2 = 1;
	$("#toogle2").click(function(){
		$("#chart_div2").toggle(function(){			
			if(visible2 == 1){
				$("#toogle2").html("&#9660; Abrir &#9660;");//Cambio botón
				visible2 = 0;
			}else{
				$("#toogle2").html("&#9650; Cerrar &#9650;");
				visible2 = 1;
			}
		});

	});

	var visible3 = 1;
	$("#toogle3").click(function(){
		$("#chart_div3").toggle(function(){			
			if(visible3 == 1){
				$("#toogle3").html("&#9660; Abrir &#9660;");//Cambio botón
				visible3 = 0;
			}else{
				$("#toogle3").html("&#9650; Cerrar &#9650;");
				visible3 = 1;
			}
		});
	});

	var visible4 = 1;
	$("#toogle4").click(function(){
		$("#chart_div4").toggle(function(){			
			if(visible4 == 1){
				$("#toogle4").html("&#9660; Abrir &#9660;");//Cambio botón
				visible4 = 0;
			}else{
				$("#toogle4").html("&#9650; Cerrar &#9650;");
				visible4 = 1;
			}
		});
	});

	var visible5 = 1;
	$("#toogle5").click(function(){
		$("#chart_div5").toggle(function(){			
			if(visible5 == 1){
				$("#toogle5").html("&#9660; Abrir &#9660;");//Cambio botón
				visible5 = 0;
			}else{
				$("#toogle5").html("&#9650; Cerrar &#9650;");
				visible5 = 1;
			}
		});
	});

	var visible6 = 1;
	$("#toogle6").click(function(){
		$("#chart_div6").toggle(function(){			
			if(visible6 == 1){
				$("#toogle6").html("&#9660; Abrir &#9660;");//Cambio botón
				visible6 = 0;
			}else{
				$("#toogle6").html("&#9650; Cerrar &#9650;");
				visible6 = 1;
			}
		});
	});


});
