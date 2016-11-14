'reset'
'clear'
'open output.ctl'
'set lat -35.6 -29.4'
'set lon -66.2 -61.0'

'maximo1 = max(t2-273.15, t=10,t=34)'
'minimo1 = min(t2-273.15, t=10,t=34)'

****************************************maximo1
'clear'
'set gxout Shaded'
'./rgbset'
'set clevs -10 -5 0 5 10 15 20 25 30 35 40'
'set ccols 47 44 42 21 22 23 24 25 26 27 28'
'd maximo1'
'draw shp CBA_Linea'
'./cbar'
'draw title Temperatura Maxima'
"set display color white"
'printim ./meteogramas/temp_max.png'
'set geotiff ./meteogramas/temp_max'
'set gxout geotiff'
'd (maximo1)'


****************************************maximo1
'clear'
'set gxout Shaded'
'./rgbset'
'set clevs -10 -5 0 5 10 15 20 25 30 35 40'
'set ccols 47 44 42 21 22 23 24 25 26 27 28'
'd minimo1'
'draw shp CBA_Linea'
'./cbar'
'draw title Temperatura Minima'
"set display color white"
'printim ./meteogramas/temp_min.png'
'set geotiff ./meteogramas/temp_min'
'set gxout geotiff'
'd (minimo1)'


'quit'

