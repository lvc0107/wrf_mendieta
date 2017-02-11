#0.5 x0 .5 horizontal resolution on the specified geographical domain
# and for the specified meteorological parameters only(slice, i.e.sub - area of global data)

import datetime
import urllib2
import sys
import os
import time

#############################################################################

def chunk_report():
    bar_len = 60
    filled_len = 0
    percents = 0
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...\r' % (bar, percents, '%'))
    sys.stdout.flush() 

def request(url, file):
  
    try:
        print file
        if os.path.exists(file):
            # TODO here add checksum verification
            return 0 
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print 'The server could not fulfill the request.'
        print 'Error code: ', e.code
        return e.code
    except IOError, e:
        print 'The server could not fulfill the request.'
        print 'IOError code: ', e
        return -1
    except urllib2.URLError, e:
        print 'Failed to reach a server.'
        print 'Reason: ', e.reason
        return -1
    else:
        w = open(file, 'w')
        w.write(response.read())

        chunk_size=8192
        while 1:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            chunk_report()
            w.write(chunk)

        response.close()
        w.close()
        return 0


def download_grib_files(start_date, offset, grib2_dir):

    INIDATE = start_date
    DIR_OPER_DATA = grib2_dir

    # Mode of managing: automatic(WORK_MODE = 'auto': automatic retrials) or manual(WORK_MODE = 'man')
    # WORK_MODE = 'man'
    WORK_MODE = 'auto'

    # Date of forecast start(analysis)
    DATE = INIDATE / 100
    # Instant(hour, UTC) of forecast start(analysis)

    FCI = INIDATE - DATE * 100

    # Archive tar - file creation option(ARCHIVE = True or ARCHIVE = False)
    ARCHIVE = False

    if ARCHIVE:
        DIR_ARCHIVE = DIR_OPER_DATA
    LON_W = "-96"
    LON_E = "-15"
    LAT_N = "-10"
    LAT_S = "-75"

    #Data grid resolution( in degree)

    ADGRID = "0.25"
    #can be: 0.25, 0.5, 1.0, 2.5

    # Defines connection timeout

    urllib2.socket.setdefaulttimeout(30)

    # Total forecast length( in hours) for which data are requested:
    NHOUR = int(offset)
    # Interval in hours between two forecast times:
    DHOUR = 03
    # Definiton of date( in required format)
    day = datetime.datetime.today()
    ### tomorrow = day + datetime.timedelta(days = 1)### yesterday = day + datetime.timedelta(days = -1)

    # If the download is made early in the morning, the date is that of yesterday

    #if day.hour < 6: #day = yesterday

    ### day = "%4.4i%2.2i%2.2i" % (day.year, day.month, day.day)# structure definition
    day = "%8.8i" % (DATE)

    FCIA = "%2.2i" % FCI

    print "Date and hour of GFS forecast initial time: ", day, FCI

    # Definition of servers name# The first in the list below of those available is used

    SERVER = []
    SERVER.append("nomads.ncep.noaa.gov/")

    # Definitions of server partial subdir.name

    SERV_PASS = "cgi-bin/"

    #Definition of requested levels and parameters

    LEV_LIST = ["all"]
    PAR_LIST = ["HGT", "LAND", "PRES", "PRMSL", "RH", "SOILW", "SPFH", "TMP", "UGRD", "VGRD", "WEASD", "TSOIL"]


    if WORK_MODE == "auto":
        COUNTMAX = 50
        icountmax = 100
        S_SLEEP1 = 600
        S_SLEEP2 = 60
    else:
        COUNTMAX = 1
        icountmax = 1
        S_SLEEP1 = 10
        S_SLEEP2 = 1

    NSERVER = len(SERVER)
    N_LEV_TYPE = 1
    NINSTANT = NHOUR / DHOUR + 1
    NFILE_REQUESTED = [NINSTANT, 1]
    FILE_NAME_DOMAIN = "&subregion=&leftlon=" + LON_W + "&rightlon=" + LON_E + "&bottomlat=" + LAT_S + "&toplat=" + LAT_N

    if ADGRID == "0.25":
        FILE_NAME_INI = "filter_gfs_0p25.pl"
        DIR_NAME = "&dir=%2Fgfs." + day + FCIA
    if ADGRID == "0.5":
        FILE_NAME_INI = "filter_gfs_hd.pl"
        DIR_NAME = "&dir=%2Fgfs." + day + FCIA + "%2Fmaster"
    if ADGRID == "1.0":
        FILE_NAME_INI = "filter_gfs.pl"
        DIR_NAME = "&dir=%2Fgfs." + day + FCIA
    if ADGRID == "2.5":
        FILE_NAME_INI = "filter_gfs_2p5.pl"
        DIR_NAME = "&dir=%2Fgfs." + day + FCIA

    # Full list of requested files

    LIST_FILE_REMOTE = []
    LIST_FLAG = []
    LIST_FILE_LOCAL_FIN = []
    NINST = NFILE_REQUESTED[0]
    for INST in range(0, NINST):
        if INST + 1 > NFILE_REQUESTED[0]:
            continue
        NLEV = len(LEV_LIST)
        NPAR = len(PAR_LIST)
        PARAMETERS = ""
        for IPAR in range(0, NPAR):
            PARAMETERS = PARAMETERS + "&var_" + PAR_LIST[IPAR] + "=on"
        LEVELS = ""
        if LEV_LIST[0] == "all":
            LEVELS = LEVELS + "&all_lev=on"
        else:
            for ILEV in range(0, NLEV):
                LEVELS = LEVELS + "&lev_" + LEV_LIST[ILEV] + "=on"
        HF = INST * DHOUR
        HFA = "%2.2i" % HF
        HFA2 = "%3.3i" % HF
        if ADGRID == "0.25":
            FILE_NAME_BASE = "?file=gfs.t" + FCIA + "z.pgrb2.0p25.f" + HFA2
        if ADGRID == "0.5":
            FILE_NAME_BASE = "?file=gfs.t" + FCIA + "z.mastergrb2f" + HFA
        if ADGRID == "1.0":
            FILE_NAME_BASE = "?file=gfs.t" + FCIA + "z.pgrbf" + HFA + ".grib2"
        if ADGRID == "2.5":
            FILE_NAME_BASE = "?file=gfs.t" + FCIA + "z.pgrbf" + HFA + ".2p5deg.grib2"
        FILE_REMOTE = FILE_NAME_INI + FILE_NAME_BASE + LEVELS + PARAMETERS + FILE_NAME_DOMAIN + DIR_NAME
        FILE_LOCAL_FIN = "GFS_" + day + FCIA + "+" + HFA2 + ".grib2"
        FLAG = 0
        LIST_FILE_REMOTE.append(FILE_REMOTE)
        LIST_FILE_LOCAL_FIN.append(FILE_LOCAL_FIN)
        LIST_FLAG.append(FLAG)

    NFILE = len(LIST_FLAG)

    # Dowloading of requested files
    WORK = True
    while WORK:
        for ISERVER in range(0, NSERVER):
            FILE_REMOTE0 = "http://" + SERVER[ISERVER] + SERV_PASS
            print 'Request in server: ', SERVER[ISERVER]

            COUNT = 1
            while COUNT <= COUNTMAX:
                print 'Attempt number: ', COUNT

                NREQ = 0
                NFLAG = 0
                for IFILE in range(0, NFILE):
                    if LIST_FLAG[IFILE] == 0:
                        NFLAG = NFLAG + 1
                        FILE_REMOTE = FILE_REMOTE0 + LIST_FILE_REMOTE[IFILE]
                        FILE_LOCAL = DIR_OPER_DATA + '/' + LIST_FILE_LOCAL_FIN[IFILE]

                        ierr = 100;
                        icount = 0
                        while ierr != 0 and icount <= icountmax:
                            icount = icount + 1
                            ierr = request(FILE_REMOTE, FILE_LOCAL)
                            print 'dowloading error= ', ierr
                            if ierr == 0: #successeful downloading
                                LIST_FLAG[IFILE] = 1
                                NREQ = NREQ + 1
                                print "Requested remote file downloaded in local file", FILE_LOCAL

                            else:#unsuccesseful downloading
                                print 'Data file', FILE_REMOTE, 'not downloaded! sleep ', S_SLEEP2, ' s'
                                time.sleep(S_SLEEP2)
                if NFLAG == NREQ:
                    WORK = False
                if WORK:
                    print "Not all requested files downloaded, sleeping", S_SLEEP1, "s before next trial"
                    time.sleep(S_SLEEP1)
                else:
                    print '*******************************************************'
                    print " All requested grib2 files downloaded !", day, FCI, 'UTC'
                    print '*******************************************************'
                    break
                COUNT = COUNT + 1
            if WORK:
                print "All acceptable attempts have been done in this server, sleeping ", S_SLEEP2, "s befor request other server"
                time.sleep(S_SLEEP2)
            else:
                break
        if not WORK:
            break
        else:
            if WORK_MODE == 'man':
                break
