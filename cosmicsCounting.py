from math import *
from dqmjson import *
from ROOT import TFile, gStyle, TCanvas, TH1F, TLegend
from ROOT import kBlue, kGreen
from optparse import OptionParser
from xml.dom.minidom import parseString
#from omsapi import getInfo
import runregistry
import xmlrpc
#import elementtree.ElementTree as ET
import sys, os, os.path, time, re, subprocess
import urllib
import json

from plot_generator import generate_plot
from html_generator import generate_html
##Run classification
groupName = "Collisions18" #TO_BE_CHANGED_EACH_YEAR
##Dataset for GUI query
express = '/StreamExpressCosmics/'
prompt  = '/Cosmics/'
##
yearPattern = ".*22" # select anything with a 17 in the name #TO_BE_CHANGED_EACH_YEAR
#Recotype= ["Online", "Prompt"]
Recotype= ["Online", "Express","Prompt"]
##
runlist = {}
##
dsetExpress={}
dsetPrompt={}


def getInfo(run):
    data=runregistry.get_run(run_number=run)
    bfield=data["oms_attributes"]["b_field"]
    duration=data["oms_attributes"]["duration"]
    lastLS=data["oms_attributes"]["last_lumisection_number"]
    return (bfield,duration,lastLS)


def isExpressDoneInGUI(run):
    global dsetExpress
    try:
        dataset = dsetExpress[int(run)]#"%s%s-%s/DQMIO" % (express[Dtype], eraForRun(run), getErForRun(run))
        info = dqm_get_json(serverurl, run, dataset, "Info/ProvInfo")
        done = info['runIsComplete']['value']
        return done == '1'
    except:
        return False 
    return False



def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


def RRrunsList(minRun,maxRun):
    runs = runregistry.get_datasets(filter={'dataset_name':{'like':'%Express%Cosmics%'},'run_number':{'and':[{'>':minRun},{'<':maxRun}]}})
    rlist = [r['run_number'] for r in runs]
    return rlist

def main():
    ####Cosmics settings are set after loading config options#####
    global groupName,express,prompt,yearPattern,Recotype,runlist,dsetExpress,dsetPrompt
    parser = OptionParser()
    parser.add_option("-c", "--cosmics", dest="cosmics", action="store_true",  default=False, help="Check cosmic instead of collision")
#    parser.add_option("-C", "--commissioning", dest="commissioning", action="store_true",  default=False, help="Check commssioning instead of collision")
    parser.add_option("-m", "--min", dest="min", type="int", default=0,      help="Minimum run")
    parser.add_option("-M", "--max", dest="max", type="int", default=999999, help="Maximum run")
    parser.add_option("-y", "--year", dest="year", type="string", default="2024", help="Year")
    parser.add_option("--min-ls",    dest="minls",  type="int", default="10",   help="Ignore runs with less than X lumis (default 10)")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",  default=False, help="Print more info")
    parser.add_option("-p", "--pretend", dest="pretend", action="store_true",  default=False, help="Use cached RR result")
    parser.add_option("-f", "--force", dest="force", action="store_true",  default=False, help="Never cached RR result")
