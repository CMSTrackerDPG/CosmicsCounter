#!/bin/sh
#kerberos authentication
kdestroy
kinit -k -t /data/users/event_display/dpgtkdqm/dpgtkdqm.keytab dpgtkdqm
klist 
eosfusebind 
aklog CERN.CH

##Only update the CMSSW release
CMSSW_REL=CMSSW_14_0_14
source /cvmfs/cms.cern.ch/cmsset_default.sh

PARENT_PATH=/data/users/event_display/dpgtkdqm/cronjobs/CosmicsCounter
echo "Parent path:"$PARENT_PATH

WORK_DIR=$PARENT_PATH/CosmicsCounter/
CMSSW_DIR=$PARENT_PATH/$CMSSW_REL/src/
OUTPUT_DIR="/eos/user/d/dpgtkdqm/www/CosmicTkCounter/"
echo $CMSSW_DIR
cd $CMSSW_DIR
eval `scramv1 ru -sh`

cd $WORK_DIR
echo "Inside work dir:"$WORK_DIR

#needed for new SSO authenticatiom
export SSO_CLIENT_ID="AskToTkDQMConveners" 
export SSO_CLIENT_SECRET="AskToTkDQMConveners" 

python3 cosmicsCounting.py -y 2025 --min 389000
echo "xrdcp -f index.html root://eosuser.cern.ch//$OUTPUT_DIR/"
xrdcp -f index.html root://eosuser.cern.ch//$OUTPUT_DIR/
echo "xrdcp -f Data/* root://eosuser.cern.ch//$OUTPUT_DIR/data/"
xrdcp -f Data/* root://eosuser.cern.ch//$OUTPUT_DIR/data/
