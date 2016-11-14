#! /bin/bash

################################# WRF Configuration ###################################
### Environment modules

#module load mpi/mvapich2-cuda/2.1-gcc_4.9.2-cuda_7.0
module load mpi/openmpi/1.8.4-gcc_4.9.2
### Load:
### 1) cuda/7.0     
### 2) libs/gcc/4.9                   
### 3) compilers/gcc/4.9
### 4) mpi/mvapich2-cuda/2.1-gcc_4.9.2-cuda_7.0

module load libs/netcdf-fortran/4.4.2-netcdf_4.3.3.1-gcc_4.9.2
### 5) libs/hdf5/1.8.15-gcc_4.9.2
### 6) libs/netcdf/4.3.3.1-gcc_4.9.2
### 7) libs/netcdf-fortran/4.4.2-netcdf_4.3.3.1-gcc_4.9.2

export WRF_VERSION=WRF3.6.1                        #Tambien disponible WRF.3.8
export WRF_BASE=$HOME/conae
export WRF_DIR=$WRF_BASE/$WRF_VERSION/WRFV3        # Directorio principal de WRF
export WPS_DIR=$WRF_BASE/$WRF_VERSION/WPS          # Directorio principal del pre-procesador WPS
export ARWPOST_DIR=$WRF_BASE/$WRF_VERSION/ARWpost  # Directorio principal del post-procesador ARWPost
export GFS_DIR=$WRF_BASE/gribfiles                 # Directorio para grib files
export SCENARIOS_DIR=$WRF_BASE/scenarios           # Directorio para scenarios

export jasper=$WRF_BASE/library/jasper
export JASPERLIB=$WRF_BASE/library/jasper/lib
export JASPERINC=$WRF_BASE/library/jasper/include

#TODO check if this folder should be /opt/netcdf/
export NETCDF=/opt/netcdf-fortran/4.4.2-netcdf_4.3.3.1-gcc_4.9.2
export NETCDF_LIB=$NETCDF/lib
export NETCDF_INC=$NETCDF/include
export HDF5=/opt/hdf5/1.8.15-gcc_4.9.2
export PHDF5=$HDF5
export CPPFLAGS="-I${NETCDF}/include -I${HDF5}/include" 
export LDFLAGS="-L${NETCDF}/lib -L${HDF5}/lib"
export LD_LIBRARY_PATH=${NETCDF}/lib:${LD_LIBRARY_PATH}   

export WRFIO_NCD_LARGE_FILE_SUPPORT=1
export WRF_EM_CORE=1

### Folder for grads configuration.
export GADDIR=$WRF_BASE/library/grads-2.0.2/data
export PATH=$PATH:$WRF_BASE/library/grads-2.0.2/bin