#    parser.add_option("-n", "--notes", dest="notes", type="string", default="notes.txt", help="Text file with notes")
    (options, args) = parser.parse_args()
    
    ##Cosmic settings...
    ##NOTE: Currently using prompt stream (not express) for central data certification
    if len(options.year)!=4:
        print("Insert the year in the 4-digit format (i.e 2018)")
        return
    yearPattern=".*"+options.year[2:4]
    groupName = "Cosmics"+options.year[2:4] #TO_BE_CHANGED_EACH_YEAR
    
    print(yearPattern)
    print(groupName)


    lumiCache = {}; 
    lumiCacheName = "Data/tracks-by-run.txt"
        
    print("Cache Used : {0}".format(lumiCacheName))
    try:
        lumiFile = open(lumiCacheName, "r")
        for l in lumiFile:
            m = re.match(r"(\d+)\s+(\d+)\s+([0-9.]+).*", l)
            if m:
                cols = l.split()
                print(cols)
                lumiCache[str(cols[0])] = [ int(cols[1]), int(cols[2]), int(cols[3]), float(cols[4]), cols[5], cols[6], cols[7].replace("_"," "), int(cols[8])] 
        print("LUMICACHE " , lumiCache)
        lumiFile.close()
    except IOError:
        print("Cache not readable or not present!")
        pass 



    print("Querying runs from DQM GUI")
    ed = express
    pd = prompt
    RRruns=RRrunsList(options.min, options.max)
    for n,d in (('Express',ed), ('Prompt',pd)):
        samples = dqm_get_samples(serverurl, d+yearPattern)
        for (r, d2) in samples:
            #if r<options.min or r>options.max: continue
            if r not in RRruns: continue
            if "DQMIO" in d2 : 
                if 'Express' in n:
                    dsetExpress[int(r)]=d2
                if 'Prompt' in n:
                    dsetPrompt[int(r)]=d2
            runlist.update({str(r): {'GUI_'+str(n) :True}})
 
    print("Getting tracks")
    newcache = open("Data/tracks-by-run.txt", "w");
    newcache.write("run\tls\talcatracks\tduration\tBfield\tmode\tmode_flag\tmode_text\tpixeltracks\n");
    for run in runlist.keys():
        if run not in lumiCache.keys():
            print(" - ",run)
            #All DECO runs (since webapp is not available) <--- Aug 2024
            dbmode = "DECO"
            lslumi = (-1,-1,-1,-1,"DECO","WAIT","no info on DB (run not in prompt GUI yet)",-1)
            #dbmode = '???'
            #link = "http://cern.ch/erik.butz/cgi-bin/getReadOutmode.pl?RUN=" + str(run)
            #f = urllib.request.urlopen(link)
            #json_data = f.read()
            #dbmodelist = json.loads(json_data)
            #print(dbmodelist)
            #if len(dbmodelist) != 0:
            #    dbmode = dbmodelist[0][1]
            #    lslumi = (-1,-1,-1,-1,dbmode,"WAIT","from DB mode (run not in prompt GUI yet)",-1)
            #else:
            #    lslumi = (-1,-1,-1,-1,"NONE","WAIT","no info on DB (run not in prompt GUI yet)",-1)
            try:
                #dataset = "%s%s-%s/DQMIO" % (prompt[1], eraForRun(run), getPrForRun(run))
                dataset = dsetPrompt[int(run)]
                bfield,duration,nlumis=getInfo(int(run))
                print("DATASET " , dataset)
                print("INFO B: %.1fT RunTime: %d LS: %d" % (bfield,duration,nlumis))
                at = dqm_get_json(serverurl, run, dataset, "AlCaReco/TkAlCosmics0T/HitProperties/Pixel",True)
                #at = dqm_get_json(serverurl, run, dataset, "AlCaReco/TkAlCosmics0T/GeneralProperties")
                ei = dqm_get_json(serverurl, run, dataset, "Info/EventInfo")
                tib =dqm_get_json(serverurl, run, dataset, "SiStrip/MechanicalView/TIB")
                nalcatracks = at['NumberOfRecHitsPerTrack_Pixel_ALCARECOTkAlCosmicsCTF0T']['rootobj'].GetEntries()
                nalcatracks_pixel = at['NumberOfRecHitsPerTrack_Pixel_ALCARECOTkAlCosmicsCTF0T']['rootobj'].Integral(2,25)
                #nalcatracks = at['Chi2Prob_ALCARECOTkAlCosmicsCTF0T']['nentries']
                ston_num = tib['Summary_ClusterStoNCorr_OnTrack__TIB']['nentries']
                ston_avg = tib['Summary_ClusterStoNCorr_OnTrack__TIB']['stats']['x']['mean']
                mode = "???"; mode_flag = 'bah'; mode_text = 'not found'
                if ston_num > 100:
                    if 28 < ston_avg and ston_avg < 35: mode, mode_flag, mode_text = "PEAK", "TODO", "from S/N plot";
                    if 15 < ston_avg and ston_avg < 24: mode, mode_flag, mode_text = "DECO", "TODO", "from S/N plot";
                if mode == dbmode:
                    mode, mode_flag, mode_text = dbmode, "GOOD","from both DB and S/N"
                elif mode == "???":
                    mode, mode_flag, mode_text = dbmode, "WAIT","from DB only (S/N info is inconclusive)"
                else:
                    mode, mode_flag, mode_text = dbmode+"?", "BAD","DB says %s, but mean S/N = %.1f suggests %s" % (dbmode,ston_avg,mode)
                lslumi = (nlumis, nalcatracks, duration, bfield, mode, mode_flag, mode_text, nalcatracks_pixel)
                print("Adding to cache")
            except:
                print("Something wrong on getting PROMP run")
                pass
            print(lslumi[1])
            if lslumi[1] == -1:
                try:
                    dataset = dsetExpress[int(run)]
                    bfield,duration,nlumis=getInfo(int(run))
                    print("DATASET " , dataset)
                    print("INFO B: %.1fT RunTime: %d LS: %d" % (bfield,duration,nlumis))
                    at = dqm_get_json(serverurl, run, dataset, "AlCaReco/TkAlCosmics0T/HitProperties/Pixel",True)#"AlCaReco/TkAlCosmics0T/GeneralProperties")
                    ei = dqm_get_json(serverurl, run, dataset, "Info/EventInfo")
                    nalcatracks = at['NumberOfRecHitsPerTrack_Pixel_ALCARECOTkAlCosmicsCTF0T']['rootobj'].GetEntries() #at['Chi2Prob_ALCARECOTkAlCosmicsCTF0T']['nentries']
                    nalcatracks_pixel = at['NumberOfRecHitsPerTrack_Pixel_ALCARECOTkAlCosmicsCTF0T']['rootobj'].Integral(2,25)
                    if nlumis > 0:
                        lslumi = (-nlumis,nalcatracks,-duration,bfield,dbmode,"WAIT","from DB mode (run not in prompt GUI yet)",nalcatracks_pixel)
                    print(lslumi)
                except:
                    print("Something wrong on getting EXPRESS run")
                    pass
            print("LSLUMI cosmics ", lslumi)
            lumiCache[str(run)] = lslumi
        else:
            print("- %s already on Cache" % run)
        print("%d\t%d\t%d\t%d\t%.1f\t%s\t%s\t%s\t%d\n" % (int(run), 
                                                       lumiCache[run][0], lumiCache[run][1], 
                                                       lumiCache[run][2], lumiCache[run][3], 
                                                       lumiCache[run][4], lumiCache[run][5], lumiCache[run][6].replace(" ","_"),lumiCache[run][7]))


        if lumiCache[run][0] >= 0:
            newcache.write("%d\t%d\t%d\t%d\t%.1f\t%s\t%s\t%s\t%d\n" % (int(run), 
                                                                   lumiCache[run][0], lumiCache[run][1], 
                                                                   lumiCache[run][2], lumiCache[run][3],                                      
                                                                   lumiCache[run][4], lumiCache[run][5], lumiCache[run][6].replace(" ","_"),lumiCache[run][7]))

    newcache.close()

    print("Done")


    allLumi_currentCRUZET=0
    allLumi_currentCRAFT=0.00000
    allTime_currentCRUZET=0
    allTime_currentCRAFT=0.000001
    allAlcaTracks_currentCRUZET=0
    allAlcaTracks_currentCRAFT=0
    allLumiWait=0
    allTracksWait=0
    maxcosmicrunforstat = 0
    mincosmicrunforstat = 999999
    maxcruzetrunforstat = 0
    mincruzetrunforstat = 999999
    allAlcaTracksPEAK=0
    
    info_run_track_CRUZET = []; 
    info_run_time_CRUZET = []; 
    info_run_track_CRAFT = []; 
    info_run_time_CRAFT = []; 

    #PIXEL
    allLumi_pix_currentCRUZET=0
    allLumi_pix_currentCRAFT=0.00000
    allTime_pix_currentCRUZET=0
    allTime_pix_currentCRAFT=0.000001
    allAlcaTracks_pix_currentCRUZET=0
    allAlcaTracks_pix_currentCRAFT=0
    maxcosmicrunforstat_pix = 0
    mincosmicrunforstat_pix = 999999
    maxcruzetrunforstat_pix = 0
    mincruzetrunforstat_pix = 999999
    info_run_pix_track_CRUZET = []; 
    info_run_pix_time_CRUZET = []; 
    info_run_pix_track_CRAFT = []; 
    info_run_pix_time_CRAFT = [];

    
    runs = list(runlist.keys()); runs.sort(); runs.reverse()
    print("ALL RUNS: " , runs , "\n")
    for r in runs:
        if abs(lumiCache[r][0]) >= 1:
            if lumiCache[r][3] < 3.6: #0T cosmics (CRUZET)  
                if lumiCache[r][1] > 0:
                    allLumi_currentCRUZET=allLumi_currentCRUZET+abs(lumiCache[r][0])
                    allTime_currentCRUZET=allTime_currentCRUZET+abs(lumiCache[r][2])
                allAlcaTracks_currentCRUZET=allAlcaTracks_currentCRUZET+abs(lumiCache[r][1])
                maxcruzetrunforstat = max(maxcruzetrunforstat, int(r)) #should only be in the current era
                mincruzetrunforstat = min(mincruzetrunforstat, int(r)) #should only be in the current era
                info_run_track_CRUZET.append([r, lumiCache[r][1]])
                info_run_time_CRUZET.append([r, lumiCache[r][2]])
                #PIXEL
                if lumiCache[r][7] > 0:
                    allLumi_pix_currentCRUZET=allLumi_pix_currentCRUZET+abs(lumiCache[r][0])
                    allTime_pix_currentCRUZET=allTime_pix_currentCRUZET+abs(lumiCache[r][2])
                allAlcaTracks_pix_currentCRUZET=allAlcaTracks_pix_currentCRUZET+abs(lumiCache[r][7])
                maxcruzetrunforstat_pix = max(maxcruzetrunforstat_pix, int(r)) #should only be in the current era
                mincruzetrunforstat_pix = min(mincruzetrunforstat_pix, int(r)) #should only be in the current era
                info_run_pix_track_CRUZET.append([r, lumiCache[r][7]])
                info_run_pix_time_CRUZET.append([r, lumiCache[r][2]])
            elif lumiCache[r][3] >= 3.6: #3.8T cosmics (CRAFT)
                if lumiCache[r][1] > 0:
                    allLumi_currentCRAFT=allLumi_currentCRAFT+abs(lumiCache[r][0])
                    allTime_currentCRAFT=allTime_currentCRAFT+abs(lumiCache[r][2])
                allAlcaTracks_currentCRAFT=allAlcaTracks_currentCRAFT+abs(lumiCache[r][1])
                maxcosmicrunforstat = max(maxcosmicrunforstat, int(r)) #should only be in the current era
                mincosmicrunforstat = min(mincosmicrunforstat, int(r)) #should only be in the current era
                info_run_track_CRAFT.append([r, lumiCache[r][1]])
                info_run_time_CRAFT.append([r, lumiCache[r][2]])
                #PIXEL
                if lumiCache[r][7] > 0:
                    allLumi_pix_currentCRAFT=allLumi_pix_currentCRAFT+abs(lumiCache[r][0])
                    allTime_pix_currentCRAFT=allTime_pix_currentCRAFT+abs(lumiCache[r][2])
                allAlcaTracks_pix_currentCRAFT=allAlcaTracks_pix_currentCRAFT+abs(lumiCache[r][7])
                maxcosmicrunforstat_pix = max(maxcosmicrunforstat_pix, int(r)) #should only be in the current era
                mincosmicrunforstat_pix = min(mincosmicrunforstat_pix, int(r)) #should only be in the current era
                info_run_pix_track_CRAFT.append([r, lumiCache[r][7]])
                info_run_pix_time_CRAFT.append([r, lumiCache[r][2]])

    #generate HTML
    generate_html(options.year,allAlcaTracks_currentCRUZET, allTime_currentCRUZET, mincruzetrunforstat, maxcruzetrunforstat, allAlcaTracks_pix_currentCRUZET, allTime_pix_currentCRUZET, mincruzetrunforstat_pix, maxcruzetrunforstat_pix, allAlcaTracks_currentCRAFT, allTime_currentCRAFT, mincosmicrunforstat, maxcosmicrunforstat, allAlcaTracks_pix_currentCRAFT, allTime_pix_currentCRAFT, mincosmicrunforstat_pix, maxcosmicrunforstat_pix)

    print(info_run_time_CRAFT)

    #print some info
    print("CRUZET "+options.year+" info:")
    print("AlCaReco Tracks: %.0fK in %.0f hours (%d runs)" % (allAlcaTracks_currentCRUZET / 1000. , abs(allTime_currentCRUZET / 3600.), len(info_run_track_CRAFT)))
    print("AlCaReco Pixel Tracks: %.0fK in %.0f hours (%d runs)" % (allAlcaTracks_pix_currentCRUZET / 1000. , abs(allTime_pix_currentCRUZET / 3600.), len(info_run_pix_track_CRAFT)))
    print("CRAFT "+options.year+" info:")
    print("AlCaReco Tracks: %.0fK in %.0f hours (%d runs)" % (allAlcaTracks_currentCRAFT / 1000. , abs(allTime_currentCRAFT / 3600.), len(info_run_track_CRUZET)))
    print("AlCaReco Pixel Tracks: %.0fK in %.0f hours (%d runs)" % (allAlcaTracks_pix_currentCRAFT / 1000. , abs(allTime_pix_currentCRAFT / 3600.), len(info_run_pix_track_CRUZET)))
    
    #Generate Plots
    fRout=TFile("Data/cosmics.root","RECREATE")
    fRout.cd()
    generate_plot("CRUZET",False,info_run_track_CRUZET, info_run_time_CRUZET, allAlcaTracks_currentCRUZET, allTime_currentCRUZET,fRout)
    generate_plot("CRUZET",True,info_run_pix_track_CRUZET, info_run_pix_time_CRUZET, allAlcaTracks_pix_currentCRUZET, allTime_pix_currentCRUZET,fRout)
    generate_plot("CRAFT",False,info_run_track_CRAFT, info_run_time_CRAFT, allAlcaTracks_currentCRAFT, allTime_currentCRAFT,fRout)
    generate_plot("CRAFT",True,info_run_pix_track_CRAFT, info_run_pix_time_CRAFT, allAlcaTracks_pix_currentCRAFT, allTime_pix_currentCRAFT,fRout)
    fRout.Write()
    fRout.Close()

    
if __name__ == '__main__':
    main()


