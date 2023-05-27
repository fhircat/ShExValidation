#!/bin/bash
# ############################
# author: Deepak Sharma
# email: m2dks@yahoo.com
# ############################
#
DIR=.
source $DIR/setup_shexjs.sh

SHEX_PATH=../fhir_rdf_validation/ShExSchemas/R5Plus
#SHEX_PATH=~/runtime_environments/ShExSchemas
LOG_DIR=../logs/shex

# Create run time log directory, if not created already
mkdir -p $LOG_DIR
search_dir=${SHEX_PATH}
echo "[$(date)] Started in the directory $SHEX_PATH"
count=0
for entry in "$search_dir"/*.shex
do
  # remove everything till teh last "/" and retrieve the shex file name
  shex_entry=$(echo "${entry##*/}")
  logFile=${LOG_DIR}/${shex_entry}.log
  count=$((count+1))
  echo "$count. Processing [$shex_entry]..."
  echo $'\t'output to log file $logFile
  echo "*************** Validating $shex_entry ****************" > $logFile
  echo "Started: $(date)" >> $logFile
  validate --human -x $SHEX_PATH/$shex_entry --dry-run --diagnose || echo fail >> $logFile
  echo "Ended: $(date)" >> $logFile
done
echo "[$(date)] Ended!"
