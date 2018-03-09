#! /bin/bash

################################# GRADS Configuration ###################################
# Execution:
# This script is executed from run_wrf_model.sh script (post_processing stage)
#
# This script can be updated by the user
#######################################################################################

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


