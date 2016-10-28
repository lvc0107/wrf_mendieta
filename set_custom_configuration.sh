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


export WRF_BASE=$HOME/WRF38
export WRF_DIR=$WRF_BASE/WRF/WRFV3          # Directorio principal de WRF
export WPS_DIR=$WRF_BASE/WRF/WPS            # Directorio principal del pre-procesador WPS
export ARWPOST_DIR=$WRF_BASE/WRF/ARWpost    # Directorio principal del post-procesador ARWPost
export GFS_DIR=$WRF_BASE/gribfiles          # Directory for grib files
export SCENARIOS_DIR=$WRF_BASE/scenarios    # Directory for scenarios

export jasper=$WRF_BASE/library/jasper
export JASPERLIB=$WRF_BASE/library/jasper/lib
export JASPERINC=$WRF_BASE/library/jasper/include


export NETCDF=$WRF_BASE/library/netCDF
export NETCDF_LIB=$NETCDF/lib
export NETCDF_INC=$NETCDF/include
export HDF5=$WRF_BASE/library/hdf5-1.8.13
export PHDF5=$HDF5
export ZLIB=$WRF_BASE/library/zlib-1.2.8

export CPPFLAGS="-I${NETCDF}/include -I${HDF5}/include -I${ZLIB}/include"
export LDFLAGS="-L${NETCDF}/lib -L${HDF5}/lib -L${ZLIB}/lib"
export LD_LIBRARY_PATH=${NETCDF}/lib:${LD_LIBRARY_PATH}


export WRFIO_NCD_LARGE_FILE_SUPPORT=1
export WRF_EM_CORE=1


### Folder for grads configuration.
export GADDIR=$WRF_BASE/library/grads-2.0.2/data
export PATH=$PATH:$WRF_BASE/library/grads-2.0.2/bin

