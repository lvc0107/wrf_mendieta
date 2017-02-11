#! /usr/bin/python
import os
import getopt
import sys
import get_GFSX025_grib2 as grib
from datetime import datetime, timedelta
import re
import subprocess
import time

SEPARATOR = "=================================================================="

def update_namelist_wps(environment):
    
    try:

        print SEPARATOR
        print "Set date for namelist.wps"

        SCENARIOS_DIR = environment["SCENARIOS_DIR"]
        os.chdir(SCENARIOS_DIR)
        patterns = {
                    "start_date" : " start_date = {0}\n".format(environment["start_date"]),
                    "end_date"   : " end_date = {0}\n".format(environment["end_date"])
         }

        namelist_wps = "namelist.wps"

        with open(namelist_wps) as infile:
            with open(namelist_wps,'r+') as outfile:
                for line in infile:
                    for k, v in patterns.iteritems():
                        if k in line:
                            line = v
                            break
                    outfile.write(line)

        infile.close()
        outfile.close()
        os.system("head -15 " + namelist_wps)

    except Exception:
        raise


def set_date_namelist_input(namelist_input_path, environment):

    try:

        print SEPARATOR
        print "Set date for namelist.input in {0}".format(namelist_input_path)

        SCENARIOS_DIR = environment["SCENARIOS_DIR"]
        os.chdir(SCENARIOS_DIR + "/" + namelist_input_path)

        patterns = {
                    "run_days"      : " run_days                            = {0}\n".format(environment["run_days"]     ),
                    "run_hours"     : " run_hours                           = {0}\n".format(environment["run_hours"]    ),
                    "run_minutes"   : " run_minutes                         = {0}\n".format(environment["run_minutes"]  ),
                    "run_seconds"   : " run_seconds                         = {0}\n".format(environment["run_seconds"]  ),
                    "start_year"    : " start_year                          = {0}\n".format(environment["start_year"]   ),
                    "start_month"   : " start_month                         = {0}\n".format(environment["start_month"]  ),
                    "start_day"     : " start_day                           = {0}\n".format(environment["start_day"]    ),
                    "start_hour"    : " start_hour                          = {0}\n".format(environment["start_hour"]   ),
                    "start_minute"  : " start_minute                        = {0}\n".format(environment["start_minute"] ),
                    "start_second"  : " start_second                        = {0}\n".format(environment["start_second"] ),
                    "end_year"      : " end_year                            = {0}\n".format(environment["end_year"]     ),
                    "end_month"     : " end_month                           = {0}\n".format(environment["end_month"]    ),
                    "end_day"       : " end_day                             = {0}\n".format(environment["end_day"]      ),
                    "end_hour"      : " end_hour                            = {0}\n".format(environment["end_hour"]     ),
                    "end_minute"    : " end_minute                          = {0}\n".format(environment["end_minute"]   ),
                    "end_second"    : " end_second                          = {0}\n".format(environment["end_second"]   )
                   }

        with open('namelist.input') as infile:
            with open('namelist.input','r+') as outfile:
                for line in infile:
                    for k, v in patterns.iteritems():
                        if k in line:
                            line = v
                            break
                    outfile.write(line)

        infile.close()
        outfile.close()
        os.system("head -15 namelist.input")

        print "Set date for namelist.ARWpost " + namelist_input_path


        patterns = {
                    "start_date"      : " start_date = {0}\n".format(environment["start_date"]),
                    "end_date"        : " end_date = {0}\n".format(environment["end_date"]),
                    "input_root_name" : " input_root_name = '../wrf_run/wrfout_d01_{0}',\n".format(environment["start_date"])
        }

        namelist_awr = "namelist.ARWpost"

        with open(namelist_awr) as infile:
            with open(namelist_awr,'r+') as outfile:
                for line in infile:
                    for k, v in patterns.iteritems():
                        if k in line:
                            line = v
                            break
                    outfile.write(line)

        infile.close()
        outfile.close()
        os.system("head -15 " + namelist_awr)

    except Exception:
        raise


