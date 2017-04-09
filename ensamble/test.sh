#!/bin/bash
. ./set_configuration.sh

OUTPUT_DIR=meteogramas
echo output dir: $OUTPUT_DIR
#mkdir -p $LOG_DIR
#mkdir -p $OUTPUT_DIR
#cp -avr $ARWPOST_RUN_DIR/output/meteogramas/* $OUTPUT_DIR
#mv $OUTPUT_DIR/*.* $OUTPUT_DIR/*$SCENARIO.*

#cd $OUTPUT_DIR/../meteogramas
cd $OUTPUT_DIR
for scenario in .
    cd scenario
PROVINCIA=CORDOBA
LOCALIDAD=NOSE
mkdir -p $PROVINCIA/$LOCALIDAD/temperatura
mkdir -p $PROVINCIA/$LOCALIDAD/lluvia
mkdir -p $PROVINCIA/$LOCALIDAD/intensidad_viento 
mkdir -p $PROVINCIA/$LOCALIDAD/direccion_viento 
mkdir -p $PROVINCIA/$LOCALIDAD/humedad 

LOG_DIR=$WRF_BASE/logs/$RUN_PARAMETERS
echo log dir: $LOG_DIR
LOGFILE=$WRF_BASE/slurm-$SLURM_JOB_ID.out
mv $LOGFILE $LOG_DIR

################################# Clean temporary files #################################
cd $WRF_RUN_DIR/../../ ; rm -rf *

