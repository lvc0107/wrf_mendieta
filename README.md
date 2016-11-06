![alt tag](https://github.com/lvc0107/wrf_mendieta/blob/master/images/cropped-ccad.jpg)

# Instalación y ejecución de WRF en Mendieta #



## Índice

1. Introducción 
2. Descarga de WRF/WPS/ARWpost   
3. Instalación de WRF + dependencias
4. Obtención de datos terrestres
5. Ejecución del modelo
6. Análisis y control de ejecución
7. Bibliografía & Guías de instalación tomadas de referencia

_______________________________________________________________________________

**1. Introducción**

Código utilizado:  

Procesamiento: WRF3.6.1
Pre-procesamiento: WPS3.6.1
Post-procesamiento: ARWpost_V3  

Para versión WRF3.8 Realizar este procedimiento cambiando 3.6.1 por 3.8  #Bajo estudio en este momento.

Herramienta adicional para post-procesamiento: Grads
Descargado desde:
http://iges.org/grads/downloads.html

Requerimientos:  
Instalados en Mendieta:

* perl
* netcdf   
* hdf5   
* mpi  

No instalados en Mendieta:

* Jasper
Descargado desde: 
http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-1.900.1.zip  

_______________________________________________________________________________

**2. Descarga de WRF/WPS/ARWpost**

clonar este repo:
```
ssh <USER>@mendieta.ccad.unc.edu.ar
cd $HOME
git clone https://github.com/lvc0107/wrf_mendieta.git
cd wrf_mendieta
mkdir WRF3.6.1 
```


Cargar las siguientes variables de entorno

```
. set_configuration.sh
```

Descarga de WRF   
```
cd $WRF_BASE/WRF3.6.1
wget http://www2.mmm.ucar.edu/wrf/src/WRFV3.6.1.TAR.gz
tar -xvzf WRFV3.6.1.TAR.gz
rm WRFV3.6.1.TAR.gz
```

Descarga de WPS

```
cd $WRF_BASE/WRF3.6.1
wget http://www2.mmm.ucar.edu/wrf/src/WPSV3.6.1.TAR.gz
tar -xvzf WPSV3.6.1.TAR.gz
rm WPSV3.6.1.TAR.gz
```

Descarga de ARWpost

```
cd $WRF_BASE/WRF3.6.1
wget http://www2.mmm.ucar.edu/wrf/src/ARWpost_V3.tar.gz
tar -xvzf ARWpost_V3.tar.gz 
rm ARWpost_V3.tar.gz
```

_______________________________________________________________________________

**3. Instalación de WRF + dependencias**

**3.1. Seteo de entorno**


Jasper:

```
cd $WRF_BASE

module load compilers/gcc/4.9
mkdir -p library/jasper
cd library/jasper
wget http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-1.900.1.zip
unzip jasper-1.900.1.zip
cd jasper-1.900.1
./configure --prefix=$WRF_BASE/library/jasper
make
make check
make install
```
Chequeo de la correcta instalación de jasper:
```
ls ../bin/
imgcmp  imginfo  jasper  tmrdemo
```


**ATENCION!!! La siguiente sección debe usarse en caso de que las dependencias de MENDIETA no estén instaladas.**  
**Actualmente las dependencias necesarias si están instaladas por lo tanto pasamos directamente a la sección 3.1.2.**  
**En caso de que no estuvieses instaladas seguir en la siguiente sección. También es importante cambiar "set_configuration.sh" por "set_custom_configuration.sh" en el archivo run_wrf_model.sh.**  

**3.1.1 Instalación de tools propias (Sin usar las que provee Mendieta)**

Cargar las siguientes variables de entorno
```
. set_custom_configuration.sh
```


Zlib
```
cd $WRF_BASE/library
mkdir zlib
cd zlib
wget http://fossies.org/linux/misc/zlib-1.2.8.tar.gz
tar -xvf zlib-1.2.8.tar.gz
rm zlib-1.2.8.tar.gz
cd zlib-1.2.8/
./configure --prefix=$(pwd)
make test
make install
```

HDF5
```
cd $WRF_BASE/library
mkdir hdf5
cd hdf5/
wget https://www.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8.13/src/hdf5-1.8.13.tar.gz
tar -xvzf hdf5-1.8.13.tar.gz
hdf5-1.8.13.tar.gz
cd hdf5-1.8.13/
 ./configure --prefix=$(pwd)
make test
make install
make check-install
```


NETCDF
```
cd $WRF_BASE/library
mkdir netcdf
wget http://pkgs.fedoraproject.org/repo/pkgs/netcdf/netcdf-4.3.3.1.tar.gz/5c9dad3705a3408d27f696e5b31fb88c/netcdf-4.3.3.1.tar.gz
md5sum  netcdf-4.3.3.1.tar.gz | grep 5c9dad3705a3408d27f696e5b31fb88c
tar -xvf netcdf-4.3.3.1.tar.gz
rm netcdf-4.3.3.1.tar.gz
cd netcdf-4.3.3.1/
./configure --prefix=$(pwd)/.. FC=gfortran F77=gfortran CC=gcc --enable-shared LDFLAGS="-L$HOME/WRF/library/hdf5/hdf5-1.8.13/lib"  CPPFLAGS="-I$HOME/WRF/library/hdf5/hdf5-1.8.13/include"
make
make check
make install
```

NETCDF-Fortran
```
cd $WRF_BASE/library/netcdf
wget  wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-fortran-4.2.tar.gz
tar -xvf netcdf-fortran-4.2.tar.gz
rm netcdf-fortran-4.2.tar.gz
cd  netcdf-fortran-4.2
./configure --prefix=$(pwd)/..  FC=gfortran F77=gfortran CC=gcc --enable-shared 2>&1 | tee configure.log
make
make check
make install

```


MVAPICH
```
cd $WRF_BASE/library
mkdir mvapich
cd mvapich
wget http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.2.tar.gz
tar -xvf  mvapich2-2.2.tar.gz
rm mvapich2-2.2.tar.gz
cd  mvapich2-2.2
#configure: error: 'infiniband/mad.h not found. Please retry with --disable-mcast'
 ./configure --prefix=$(pwd)/.. --disable-mcast
make
make install

# Add $(pwd)/../bin to PATH
```

**3.1.2 Uso de tools instaladas en Mendieta**

```
. set_configuration.sh
```


**3.2. Instalación de WRF**

 

```
cd $WRF_DIR
./clean -a
./configure
```


Al iniciar configure debe dar un mensaje como el siguiente:   
De esta pinta si se esta usando set_configuration.sh (Herramientas provistas por Miendeta. RECOMENDADO)
```
checking for perl5... no
checking for perl... found /usr/bin/perl (perl)
Will use NETCDF in dir: /opt/netcdf-fortran/4.4.2-netcdf_4.3.3.1-gcc_4.9.2
Will use PHDF5 in dir: /opt/hdf5/1.8.15-gcc_4.9.2
which: no timex in (/opt/netcdf-fortran/4.4.2-netcdf_4.3.3.1-gcc_4.9.2/bin:/opt/netcdf/4.3.3.1-gcc_4.9.2/bin:/opt/hdf5/1.8.15-gcc_4.9.2/bin:/opt/openmpi-cuda/1.8.8-gcc_4.9-cuda_7.0-clean/bin:/opt/gcc/4.9.3/bin:/opt/cuda/7.0/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/ibutils/bin:/opt/mendieta/bin:/home/alighezzolo/bin:/home/alighezzolo/conae/library/grads-2.0.2/bin)

```

O de esta pinta si se esta usando set_custom_configuration.sh
```
checking for perl... found /usr/bin/perl (perl)
Will use NETCDF in dir: /home/<USER>/wrf_mendieta/library/netCDF
Will use PHDF5 in dir: /home/<USER>/wrf_mendieta/library/hdf5-1.8.13
which: no timex in (/opt/gcc/4.9.3/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/ibutils/bin:/opt/mendieta/bin:/home/<USER>/bin

```

Verificar que las variables **NETCDF** y **PHDF5** apunten a los path seteados en los archivos set_configuration.sh (set_custom_configuration.sh). 

Elegir opciones 34-1
34. x86_64 Linux, gfortran compiler with gcc (dmpar)
Compile for nesting? (1=basic) 1


Si se va a utilizar openmpi(en lugar de mvapich), actualizar la variable DM_CC con el valor -DMPI2_SUPPORT  en el archivo configure.wrf

```
DM_CC           =       mpicc -DMPI2_SUPPORT
```


```
./compile em_real &> compile.log
```
Comprobar la generación de los siguientes archivos .exe:

```
ls -lt main/*.exe

real.exe
tc.exe
nup.exe
ndown.exe
wrf.exe
```

**3.3 Instalación de WPS**

```
cd $WPS_DIR
./clean -a
./configure
```
Notar que al iniciar debe dar un mensaje como el siguiente:

```
Will use NETCDF in dir: /home/<USER>/library/netCDF
Found Jasper environment variables for GRIB2 support...
  $JASPERLIB = /home/<USER>/wrf_mendieta/library/jasper/lib
  $JASPERINC = /home/<USER>/wrf_mendieta/library/jasper/include
```

Elegir opción 1   

Actualizar Vtable.

```
cd ungrib/Variable_Tables
wget http://www2.mmm.ucar.edu/wrf/src/Vtable.GFS_new
cd ../../
ln -s ungrib/Variable_Tables/Vtable.GFS_new Vtable
```


```
./compile &> compile.log
```
Comprobar la generación de los siguientes archivos .exe:

```
ls -lt *.exe
```

```
metgrid.exe -> metgrid/src/metgrid.exe
ungrib.exe -> ungrib/src/ungrib.exe
geogrid.exe -> geogrid/src/geogrid.exe
```

Copiar este script:
```
cp $WRF_BASE/link_grib.csh $WPS_DIR
```

**3.4 Instalación de ARWpost**

```
cd $ARWPOST_DIR
```
Agregar -lnetcdff en src/Makefile

```
ARWpost.exe: $(OBJS)
    $(FC) $(FFLAGS) $(LDFLAGS) -o $@ $(OBJS) 
        -L$(NETCDF)/lib -I$(NETCDF)/include -lnetcdff -lnetcdf
```


```
./clean -a
./configure
```
Elegir opción 3.

```
./compile
```
Comprobar la generación del siguiente archivo .exe:
 
```
ls *.exe 
ARWpost.exe 
```

**3.5 Instalación de grads**

```
cd $WRF_BASE/library
wget http://cola.gmu.edu/grads/downloads/grads-2.0.2-bin-CentOS5.8-x86_64.tar.gz
tar -xvzf grads-2.0.2-bin-CentOS5.8-x86_64.tar.gz
rm grads-2.0.2-bin-CentOS5.8-x86_64.tar.gz
cd grads-2.0.2
mkdir data
cp data2.tar.gz .
tar xvf data2.tar.gz
TODO explicar de dónde obtener el archivo data2.tar.gz (por ahora lo provee Andres)
```

_________________________________________________________________________

**4. Obtención de datos terrestres**

```
cd $WPS_DIR
wget http://www2.mmm.ucar.edu/wrf/src/wps_files/geog_complete.tar.bz2
tar -xjvf geog_complete.tar.bz2
rm geog_complete.tar.bz2

#datos adicionales
cd geog
wget http://www2.mmm.ucar.edu/wrf/src/wps_files/topo_gmted2010_30s.tar.bz2
tar -xjvf topo_gmted2010_30s.tar
rm topo_gmted2010_30s.tar

wget http://www2.mmm.ucar.edu/wrf/src/wps_files/topo_30s.tar.bz2
tar -xjvf topo_30s.tar.bz2
rm  topo_30s.tar.bz2

wget http://www2.mmm.ucar.edu/wrf/src/wps_files/modis_landuse_21class_30s.tar.bz2
tar -xjvf modis_landuse_21class_30s.tar.bz2
rm modis_landuse_21class_30s.tar.bz2
```
Actualizar namelist.wps con path al directorio recién creado.

```
cd $WRF_BASE/scenarios
#Edit namelist.wps
geog_data_path = ‘/home/<USER>/wrf_mendieta/<WRF_VERSION>/WPS/geog’ # <USER> y <WRF_VERSION> que correspondan
```
_________________________________________________________________________
**5. Ejecucion del modelo**

Configuración de entorno:

```
cd $WRF_BASE/
mkdir gribfiles
```
**5.1. Crear el directorio scenarios con la siguiente estructura:**

```
tree scenarios
scenarios
├── Scenario1
│   ├── namelist.ARWpost
│   └── namelist.input
├── Scenario2
│   ├── namelist.ARWpost
│   └── namelist.input
├── Scenario3
│   ├── namelist.ARWpost
│   └── namelist.input
│   .
│   .
│   .
├── ScenarioN
│   ├── namelist.ARWpost
│   └── namelist.input
├── gradfile1.gs
├── gradfile2.gs
├── .
├── .
├── .
├── gradfileN.gs
└── namelist.wps
```

Ejemplo usado para CAEARTE  
```
tree scenarios
scenarios
├── A_Thompson_MYJ
│   ├── namelist.ARWpost
│   └── namelist.input
├── B_Marrison_MYJ_sf_sfclay_physics
│   ├── namelist.ARWpost
│   └── namelist.input
├── cbar.gs
├── C_WDM6_QNSE_sf_sfclay_physics
│   ├── namelist.ARWpost
│   └── namelist.input
├── D_WRF6_MYJ_sf_sfclay_physics
│   ├── namelist.ARWpost
│   └── namelist.input
├── E_WDM6_MYNN3
│   ├── namelist.ARWpost
│   └── namelist.input
├── HPC_CBA_Rain.gs
├── HPC_CBA_Tmax_Min.gs
├── meteogramas_Preciptation.gs
├── meteogramas_rh.gs
├── meteogramas_Temp.gs
├── meteogramas_WindDir.gs
├── meteogramas_WindSpeed.gs
├── namelist.wps
└── rgbset.gs
```

**5.2 Correr script: run_wrf_model.py**   
Este script realiza las siguientes tareas:   
1) Descarga grib files dada una fecha en el directorio gribfiles creado en el step anterior    
2) Actualiza fecha en namelist.wps en el directorio scenarios      
3) Actualiza fecha en los namelist.input dentro de cada directorio scenarios/Scenarioi con i:{1..N}     
4) Actualiza fecha en namelist.ARWpost dentro de cada directorio scenarios/Scenarioi con i:{1..N}     
5) Ejecuta el modelo para cada uno de los scenarios  

