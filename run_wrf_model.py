#! /usr/bin/python
import os
import getopt
import sys
import get_GFSX025_grib2 as grib
from datetime import datetime, timedelta
import re
import subprocess


SEPARATOR = "=================================================================="

def update_namelist_wps(environment):
    
    try:

        print SEPARATOR
        print "Set date for namelist.wps"

        SCENARIOS_DIR = environment["SCENARIOS_DIR"]
        os.chdir(SCENARIOS_DIR)
        patterns = {
                    "start_date" : '%s %s,\n' % (' ', "start_date = " + environment["start_date"]),
                    "end_date"   : '%s %s,\n' % (' ', "end_date = " + environment["end_date"])
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
        print "Set date for namelist.input in " + namelist_input_path

        SCENARIOS_DIR = environment["SCENARIOS_DIR"]
        os.chdir(SCENARIOS_DIR + "/" + namelist_input_path)

        patterns = {
                    "run_days"      : '%s%-35s = %s,\n' % (' ', "run_days",     environment["run_days"]),
                    "run_hours"     : '%s%-35s = %s,\n' % (' ', "run_hours",    environment["run_hours"]),
                    "run_minutes"   : '%s%-35s = %s,\n' % (' ', "run_minutes",  environment["run_minutes"]),
                    "run_seconds"   : '%s%-35s = %s,\n' % (' ', "run_seconds",  environment["run_seconds"]),
                    "start_year"    : '%s%-35s = %s,\n' % (' ', "start_year",   environment["start_year"]),
                    "start_month"   : '%s%-35s = %s,\n' % (' ', "start_month",  environment["start_month"]),
                    "start_day"     : '%s%-35s = %s,\n' % (' ', "start_day",    environment["start_day"]),
                    "start_hour"    : '%s%-35s = %s,\n' % (' ', "start_hour",   environment["start_hour"]),
                    "start_minute"  : '%s%-35s = %s,\n' % (' ', "start_minute", environment["start_minute"]),
                    "start_second"  : '%s%-35s = %s,\n' % (' ', "start_second", environment["start_second"]),
                    "end_year"      : '%s%-35s = %s,\n' % (' ', "end_year",     environment["end_year"]),
                    "end_month"     : '%s%-35s = %s,\n' % (' ', "end_month",    environment["end_month"]),
                    "end_day"       : '%s%-35s = %s,\n' % (' ', "end_day",      environment["end_day"]),
                    "end_hour"      : '%s%-35s = %s,\n' % (' ', "end_hour",     environment["end_hour"]),
                    "end_minute"    : '%s%-35s = %s,\n' % (' ', "end_minute",   environment["end_minute"]),
                    "end_second"    : '%s%-35s = %s,\n' % (' ', "end_second",   environment["end_second"])
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
                    "start_date"        : '%s %s,\n' % (' ', "start_date = " + environment["start_date"]),
                    "end_date"          : '%s %s,\n' % (' ', "end_date = " + environment["end_date"]),
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


def download_grib_files(environment):

    try:
        print SEPARATOR

        GFS_DIR = environment["GFS_DIR"]
        os.chdir(GFS_DIR)
        start_date_dir = str(environment["start_date"])
        start_date = environment["start_date_int"]

        if not os.path.exists(start_date_dir):
            os.system("mkdir " + start_date_dir)

        grib.download_grib_files(start_date, GFS_DIR + "/" + start_date_dir)

    except Exception:
        raise


def load_configuration(environment):

    try:

        download_grib_files(environment)
        update_namelist_wps(environment)

        scenarios_name = environment["SCENARIOS"]
        for scenario in scenarios_name:
            set_date_namelist_input(scenario, environment)

    except Exception:
        raise


def run_process_model(environment):

    try:
        os.chdir(environment["WRF_BASE"])
        scenarios_name = environment["SCENARIOS"]
        start_date = environment["start_date"]
        end_date = environment["end_date"]
        
        for scenario in scenarios_name:
           print SEPARATOR
           command = "sbatch job_wrf.sh {0} {1} {2}".format(scenario, start_date, end_date)
           print command
           os.system(command)
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
    start_date = 'YYYY-MM-DD_HH:MM:SS'
    end_date = 'YYYY-MM-DD_HH:MM:SS'

    Example:
    start_date = '2015-02-24_18:00:00'
    """   
    try:

        start_date_int = int(start_date)
        start_date = datetime.strptime(start_date, '%Y%m%d%H')
        start_year = '{0:02d}'.format(start_date.year)
        start_month = '{0:02d}'.format(start_date.month)
        start_day = '{0:02d}'.format(start_date.day)
        start_hour = '{0:02d}'.format(start_date.hour)
        start_minute = '{0:02d}'.format(start_date.minute)
        start_second = '{0:02d}'.format(start_date.second)

        end_date = start_date + timedelta(hours = int(offset))
        end_year = '{0:02d}'.format(end_date.year)
        end_month = '{0:02d}'.format(end_date.month)
        end_day = '{0:02d}'.format(end_date.day)
        end_hour = '{0:02d}'.format(end_date.hour)
        end_minute = '{0:02d}'.format(end_date.minute)
        end_second = '{0:02d}'.format(end_date.second)

        #TODO ASK about these parameters
        run_days = '0'
        run_hours = offset
        run_minutes = '0'
        run_seconds = '0'

        start_date = start_year + "-" + start_month + "-" + start_day + "_" + start_hour + ":" + start_minute + ":" + start_second
        end_date = end_year + "-" + end_month + "-" + end_day + "_" + end_hour + ":" + end_minute + ":" + end_second

        print "Start forecast date: " + start_date
        print "End forecast date: " + end_date


        environment = {
                       "start_date_int" : start_date_int,
                       "start_date" : start_date,   #Date object. Format: Y-%-m-%d_%H:%M:%S
                       "end_date": end_date,        #Date object. Format: Y-%-m-%d_%H:%M:%S
                       "offset" : offset,           #measured in hours
                       "start_year" : start_year,
                       "start_month" : start_month,
                       "start_day" : start_day,
                       "start_hour" : start_hour,
                       "start_minute" : start_minute,
                       "start_second" : start_second,
                       "end_date" : end_date,
                       "end_year" : end_year,
                       "end_month" : end_month,
                       "end_day" : end_day,
                       "end_hour" : end_hour,
                       "end_minute" : end_minute,
                       "end_second" : end_second,
                       "run_days" : run_days,
                       "run_hours" : run_hours,
                       "run_minutes" : run_minutes,
                       "run_seconds" : run_seconds
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

    print "=========================================================="
    print "=========================================================="
    print "=========================================================="
    print "Execution of WRF model:"
    print "python run_model.py -i=STARTDATE -o=OFFSET"
    print "or:"
    print "python run_model.py --start_date=STARTDATE --offset=OFFSET"
    print ""
    print "    Where STARTDATE has the follow format: YYYYMMDDHH"
    print "    and OFFSET is an integer value that represent the forecast hours"
    print "    starting from the STARTDATE and defined in the range [0-168]hs"
    print ""
    print "    Example:"
    print "    python run_wrf_model.py -i=2015112218 -o=24"
    print "    means Forecast of 24hs starting from the date:"
    print "    year: 2015"
    print "    month: 11"
    print "    day: 22"
    print "    hour: 18"
    print "    forecast time: 24 hs"
    print " "
    print "Warning: The date is valid only until 15 days behind"

    sys.exit(1)


def check_parameter(option,arg):

    try:
        arg = arg.replace("=", "")
        arg = str(int(arg))
        if option in ("-i", "--start_date"):
            date = datetime.strptime(arg, '%Y%m%d%H')
            print "date selected: {0}".format(date)
        elif option in ("-o", "--offset"):

            #TODO: define the correct range of OFFSET to validate
            # In the meantime we are defined the range of offset hours in [0-168]hs
            if not (0 <= int(arg) and  int(arg) <= 168) :
               raise
        return arg
    except Exception:
        raise


def main():

    start_date = None
    offset = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "start_date=", "offset="])
    except getopt.GetoptError as err:
        usage()

    valid_start_date = False
    valid_offset = False
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
        else:
            usage()
    if not valid_offset or not valid_start_date:
        usage()

    try:
        environment = define_environment(start_date, offset)
        load_configuration(environment)
        run_process_model(environment)
    except Exception:
        raise

if __name__ == "__main__":

    main()

