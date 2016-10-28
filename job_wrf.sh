#!/bin/bash

################################# Content of this file ##################################

export FILENAME=job_wrf.sh
/bin/echo "Content of thies file: $FILENAME"
/bin/cat $FILENAME

### How to run:
### ./job_wrf.sh Thompson_MYJ 2016-08-25_18:00:00 2016-08-26_18:00:00

################################# Configuración para Slurm ###################################

#### Samples of job scripts in /usr/share/doc/mendieta/
 
#SBATCH --mail-type=ALL
#SBATCH --mail-user=miguelmnr@gmail.com
#SBATCH --job-name=40_openmpi
#SBATCH --partition=capability
#SBATCH --exclusive

### mpi in two nodes.
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=20

### Execution Time. Format: days-hours:minutes. Max time: Four days.
#SBATCH --time 0-2:00


### Environment setup
. /etc/profile

################################# WRF Configuration ###################################


scenario=$1
ACTUAL_START_DATE=$2
ACTUAL_END_DATE=$3
echo SCENARIO = $1
echo ACTUAL START DATE = $2
echo ACTUAL END DATE = $3

RUN_PARAMETERS='40_mpi_'$scenario
if [ -z $SLURM_JOB_ID ]; then
    SLURM_JOB_ID=1111
fi
LOGFILE=$WRF_BASE/slurm-$SLURM_JOB_ID.out
FINAL_LOGFILE=$WRF_BASE/$RUN_PARAMETERS'_'$SLURM_JOB_ID.out

WPS_RUN_DIR=$WRF_DIR/test/em_real/$RUN_PARAMETERS/$SLURM_JOB_ID/wps_run
WRF_RUN_DIR=$WRF_DIR/test/em_real/$RUN_PARAMETERS/$SLURM_JOB_ID/wrf_run
ARWPOST_RUN_DIR=$WRF_DIR/test/em_real/$RUN_PARAMETERS/$SLURM_JOB_ID/arwpost_run

mkdir -p $WPS_RUN_DIR
mkdir -p $WRF_RUN_DIR
mkdir -p $WPS_RUN_DIR/gribfiles
mkdir -p $ARWPOST_RUN_DIR


################################# Model execution ###################################


### Pre-processing configuration

echo "Entering directory" $WPS_RUN_DIR
cd $WPS_RUN_DIR

cp $WPS_DIR/link_grib.csh .
cp $SCENARIOS_DIR/namelist.wps .
ln -s $WPS_DIR/geogrid .
ln -s $WPS_DIR/geogrid.exe .

ln -s $WPS_DIR/ungrib .
ln -s $WPS_DIR/ungrib.exe .
ln -s $WPS_DIR/metgrid .
ln -s $WPS_DIR/metgrid.exe .

### Used Vtable downloaded from http://www2.mmm.ucar.edu/wrf/src/Vtable.GFS_new
ln -s $WPS_DIR/ungrib/Variable_Tables/Vtable.GFS_new Vtable

cp $GFS_DIR/$ACTUAL_START_DATE/* gribfiles
./link_grib.csh gribfiles/GFS*

echo "****************** PRE-PROCESSING STARTED ***********************"

./geogrid.exe
./ungrib.exe
./metgrid.exe


### Processing Configuration

echo "Entering directory" $WRF_RUN_DIR
cd $WRF_RUN_DIR

ln -sf $WPS_RUN_DIR/met_em.* .
cp $WRF_DIR/run/* .
echo setting $scenario
cp $SCENARIOS_DIR/$scenario/namelist.input .

rm -f real.exe
ln -s $WRF_DIR/run/real.exe real.exe

rm -f wrf.exe
ln -s $WRF_DIR/run/wrf.exe wrf.exe

rm -f ndown.exe
ln -s $WRF_DIR/run/ndown.exe ndown.exe

rm -f nup.exe
ln -s $WRF_DIR/run/nup.exe nup.exe

rm -f tc.exe
ln -s $WRF_DIR/run/tc.exe tc.exe


echo "****************** PROCESSING STARTED ***********************"
echo configuration used: $RUN_PARAMETERS
echo JOBID: $SLURM_JOB_ID
echo JOBNAME: $SLURM_JOB_NAME
echo NODES: $SLURM_JOB_NUM_NODES
echo TASK PER NODES: $SLURM_TASKS_PER_NODE
echo Cores obteined: $CORES
echo SLURM_NODELIST: $SLURM_NODELIST

echo real.exe execution
###srun ./real.exe 
./real.exe 

echo wrf.exe execution
echo execution time
###time srun numactl --physcpubind=0-19 ./wrf.exe
time srun ./wrf.exe

echo execution status
tail -5 rsl.error.0000
 
echo output size:
ls -lh wrfout_d01_$ACTUAL_START_DATE

echo "****************** POST-PROCESSING STARTED ***********************"

### Post-processing configuration

### Target folder for ARWPost
mkdir output

cd $ARWPOST_RUN_DIR

cp $SCENARIOS_DIR/$scenario/namelist.ARWpost .

rm -f ARWpost.exe
ln -s $ARWPOST_DIR/ARWpost.exe ARWpost.exe

###srun ./ARWpost.exe
./ARWpost.exe

cd $WRF_RUN_DIR/output 
mkdir meteogramas
cp $SCENARIOS_DIR/*.gs .

grads -pbcx 'run HPC_CBA_Tmax_Min.gs'
grads -pbcx 'run HPC_CBA_Rain.gs'
grads -pbcx 'meteogramas_Preciptation.gs'
grads -pbcx 'meteogramas_rh.gs'
grads -pbcx 'meteogramas_Temp.gs'
grads -pbcx 'meteogramas_WindDir.gs'
grads -pbcx 'meteogramas_WindSpeed.gs'

mv $LOGFILE $FINAL_LOGFILE

################################# Clean temporary files #################################
### TODO check files to be deleted
cd $WPS_RUN_DIR
cd ..
### rm -rf $WPS_RUN_DIR
cd $WRF_RUN_DIR
shopt -s extglob
### rm all but not output andy perf.data
### rm !(wrfout*)

