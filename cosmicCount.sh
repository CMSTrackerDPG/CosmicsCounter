#!/bin/sh
#kerberos authentication
kdestroy
kinit -k -t /home/dpgtkdqm/dpgtkdqm.keytab dpgtkdqm
klist 
eosfusebind 
aklog CERN.CH

##Only update the CMSSW release
CMSSW_REL=CMSSW_14_0_0
source /cvmfs/cms.cern.ch/cmsset_default.sh

PARENT_PATH=/home/dpgtkdqm/cronjobs/cosmictkcounter/
echo "Parent path:"$PARENT_PATH

WORK_DIR=$PARENT_PATH/CosmicsCount/
CMSSW_DIR=$PARENT_PATH/$CMSSW_REL/src/
OUTPUT_DIR="/eos/user/d/dpgtkdqm/www/CosmicTkCounter/"
echo $CMSSW_DIR
cd $CMSSW_DIR
eval `scramv1 ru -sh`

cd $WORK_DIR
echo "Inside work dir:"$WORK_DIR

#needed for new SSO authenticatiom
export SSO_CLIENT_ID="dcsonly"
export SSO_CLIENT_SECRET="e4c56fdb-6494-4bce-a2cc-b170b9a6e910"

python3 cosmicsCounting.py --min 376680
echo "xrdcp -f index.html root://eosuser.cern.ch//$OUTPUT_DIR/"
xrdcp -f index.html root://eosuser.cern.ch//$OUTPUT_DIR/
echo "xrdcp -f Data/* root://eosuser.cern.ch//$OUTPUT_DIR/data/"
xrdcp -f Data/* root://eosuser.cern.ch//$OUTPUT_DIR/data/

#xrdcp -f TEST/*.png root://eosuser.cern.ch//$OUTPUT_DIR/data/
#xrdcp -f TEST/*.root root://eosuser.cern.ch//$OUTPUT_DIR/data/


