#! /bin/bash

################################# WRF Configuration ###################################
# Execution:
# . set_configuration <version_numer>
#
# Example:
# . set_configuration 3.8


#######################################################################################

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    echo "Execution mode:"
    echo "1 ) . set_configuration <WRF_VERSION_NUMBER> (must be installed)"
    echo "2 ) . set_configuration # take the default value:3.8 "
    echo "Example"
    echo "2 ) . set_configuration 3.8 "
    export WRF_VERSION=WRF3.8
  else
    export WRF_VERSION=WRF$1
fi


### Environment modules

echo "    __          _______  ______ "
echo "    \ \        / /  __ \|  ____|"
echo "     \ \  /\  / /| |__) | |__   "
echo "      \ \/  \/ / |  _  /|  __|  "
echo "       \  /\  /  | | \ \| |     "
echo "        \/  \/   |_|  \_\_|     "
echo ""

module load gcc/5
module load openmpi/2
module load hdf5/1.8.18
module load netcdf/4.4.1.1
module load netcdf-fortran/4.4.4
module list
echo ""
echo "Variables defined:"

echo WRF_VERSION=$WRF_VERSION

export WRF_BASE=$HOME/wrf_mendieta
echo WRF_BASE=$WRF_BASE

export WRF_DIR=$WRF_BASE/$WRF_VERSION/WRFV3        # Directorio principal de WRF
echo WRF_DIR=$WRF_DIR
 
export WPS_DIR=$WRF_BASE/$WRF_VERSION/WPS          # Directorio principal del pre-procesador WPS
echo WPS_DIR=$WPS_DIR

export ARWPOST_DIR=$WRF_BASE/$WRF_VERSION/ARWpost  # Directorio principal del post-procesador ARWPost
echo ARWPOST_DIR=$ARWPOST_DIR

export GFS_DIR=$WRF_BASE/gribfiles                 # Directorio para grib files
echo GFS_DIR=$GFS_DIR 

export ENSAMBLE_DIR=$WRF_BASE/ensamble            # Directorio para miembros del ensamble (scenarios)
echo ENSAMBLE_DIR=$ENSAMBLE_DIR

export JASPER=$WRF_BASE/library/jasper
echo  JASPER=$JASPER

export JASPERLIB=$JASPER/lib
echo JASPERLIB=$JASPERLIB

export JASPERINC=$JASPER/include
echo JASPERINC=$JASPERINC

#export NETCDF=/opt/spack/opt/spack/linux-centos6-x86_64/gcc-5.4.0/netcdf-4.4.1.1-nr3a5yon26ljgjdnsuyxd4evjqnaw4z2
export NETCDF=/opt/spack/opt/spack/linux-centos6-x86_64/gcc-5.4.0/netcdf-fortran-4.4.4-farzkr5oqxp5k2u7bnyaps5g6pnvxffj/
echo NETCDF=$NETCDF

export NETCDF_LIB="${NETCDF}/lib -lnetcdf"
echo NETCDF_LIB=$NETCDF_LIB

export NETCDF_INC=$NETCDF/include
echo NETCDF_INC=$NETCDF_INC

export HDF5=/opt/hdf5/1.8.15-gcc_4.9.2
echo HDF5=$HDF5

export PHDF5=$HDF5
echo PHDF5=$PHDF5

export CPPFLAGS="-I${NETCDF}/include -I${HDF5}/include" cho CPPFLAGS="-I${NETCDF}/include -I${HDF5}/include" 
echo CPPFLAGS=$CPPFLAGS

export LDFLAGS="-L${NETCDF}/lib -L${HDF5}/lib"
#echo LDFLAGS=$LDFLAGS

export LD_LIBRARY_PATH=${NETCDF}/lib:${LD_LIBRARY_PATH}:/opt/netcdf/4.3.3.1-gcc_4.9.2/lib
#echo LD_LIBRARY_PATH=$LD_LIBRARY_PATH

export WRFIO_NCD_LARGE_FILE_SUPPORT=1
echo WRFIO_NCD_LARGE_FILE_SUPPORT=$WRFIO_NCD_LARGE_FILE_SUPPORT 

export WRF_EM_CORE=1
echo WRF_EM_CORE=$WRF_EM_CORE

### Folder for grads configuration.
export GADDIR=$WRF_BASE/library/grads-2.0.2/data
echo GADDIR=$GADDIR

export PATH=$PATH:$WRF_BASE/library/grads-2.0.2/bin


mkdir -p ensamble
mkdir -p output
mkdir -p logs
mkdir -p gribfiles
