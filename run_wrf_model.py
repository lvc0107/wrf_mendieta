#! /usr/bin/python
import os
import argparse
import sys
import get_GFSX025_grib2 as grib
from datetime import datetime, timedelta
import time


# Default values. Editable by user

MAX_OFFSET = 168         # MAX_OFFSET == 168hs(7 days)
MIN_NODES_AMOUNT = 2
MAX_NODES_AMOUNT = 9
SEPARATOR = '-' * 80


def update_namelist_wps(environment):

    try:

        print SEPARATOR
        print "Set date for namelist.wps"

        ENSAMBLE_DIR = environment["ENSAMBLE_DIR"]
        os.chdir(ENSAMBLE_DIR)
        start_date = " start_date = {0}\n".format(environment["start_date"])
        end_date = " end_date = {0}\n".format(environment["end_date"])
        patterns = {"start_date": start_date, "end_date": end_date}

        namelist_wps = "namelist.wps"

        with open(namelist_wps) as infile:
            with open(namelist_wps, 'r+') as outfile:
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


def update_namelist_input_output(ensamble_path, environment):

    try:
        print SEPARATOR
        print "Set date for namelist.input in {0}".format(ensamble_path)

        ENSAMBLE_DIR = environment["ENSAMBLE_DIR"]
        os.chdir(ENSAMBLE_DIR + "/" + ensamble_path)

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
            with open('namelist.input', 'r+') as outfile:
                for line in infile:
                    for k, v in patterns.iteritems():
                        if k in line:
                            line = v
                            break
                    outfile.write(line)

        infile.close()
        outfile.close()
        os.system("head -15 namelist.input")

        print "Set date for namelist.ARWpost {0}".format(ensamble_path)

        start_date = " start_date = {0}\n".format(environment["start_date"])
        end_date = " end_date = {0}\n".format(environment["end_date"])
        input_root_name =  " input_root_name = '../wrf_run/wrfout_d01_{0}',\n".format(environment["start_date"])

        patterns = {
                    "start_date": start_date,
                    "end_date": end_date,
                    "input_root_name": input_root_name
                    }

        namelist_awr = "namelist.ARWpost"

        with open(namelist_awr) as infile:
            with open(namelist_awr, 'r+') as outfile:
                for line in infile:
                    for k, v in patterns.iteritems():
                        if k in line:
                            line = v
                            break
                    outfile.write(line)

        infile.close()
        outfile.close()
        os.system("head -15 {0}".format(namelist_awr))

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
            os.system("mkdir {0}".format(start_date_dir))

        gfs_path = GFS_DIR + "/" + start_date_dir
        grib.download_grib_files(start_date, offset, gfs_path)

    except Exception:
        raise


def load_configuration(environment, offset):

    try:

        update_namelist_wps(environment)
        ensamble_names = environment["ENSAMBLE"]
        for ensamble in ensamble_names:
            update_namelist_input_output(ensamble, environment)

    except Exception:
        raise


def run_process_model(environment, nodes):

    try:
        os.chdir(environment["WRF_BASE"])
        ensamble_names = environment["ENSAMBLE"]
        start_date = environment["start_date"]
        end_date = environment["end_date"]

        for ensamble in ensamble_names:
            print SEPARATOR
            execute_command = "sbatch job_wrf_{0}_nodes.sh {1} {2} {3}".format(nodes, ensamble, start_date, end_date)
            print execute_command
            os.system(execute_command)

        check_command = "squeue -u $USER"
        print check_command
        os.system(check_command)
    except Exception:
        raise


def get_ensamble_names(environment):
    """
      This function return a list of ensamble's names:
      [
       ensamble1,
       ensamble2,
       .
       .
       .
       ensambleN,
      ]
    """

    try:

        ENSAMBLE_DIR = environment["ENSAMBLE_DIR"]
        os.chdir(ENSAMBLE_DIR)
        ensamble_names = []
        subdirs = [x[0] for x in os.walk(ENSAMBLE_DIR)]
        for subdir in subdirs:
            ensamble_names.append(subdir.split("/")[-1])

        return ensamble_names[1:]

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
            print SEPARATOR
            print "Before run this script you should run: . ./set_configuration.sh"
            print SEPARATOR
            sys.exit(1)

        print "ENVIRONMENT VARIABLE LOADED: {0}".format(os.getenv("WRF_BASE"))
        environment["WRF_BASE"] = os.getenv("WRF_BASE")
        print "ENVIRONMENT VARIABLE LOADED: {0}".format(os.getenv("GFS_DIR"))
        environment["GFS_DIR"] = os.getenv("GFS_DIR")
        print "ENVIRONMENT VARIABLE LOADED: {0}".format(os.getenv("ENSAMBLE_DIR"))
        environment["ENSAMBLE_DIR"] = os.getenv("ENSAMBLE_DIR")
        environment["ENSAMBLE"] = get_ensamble_names(environment)

        return environment

    except Exception:
        raise


def usage(msg):

    print SEPARATOR
    print SEPARATOR
    print msg
    print SEPARATOR
    print SEPARATOR
    print """
       Execution of WRF model:

       ./run_wrf_model.py -i=STARTDATE -o=OFFSET -n=2
       or:
       ./run_wrf_model.py --start_date=STARTDATE --offset=OFFSET --nodes=2

       Where STARTDATE has the follow format: YYYYMMDDHH
       and OFFSET is an integer value that represent the forecast hours
       starting from the STARTDATE and defined in the range [0-MAX_OFFSET]hs.
       The MAX_OFFSET is currently defined in 168hs(a week),
       but it can be editable by the user, changing it in this file.

       The nodes flag is the number of:
       nodes in multi partition, with nodes in [2,8].
       This values can also be changed in this file editing the
       MIN_NODES_AMOUNT/MAX_NODES_AMOUNT variables

       Example:
       ./run_wrf_model.py -i=2018020218 -o=36 -n=2
       means Forecast of 36 hs starting from the date:
       year: 2018
       month: 02
       day: 02
       hour: 18
       forecast time: 36 hs

       running in 2 nodes of multi partition


       Warning: The date is valid only until 14 days behind
       This is a constrain from the GFS site
      """
    print SEPARATOR
    print SEPARATOR

    sys.exit(1)


def check_parameter(i, o, n):

    try:
        date = datetime.strptime(i, '%Y%m%d%H')
        if date < datetime.now() - timedelta(days=14):
            usage(msg="Date available until 14 days ago")
        if not int(o) in range(0, MAX_OFFSET + 1):
            usage(msg="Forecast's hours grater than 168hs")
        if not int(n) in range(MIN_NODES_AMOUNT, MAX_NODES_AMOUNT):
            usage(msg="Mendieta nodes out of allowed range")
    except ValueError:
        usage(msg="Error in the date format")



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
    start_date = None
    offset = None
    nodes = 2  # Default value in multi partition

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--start_date', help='Start date for a forecast')
    parser.add_argument('-o', '--offset', help='Amount of forecast hs')
    parser.add_argument('-n', '--nodes', help='Mendieta nodes'  )
    args = parser.parse_args()  

    if args.start_date and args.offset and args.nodes:
        start_date = args.start_date
        offset = args.offset
        nodes = args.nodes
        check_parameter(start_date, offset, nodes)
    else:
        usage("Insert all the parameters")

    try:
        environment = define_environment(start_date, offset)
        download_grib_files(environment, offset)
        load_configuration(environment, offset)
        run_process_model(environment, nodes)
    except Exception:
        raise


if __name__ == "__main__":
    main()
