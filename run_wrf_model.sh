#!/bin/bash

################################# WRF Configuration ###################################


ENSAMBLE=$1
ACTUAL_START_DATE=$2
ACTUAL_END_DATE=$3
NODES=$4
echo ENSAMBLE: $1
echo ACTUAL START DATE: $2
echo ACTUAL END DATE: $3
echo NODES: $4
RUN_PARAMETERS=$NODES'_nodes_'$ENSAMBLE
if [ -z $SLURM_JOB_ID ]; then
    SLURM_JOB_ID=11111
    TEMP_PATH=$WRF_DIR/test/em_real/$RUN_PARAMETERS/$SLURM_JOB_ID
    while [ -d $TEMP_PATH ]
    do
        SLURM_JOB_ID=$[ $SLURM_JOB_ID + 1]
        TEMP_PATH=$WRF_DIR/test/em_real/$RUN_PARAMETERS/$SLURM_JOB_ID
        echo checking for $TEMP_PATH
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

echo Entering directory $WPS_RUN_DIR
cd $WPS_RUN_DIR

cp $WPS_DIR/link_grib.csh .
cp $ENSAMBLE_DIR/namelist.wps .
ln -s $WPS_DIR/geogrid .
ln -s $WPS_DIR/geogrid.exe .

ln -s $WPS_DIR/ungrib .
ln -s $WPS_DIR/ungrib.exe .
ln -s $WPS_DIR/metgrid .
ln -s $WPS_DIR/metgrid.exe .

ln -s $WPS_DIR/ungrib/Variable_Tables/Vtable.GFS_new Vtable
./link_grib.csh $GFS_DIR/$ACTUAL_START_DATE/GFS*

echo =================== PRE-PROCESSING STARTED =====================

./geogrid.exe
./ungrib.exe
./metgrid.exe


### Processing Configuration

echo Entering directory $WRF_RUN_DIR
cd $WRF_RUN_DIR

ln -sf $WPS_RUN_DIR/met_em.* .
cp $WRF_DIR/run/* .
echo setting $ENSAMBLE
cp $ENSAMBLE_DIR/$ENSAMBLE/namelist.input .

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

echo ===================== PROCESSING STARTED =======================
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

echo =================== POST-PROCESSING STARTED =====================

### Post-processing configuration


echo Entering directory $ARWPOST_RUN_DIR
cd $ARWPOST_RUN_DIR

### Target folder for ARWPost
mkdir -p output/meteogramas

cp $ENSAMBLE_DIR/$ENSAMBLE/namelist.ARWpost .

rm -f ARWpost.exe
ln -s $ARWPOST_DIR/ARWpost.exe ARWpost.exe

./ARWpost.exe

cd output
cp $ENSAMBLE_DIR/*.gs .
sh $WRF_BASE/grads_process.sh

LOG_DIR=$WRF_BASE/logs/$RUN_PARAMETERS
echo log dir: $LOG_DIR
OUTPUT_DIR=$WRF_BASE/output/$RUN_PARAMETERS/meteogramas
echo output dir: $OUTPUT_DIR
mkdir -p $LOG_DIR
mkdir -p $OUTPUT_DIR
cp -avr $ARWPOST_RUN_DIR/output/meteogramas/* $OUTPUT_DIR
LOGFILE=$WRF_BASE/slurm-$SLURM_JOB_ID.out
mv $LOGFILE $LOG_DIR

################################# Clean temporary files #################################
cd $WRF_RUN_DIR/../../ ; rm -rf *

