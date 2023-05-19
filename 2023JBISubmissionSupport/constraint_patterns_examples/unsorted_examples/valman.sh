# 5/7/2023
# validates using Shex.js parser

# First location of the shex.js parser 
SHEXJS=/Users/DKS02/A123/git/research/FHIRCat/shex.js
VALIDATE=$SHEXJS/packages/shex-cli/bin
WORKDIR=/Users/DKS02/A123/git/research/FHIRCat/validation


set -x
cd $WORKDIR

export PATH=$VALIDATE:$PATH

# One way to invoke validate with YAML FILE
# YAML=./FunctionPatterns/FunctionPatterns.yaml
YAML=./2023JBISubmissionSupport/fhir_rdf_examples_validation/Account.yaml

# validate --human --yaml-manifest $YAML

# Another way of invoking validate with SHEX and TTL
SHEX=./2023JBISubmissionSupport/fhir_rdf_examples_validation/ShExSchemas/R5Plus/Account.shex
TTL=./2023JBISubmissionSupport/fhir_rdf_examples_validation/FHIR_RDF_Examples/R5/account-example.ttl

# validate shex with a ttl
validate --human -x $SHEX -d $TTL -m '{FOCUS a fhir:Account}@<Account>'

# validate for a select query map
# validate -x $SHEX -d $TTL -m '<inst_exists>@<FunctionPatternsShape>,<inst_noExists>@!<FunctionPatternsShape>'

# run it as a server
# validate -x ../validation/ShExSchemas/R5/Observation.shex --diagnose  --serve http://localhost/validate || echo fail

# example to check if ShEx schema has any error
# for example if they have duplicate shapes
# validate -x packages/shex-cli/test/Imports/TrompPersonMissingRep/Issue.shex --diagnose --dry-run || echo fail
set +x
