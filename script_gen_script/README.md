# Command Line validation with shex.js library
FHIR RDF data validation with shex.js library on command line with the FHIR R5 ShEx Schemas R5 Test for Structure and Constraint Patterns

## Preparation
The shex.js project is available at https://github.com/shexjs/shex.js

### Clone the repository

` git clone git@github.com:shexjs/shex.js --branch main --depth 1 `

- once it is cloned, make sure `packages/shex-cli/bin` directory is in path.

### Usage of shex.js validate command

`validate -x <ShEx_Schema_file_name> -d <FHIR_rdf_data_ttl_file_name> -m '<instance_name>@<focus_shape>'`

Examples:
- validate and get human friendly error messages, if it fails.
  - `validate --human -x ../fhir_rdf_validation/ShExSchemas/R5Plus/Account.shex -d ../fhir_rdf_validation/FHIR_RDF_Examples/R5/account-example.ttl -m '{FOCUS a fhir:Account}@<Account>'`

- validate a shex shape only - to check if it is a valid shex shape
  - `validate -x packages/shex-cli/test/Imports/TrompPersonMissingRep/Issue.shex --diagnose --dry-run || echo fail`
