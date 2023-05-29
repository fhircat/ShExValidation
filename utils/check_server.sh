#!/bin/bash
process="ShEx.shex"

function check_validation_server() {
  date
  if ! pgrep -qf "$process"; then
    echo "Validation Server is not running, waiting 45 seconds to validate..."
    sleep 45
  else
    echo "Validation Server is running... Validating now...."
  fi
}