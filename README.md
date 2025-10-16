# CosmicCounter
Cronjob script to list Cosmics runs on webpage (cronjob on vocms)

Webpage of the tool: https://cosmictkcounter.web.cern.ch/

Steps of the script:
- Search for runs in Run Registry 
- For those runs, search for their datasets in DQM GUI
- Rerieve the number of LS (from OMS) and Tracks (from DQM GUI)
- If the run is not in the cache:
  - Saves its properties (Run, LS, Tracks, ...)
- Update .html and data on eos (to be displayed as webpage)


## Setup on vocms

1) Go to top folder 
```
cd /data/users/event_display/dpgtkdqm/cronjobs/ 
```

2) Create main folder 
```
mkdir CosmicsCounter 
cd CosmicsCounter
``` 

3) Setup CMS environment 
```
source /cvmfs/cms.cern.ch/cmsset_default.sh 
```
 
4) Download and compile CMSSW 
```
scram project CMSSW_14_0_14 
cd CMSSW_14_0_14/src/ 
cmsenv 
scram b -j 10 
``` 

5) Go to main folder 
```
cd /data/users/event_display/dpgtkdqm/cronjobs/CosmicsCounter
```
 
6) Get the code from GitHub
```
git clone https://github.com/CMSTrackerDPG/CosmicsCounter.git
```

7) Enter and create Data folder (otherwise nothing is saved)
```
cd CosmicsCounter 
mkdir Data 
```
 
8) Modify the secret codes (not stored on git online) for new SSO authenticatiom 
```
emacs cosmicCount.sh 
```

9) Fix the year & minimum run number  
```
emacs cosmicCount.sh 
```

9.1) Change 2025 and 398080
```
#Change values in this line: python3 cosmicsCounting.py -y 2025 --min 389000
```

10) Eventually import (or clean) the cache

Cache is stored inside file tracks-by-run.txt

11) Test execution 
```
source cosmicCount.sh
```

12) Edit the cronjob list
```
crontab -e
```

12.1) Add the cronjob details (every hour, at minute 10)

```
10 */1 * * * /data/users/event_display/dpgtkdqm/cronjobs/CosmicsCounter/CosmicsCounter/cosmicCount.sh > /data/users/event_display/dpgtkdqm/cronjobs/cronlogs/CosmicsCounter_cron.log 2>&1
```