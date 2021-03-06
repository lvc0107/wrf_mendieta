#!/bin/bash

##############################################################################################
### How to run:
### sbatch job_wrf.sh f_Thompson_MYJ 2016-09-28_18:00:00 2016-09-30_06:00:00 N
### With N in {2..8}
###

#################################### Slurm configuration #####################################

### Samples of job scripts in /usr/share/doc/mendieta/

#SBATCH --mail-type=ALL
#SBATCH --mail-user=miguelmnr@gmail.com
#SBATCH --job-name=WRF
#SBATCH --partition=multi
#SBATCH --exclusive

#SBATCH --nodes=2
#SBATCH --ntasks-per-node=20

### Execution Time. Format: days-hours:minutes. Max time: Four days.
#SBATCH --time 0-3:30


### Environment setup
. /etc/profile
################################# WRF Configuration ###################################

### $1: Ensamble name
### $2 Start Date
### $3: End Date
### $4: Amount of nodes

./run_wrf_model.sh $1 $2 $3 $4


