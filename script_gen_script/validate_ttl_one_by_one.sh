#!/bin/bash
# ############################
# author: Deepak Sharma
# email: m2dks@yahoo.com
# ############################
#
DIR=.
source $DIR/setup_shexjs.sh

YAML_PATH=../fhir_rdf_validation
LOG_DIR=../logs/rdfs

# Create run time log directory, if not created already
mkdir -p $LOG_DIR
search_dir=${YAML_PATH}
echo "[$(date)] Started in the directory $YAML_PATH"
echo "This reads each YAML file and creates individual validate command for each RDF data file (ttl)"
count=0
for entry in "$search_dir"/*.yaml
do
  # remove everything till teh last "/" and retrieve the yaml file name
  yaml_entry=$(echo "${entry##*/}")
  logFile=${LOG_DIR}/${yaml_entry}.log
  count=$((count+1))
  echo "$count. Processing [$yaml_entry]..."
  echo $'\t'output to log file $logFile

  echo "Started: $(date)" >> $logFile
  #validate --human --yaml-manifest $YAML_PATH/$yaml_entry >> $logFile
  echo "Ended: $(date)" >> $logFile
done
echo "[$(date)] Ended!"

set -x
validate --human - --yaml-manifest ${YAML_PATH}/ActivityDefinition.yaml
set +x
