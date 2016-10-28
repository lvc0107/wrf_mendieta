'reset'
'clear'
'open output.ctl'
'set lat -35.6 -29.4'
'set lon -66.2 -61.0'


***********precipitacion horas previas
'set t 10'
'lluvia1 = rainnc'

****************************Precipitacion dia 
'set t 34'
'lluvia = rainnc -lluvia1'
'set gxout Shaded'
'./rgbset'
'set clevs 0 0.5 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 100 150 200 300 500'
'set ccols 0 0 43 81 39 38 37 36 35 34 22 23 24 26 27 28 86 87 82 88 89 49'
'd lluvia'
'draw shp CBA_Linea'
'./cbar'
'draw title Precipitacion acumulada 24 hs - FECHA - A'
"set display color white"
'printim ./meteogramas/rain24h_A.png'
'set geotiff ./meteogramas/rain24h_A'
'set gxout geotiff'
'd lluvia'
'quit'