def download_grib_files(environment, offset):

    try:
        print SEPARATOR

        GFS_DIR = environment["GFS_DIR"]
        os.chdir(GFS_DIR)
        start_date_dir = environment["start_date"]
        start_date = environment["start_date_int_format"]

        if not os.path.exists(start_date_dir):
            os.system("mkdir " + start_date_dir)

        grib.download_grib_files(start_date, offset, GFS_DIR + "/" + start_date_dir)

    except Exception:
        raise


def load_configuration(environment, offset):

    try:

        download_grib_files(environment, offset)
        update_namelist_wps(environment)

        scenarios_name = environment["SCENARIOS"]
        for scenario in scenarios_name:
            set_date_namelist_input(scenario, environment)

    except Exception:
        raise


def run_process_model(environment, nodes):

    try:
        os.chdir(environment["WRF_BASE"])
        scenarios_name = environment["SCENARIOS"]
        start_date = environment["start_date"]
        end_date = environment["end_date"]
        
        for scenario in scenarios_name:
           print SEPARATOR
           execute_command = "sbatch job_wrf_{0}_nodes.sh {1} {2} {3}".format(nodes, scenario, start_date, end_date)
           print execute_command
           os.system(execute_command)

        check_command = "squeue -u $USER"
        print check_command
        os.system(check_command)
    except Exception:
        raise


def get_scenarios_name(environment):
    """
    This function return a list of scenarios name:
      [
       sceneario1,
       sceneario2,
       .
       .
       .
       scenearioN,

      ]
    """

    try:

        SCENARIOS_DIR = environment["SCENARIOS_DIR"]
        os.chdir(SCENARIOS_DIR)
        scenarios_name = []
        subdirs = [x[0] for x in os.walk(SCENARIOS_DIR)]
        for subdir in subdirs:
            scenarios_name.append(subdir.split("/")[-1])

        return scenarios_name[1:]

    except Exception:
        raise


def define_environment(start_date, offset):
    """
    Format of start and end date:
    start_date = YYYY-MM-DD_HH:MM:SS
    end_date = YYYY-MM-DD_HH:MM:SS

    Example:
    start_date = 2015-02-24_18:00:00
    """   
    try:

        start_date_int_format = int(start_date)
        start_date            = datetime.strptime(start_date, "%Y%m%d%H")
        start_year            = "{0:02d}".format(start_date.year)
        start_month           = "{0:02d}".format(start_date.month)
        start_day             = "{0:02d}".format(start_date.day)
        start_hour            = "{0:02d}".format(start_date.hour)
        start_minute          = "{0:02d}".format(start_date.minute)
        start_second          = "{0:02d}".format(start_date.second)

        end_date              = start_date + timedelta(hours = int(offset))
        end_year              = "{0:02d}".format(end_date.year)
        end_month             = "{0:02d}".format(end_date.month)
        end_day               = "{0:02d}".format(end_date.day)
        end_hour              = "{0:02d}".format(end_date.hour)
        end_minute            = "{0:02d}".format(end_date.minute)
        end_second            = "{0:02d}".format(end_date.second)

        #TODO ASK about these parameters
        run_days              = "0"
        run_hours             = offset
        run_minutes           = "0"
        run_seconds           = "0"

        start_date            = start_date.strftime("%Y-%m-%d_%H:%M:%S")
        end_date              = end_date.strftime("%Y-%m-%d_%H:%M:%S")
        print "Start forecast date: {0}".format(start_date)
        print "End forecast date: {0}".format(end_date)


        environment = {
                       "start_date_int_format" : start_date_int_format,
                       "start_date"            : start_date,
                       "end_date"              : end_date,
                       "offset"                : offset,
                       "start_year"            : start_year,
                       "start_month"           : start_month,
                       "start_day"             : start_day,
                       "start_hour"            : start_hour,
                       "start_minute"          : start_minute,
                       "start_second"          : start_second,
                       "end_date"              : end_date,
                       "end_year"              : end_year,
                       "end_month"             : end_month,
                       "end_day"               : end_day,
                       "end_hour"              : end_hour,
                       "end_minute"            : end_minute,
                       "end_second"            : end_second,
                       "run_days"              : run_days,
                       "run_hours"             : run_hours,
                       "run_minutes"           : run_minutes,
                       "run_seconds"           : run_seconds
                      }

        if not os.getenv("WRF_BASE"):
            print "==============================================================="
            print "Before run this script you should run . ./set_configuration.sh"
            print "==============================================================="
            sys.exit(1)

        print "ENVIRONMENT VARIABLE LOADED: {0}".format(os.getenv("WRF_BASE"))
        environment["WRF_BASE"] = os.getenv("WRF_BASE")
        print "ENVIRONMENT VARIABLE LOADED: {0}".format(os.getenv("GFS_DIR"))
        environment["GFS_DIR"] = os.getenv("GFS_DIR")
        print "ENVIRONMENT VARIABLE LOADED: {0}".format(os.getenv("SCENARIOS_DIR"))
        environment["SCENARIOS_DIR"] = os.getenv("SCENARIOS_DIR")
        environment["SCENARIOS"] = get_scenarios_name(environment)

        return environment

    except Exception:
        raise