```
python run_wrf_model.py --start_date=STARTDATE --offset=OFFSET --nodes=2
```

El script ejecuta todos los scenarios en paralelo corriendo WRF en 2 nodos de la partición capability(40 cores en total).   

Ejemplo: Para ejecutar todos los scenarios en dos nodos de capability (20 cores p/nodo)
```
python run_wrf_model.py --start_date=2016102000 --offset=36 --nodes=2
```

Nota: 
Ajustar el tiempo de ejecución del modelo en el script job_wrf_N_nodes.sh de la forma más precisa posible. # Con N en [2, 3, 4, 5]    
Ejemplo si la ejecución del modelo toma aproximadamente (poco menos que) una hora y media:

```
SBATCH --time 0-1:30
```


Para ejecutar solo un scenario(por ejemplo A_Thompson_MYJ) en dos nodos de capability (20 cores p/nodo)  
para las misma fecha de inicio y periodo de 36 hs    
```
sbatch job_wrf_2_nodes.sh A_Thompson_MYJ 2016-10-20_00:00:00 2016-10-21_12:00:00
```
El output de la ejecución es el siguiente:

```


    __          _______  ______
     \ \        / /  __ \|  ____|
      \ \  /\  / /| |__) | |__
       \ \/  \/ / |  _  /|  __|
        \  /\  /  | | \ \| |
         \/  \/   |_|  \_\_|


Start forecast date: 2016-10-20_00:00:00
End forecast date: 2016-10-21_12:00:00



==================================================================
sbatch job_wrf_2_nodes.sh D_WRF6_MYJ_sf_sfclay_physics 2016-10-20_00:00:00 2016-10-21_12:00:00
Submitted batch job 50360
==================================================================
sbatch job_wrf_2_nodes.sh A_Thompson_MYJ 2016-10-20_00:00:00 2016-10-21_12:00:00
Submitted batch job 50361
==================================================================
sbatch job_wrf_2_nodes.sh C_WDM6_QNSE_sf_sfclay_physics 2016-10-20_00:00:00 2016-10-21_12:00:00
Submitted batch job 50362
==================================================================
sbatch job_wrf_2_nodes.sh E_WDM6_MYNN3 2016-10-20_00:00:00 2016-10-21_12:00:00
Submitted batch job 50363
==================================================================
sbatch job_wrf_2_nodes.sh B_Marrison_MYJ_sf_sfclay_physics 2016-10-20_00:00:00 2016-10-21_12:00:00
Submitted batch job 50364
squeue -u $USER
PARTITION   JOBID PRIO       NAME     USER ST       TIME NO CPU  GRES NODELIST(REASON)
capability  50360 2472        WRF alighezz R        0:13  2  40 (null mendieta[17-18])
capability  50361 2472        WRF alighezz R        0:13  2  40 (null mendieta[20-21])
capability  50362 2472        WRF alighezz PD       0:00  2  40 (null (Resources)
capability  50363 2472        WRF alighezz PD       0:00  2  40 (null (Resources)
capability  50364 2472        WRF alighezz PD       0:00  2  40 (null (Resources)
```

