#! /bin/bash

################################# WRF Configuration ###################################
### Environment modules

module load gcc/5

export WRF_VERSION=WRF3.6.1                        #Tambien disponible WRF.3.8
export WRF_BASE=$(pwd)
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

