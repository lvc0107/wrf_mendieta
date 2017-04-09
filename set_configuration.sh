#! /bin/bash

################################# WRF Configuration ###################################
### Environment modules

module load gcc/5
module load openmpi/2
module load hdf5/1.10.0p1
module load netcdf/4.4.1.1
module load netcdf-fortran/4.4.4

export WRF_VERSION=WRF3.6.1                        #Tambien disponible WRF.3.8
export WRF_BASE=$HOME/wrf_mendieta
export WRF_DIR=$WRF_BASE/$WRF_VERSION/WRFV3        # Directorio principal de WRF
export WPS_DIR=$WRF_BASE/$WRF_VERSION/WPS          # Directorio principal del pre-procesador WPS
export ARWPOST_DIR=$WRF_BASE/$WRF_VERSION/ARWpost  # Directorio principal del post-procesador ARWPost
export GFS_DIR=$WRF_BASE/gribfiles                 # Directorio para grib files
export SCENARIOS_DIR=$WRF_BASE/ensamble            # Directorio para miembros del ensamble (scenarios)

export JASPER=$WRF_BASE/library/jasper
export JASPERLIB=$JASPER/lib
export JASPERINC=$JASPER/include

#export NETCDF=/opt/spack/opt/spack/linux-centos6-x86_64/gcc-5.4.0/netcdf-4.4.1.1-nr3a5yon26ljgjdnsuyxd4evjqnaw4z2
export NETCDF=/opt/spack/opt/spack/linux-centos6-x86_64/gcc-5.4.0/netcdf-fortran-4.4.4-farzkr5oqxp5k2u7bnyaps5g6pnvxffj/
export NETCDF_LIB="${NETCDF}/lib -lnetcdf"
export NETCDF_INC=$NETCDF/include
export HDF5=/opt/hdf5/1.8.15-gcc_4.9.2
export PHDF5=$HDF5
export CPPFLAGS="-I${NETCDF}/include -I${HDF5}/include" 
export LDFLAGS="-L${NETCDF}/lib -L${HDF5}/lib"
export LD_LIBRARY_PATH=${NETCDF}/lib:${LD_LIBRARY_PATH}:/opt-old/netcdf/4.3.3.1-gcc_4.9.2/lib

export WRFIO_NCD_LARGE_FILE_SUPPORT=1
export WRF_EM_CORE=1

### Folder for grads configuration.
export GADDIR=$WRF_BASE/library/grads-2.0.2/data
export PATH=$PATH:$WRF_BASE/library/grads-2.0.2/bin


mkdir -p ensamble
mkdir -p output
mkdir -p logs
mkdir -p gribfiles