El script run_wrf_model.py ejecuta el comando **squeue -u $USER** luego de hacer submit de los jobs (ejecución del scenario). Estos jobs están en estado PD (pending) de obtener recursos. Cuando haya nodos disponibles para la ejecución los jobs que obtengan recursos van a pasar a estado R (running).

EL log proporciona también información relevante:  
 * PARTITION: Partición a la que pertenecen los nodos   
 * JOBID:  identificador único del job (ejecución del scenario)
 * USER: usuario que  lanzo la ejecución
 * NAME: Nombre e identificador del job
 * TIME: cuando el job está en estado R este valor se actualiza mostrando el tiempo transcurrido de ejecución.
   Importante: si el tiempo de ejecución es mayor al estimado en **SBATCH --time** el job se cancela. Por lo tanto  es necesario actualizar ese valor en el script job_wrf_N_nodes.sh de manera que ese valor sea mayor y correr nuevamente.
 * NO: números de nodos asignados
 * CPU: número de cores asignados
 * NODELIST: lista de nodos asignados al job


La ejecución genera los output en los directorios:
```
$WRF_BASE/output/<fecha_actual>/<JOB_ID>
```

La ejecución genera logs en los directorios:
```
$WRF_BASE/logs/<fecha_actual>/$RUN_PARAMETERS'_'$SLURM_JOB_ID.out
```
donde RUN_PARAMETERS esta definido en el script job_wrf_N_nodes.sh  # con N en [2, 3, 4, 5]    