def usage():

    print """
==================================================================================
==================================================================================
       Execution of WRF model:

       ./run_wrf_model.py -i=STARTDATE -o=OFFSET -n=2
       or:
       ./run_wrf_model.py --start_date=STARTDATE --offset=OFFSET --nodes=2

       Where STARTDATE has the follow format: YYYYMMDDHH
       and OFFSET is an integer value that represent the forecast hours
       starting from the STARTDATE and defined in the range [0-168]hs.
       The nodes flag is the number of nodes in Capability partition,
       with nodes in [2,8].

       Example:
       ./run_wrf_model.py -i=2015112218 -o=36 -n=2
       means Forecast of 36 hs starting from the date:
       year: 2015
       month: 11
       day: 22
       hour: 18
       forecast time: 36 hs

       running in 2 nodes of Capability partition


       Warning: The date is valid only until 15 days behind
==================================================================================
==================================================================================
      """

    sys.exit(1)


def check_parameter(option,arg):

    try:
        arg = arg.replace("=", "")
        arg = str(int(arg))
        if option in ("-i", "--start_date"):
            date = datetime.strptime(arg, '%Y%m%d%H')
        elif option in ("-o", "--offset"):

            #TODO: define the correct range of OFFSET to validate
            # In the meantime we are defined the range of offset hours in [0-168]hs
            if not (0 <= int(arg) and  int(arg) <= 168):
               usage()
        elif option in ("-n", "--nodes"):
            if not int(arg) in range(1,9):
               usage()
        return arg
    except Exception:
        usage()


def main():

    print """
    __          _______  ______ 
     \ \        / /  __ \|  ____|
      \ \  /\  / /| |__) | |__   
       \ \/  \/ / |  _  /|  __|  
        \  /\  /  | | \ \| |     
         \/  \/   |_|  \_\_|     

        """
    time.sleep(1)
    start_date  = None
    offset      = None
    nodes       = 1  #default value = i node in capability partition
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hin:o:", ["help", "start_date=", "offset=", "nodes="])
    except getopt.GetoptError as err:
        usage()

    valid_start_date = False
    valid_offset = False
    valid_nodes = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--start_date"):
            a = check_parameter(o,a)
            start_date = a
            valid_start_date = True
        elif o in ("-o", "--offset"):
            a = check_parameter(o,a)
            offset = a
            valid_offset = True
        elif o in ("-n", "--nodes"):
            a = check_parameter(o,a)
            nodes = a
            valid_nodes = True
        else:
            usage()
    if not valid_offset or not valid_start_date or not valid_nodes:
        usage()

    try:
        environment = define_environment(start_date, offset)
        load_configuration(environment, offset)
        run_process_model(environment, nodes)
    except Exception:
        raise

if __name__ == "__main__":

    main()

