# 5/18/2023 (Updated)
# validates using Shex.js parser

# First location of the shex.js parser 
SHEXJS=~/A123/git/research/FHIRCat/shex.js
VALIDATE=$SHEXJS/packages/shex-cli/bin

set -x
export PATH=$VALIDATE:$PATH

# One way to invoke validate with YAML FILE
# YAML=./FunctionPatterns/FunctionPatterns.yaml
YAML=../fhir_rdf_validation/Account.yaml

# validate --help

# validate --verbose --human --yaml-manifest $YAML

# Another way of invoking validate with SHEX and TTL
SHEX=../fhir_rdf_validation/ShExSchemas/R5Plus/Account.shex
TTL=../fhir_rdf_validation/FHIR_RDF_Examples/R5/account-example.ttl

# validate shex with a ttl
validate --human -x $SHEX -d $TTL -m '{FOCUS a fhir:Account}@<Account>'
TTL=../fhir_rdf_validation/FHIR_RDF_Examples/R5/account-example-with-guarantor.ttl
validate --human -x $SHEX -d $TTL -m '{FOCUS a fhir:Account}@<Account>'

# validate for a select query map
# validate -x $SHEX -d $TTL -m '<inst_exists>@<FunctionPatternsShape>,<inst_noExists>@!<FunctionPatternsShape>'

# run it as a server
# validate -x ../fhir_rdf_validation/ShExSchemas/R5Plus/Account.shex --diagnose  --serve http://localhost/validate || echo fail

# example to check if ShEx schema has any error
# for example if they have duplicate shapes
# validate -x packages/shex-cli/test/Imports/TrompPersonMissingRep/Issue.shex --diagnose --dry-run || echo fail

# validate -x ../fhir_rdf_validation/ShExSchemas/R5Plus/Account.shex --dry-run --diagnose  || echo fail

set +x