También se pueden ejecutar los scripts:  
```
job_wrf_3_nodes.sh  
job_wrf_4_nodes.sh  
job_wrf_5_nodes.sh  
```
Que ejecutan los scenarios usando 3, 4 y 5 nodos de 20 cores c/u respectivamente

```
python run_wrf_model.py --start_date=2016102000 --offset=36 --nodes=3
python run_wrf_model.py --start_date=2016102000 --offset=36 --nodes=4
python run_wrf_model.py --start_date=2016102000 --offset=36 --nodes=5
```
Importante: La quota por usuario es de 500GB. Por lo tanto es necesario limpiar(borrar) los resultados que se van generando periódicamente, luego de su procesamiento.


**6. Análisis y control de ejecución**

Durante la ejecución de los jobs podemos ejecutar algunos comandos que nos brindan información del estado de la ejecución:
```
squeue -u $USER   # muestra el estado de los jobs propios
squeue            # muestra el estado de todos los jobs en el cluster
```

Si la ejecución de un job está en estado R podemos acceder al nodo para ver la ejecución en tiempo real
```
squeue -u $USER
capability  50361 2472        WRF alighezz R        0:13  2  40 (null mendieta[20-21])
ssh mendieta20         # también podríamos haber hecho ssh mendieta21

mendieta20 $ htop      # Ver estado de los cores. 
```

![alt tag](https://github.com/lvc0107/wrf_mendieta/blob/master/images/htop.png)

```
ssh mendieta20              # también podríamos haber hecho ssh mendieta21
mendieta20 $ perf top  # Ver funciones que consumen mas computo. 
```

![alt tag](https://github.com/lvc0107/wrf_mendieta/blob/master/images/perf-top-2nodes.PNG)


```
ssh mendieta20         # también podríamos haber hecho ssh mendieta21
lstopo                          # Conocer topología del nodo
```
![alt tag](https://github.com/lvc0107/wrf_mendieta/blob/master/images/mendieta_lstopo.png)






**7. Bibliografía & Guías de instalación tomadas de referencia**

[1] http://forum.wrfforum.com/viewtopic.php?f=5&t=7099   
[2] http://www.unidata.ucar.edu/software/netcdf/docs/building_netcdf_fortran.html   
[3] http://www2.mmm.ucar.edu/wrf/users/docs/user_guide_V3/users_guide_chap2.htm#_Required_Compilers_and_1   
[4] http://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php#STEP5   
[5] http://www2.mmm.ucar.edu/wrf/users/FAQ_files/FAQ_wrf_installation.html
