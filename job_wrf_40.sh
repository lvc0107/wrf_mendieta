#!/bin/bash

##############################################################################################
### How to run:
### sbatch job_wrf_40.sh A_Thompson_MYJ 2016-09-28_18:00:00 2016-09-30_06:00:00

#################################### Slurm configuration #####################################

### Samples of job scripts in /usr/share/doc/mendieta/
 
#SBATCH --mail-type=ALL
#SBATCH --mail-user=miguelmnr@gmail.com
#SBATCH --job-name=WRF
#SBATCH --partition=capability
#SBATCH --exclusive

#SBATCH --nodes=2
#SBATCH --ntasks-per-node=20

### Execution Time. Format: days-hours:minutes. Max time: Four days.
#SBATCH --time 0-2:00


### Environment setup
. /etc/profile
. ./set_configuration.sh
################################# WRF Configuration ###################################


scenario=$1
ACTUAL_START_DATE=$2
ACTUAL_END_DATE=$3
echo SCENARIO = $1
echo ACTUAL START DATE = $2
echo ACTUAL END DATE = $3

RUN_PARAMETERS=$[ $NODES * 20 ]'_cores_'$scenario
if [ -z $SLURM_JOB_ID ]; then
    SLURM_JOB_ID=11111
    TEMP_PATH=$WRF_DIR/test/em_real/$RUN_PARAMETERS/$SLURM_JOB_ID
    while [ -d $TEMP_PATH ]
    do
        SLURM_JOB_ID=$[ $SLURM_JOB_ID + 1]
        TEMP_PATH=$WRF_DIR/test/em_real/$RUN_PARAMETERS/$SLURM_JOB_ID
        echo "checking for" $TEMP_PATH
    done

fi

WPS_RUN_DIR=$WRF_DIR/test/em_real/$RUN_PARAMETERS/$SLURM_JOB_ID/wps_run
WRF_RUN_DIR=$WRF_DIR/test/em_real/$RUN_PARAMETERS/$SLURM_JOB_ID/wrf_run
ARWPOST_RUN_DIR=$WRF_DIR/test/em_real/$RUN_PARAMETERS/$SLURM_JOB_ID/arwpost_run

mkdir -p $WPS_RUN_DIR
mkdir -p $WRF_RUN_DIR
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
./link_grib.csh $GFS_DIR/$ACTUAL_START_DATE/GFS*

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


echo "Entering directory" $ARWPOST_RUN_DIR
cd $ARWPOST_RUN_DIR

### Target folder for ARWPost
mkdir -p output/meteogramas

cp $SCENARIOS_DIR/$scenario/namelist.ARWpost .

rm -f ARWpost.exe
ln -s $ARWPOST_DIR/ARWpost.exe ARWpost.exe

###srun ./ARWpost.exe
./ARWpost.exe

cd output
cp $SCENARIOS_DIR/*.gs .
echo ==================================================
echo executing grads -pbcx 'run HPC_CBA_Tmax_Min.gs'
grads -pbcx 'run HPC_CBA_Tmax_Min.gs'
echo ==================================================
echo executing grads -pbcx 'run HPC_CBA_Rain.gs'
grads -pbcx 'run HPC_CBA_Rain.gs'
echo ==================================================
echo executing grads -pbcx 'run meteogramas_Preciptation.gs'
grads -pbcx 'run meteogramas_Preciptation.gs'
echo ==================================================
echo executing grads -pbcx 'run meteogramas_rh.gs'
grads -pbcx 'run meteogramas_rh.gs'
echo ==================================================
echo executing grads -pbcx 'run meteogramas_Temp.gs'
grads -pbcx 'run meteogramas_Temp.gs'
echo ==================================================
echo executing grads -pbcx 'run meteogramas_WindDir.gs'
grads -pbcx 'run meteogramas_WindDir.gs'
echo ==================================================
echo executing grads -pbcx 'run meteogramas_WindSpeed.gs'
grads -pbcx 'run meteogramas_WindSpeed.gs'

current_date=$(date '+%d-%b-%Y')

OUTPUT_DIR=$WRF_BASE/output/$current_date/$SLURM_JOB_ID
mkdir -p $OUTPUT_DIR
cp -avr $ARWPOST_RUN_DIR/* $OUTPUT_DIR 

################################# Clean temporary files #################################

LOGFILE=$WRF_BASE/slurm-$SLURM_JOB_ID.out
FINAL_LOGFILE=$RUN_PARAMETERS'_'$SLURM_JOB_ID.out
mkdir -p $WRF_BASE/logs/$current_date
mv $LOGFILE $WRF_BASE/logs/$current_date/$FINAL_LOGFILE

rm -rf $WPS_RUN_DIR
rm -rf $WRF_RUN_DIR
rm -rf $ARWPOST__RUN_DIR

