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

```
validate

  validate nodes in RDF graphs with respect to ShEx schemas.

Synopsis

  validate (-x <ShExC> | -j <ShExJ>) -s <start shape> (-d <Turtle> | -l <JSON-
  LD>) -n <start node>
  validate (-x |-j)? (-s)? (-d|-l)? (-n)? -S http://localhost:8088/validate

Options

  -v, --verbose                            print extra information
  -q, --quiet                              don't print anything
  -Q, --terse                              don't print diagnistics or advice
  --human                                  print human-readable results
  --query                                  show matching RDF graph
  --remainder                              show triples not touched by validation
  --grep
  --list
  --track                                  display graph nodes touched by validation
  --slurp                                  record minimal neighborhoods needed by validation
  --slurp-all                              record complete neighborhoods visited by validation. implies --slurp; may be
                                           the same as --slurp, depending on the databse
  -h, --help                               print usage information and quit
  -n, --node RDFTerm                       node to validate
  -t, --node-type IRI                      validate nodes of this type
  -m, --queryMap string                    QueryMap
  -M, --mapURL file|URL                    QueryMap
  -s, --shape IRI|Bnode                    shape to validate
  -x, --schemaURL file|URL                 ShExC schema
  -j, --json file|URL                      ShExJ schema
  -d, --dataURL file|URL                   Turtle data
  -l, --jsonld file|URL                    JSON-LD data
  --endpoint IRI                           data query endpoint
  --extension file glob                    ShExC schema
  --result file|URL                        expected JSON results
  -S, --serve URL                          server
  --serve-n integer                        serve N times and exit
  --exec javascript code                   run some js code with results
  --duplicate-shape abort|replace|ignore   what to do with duplicate shapes
  --diagnose                               parse and diagnose schema, the exit
  --skipCycleCheck                         don't look for cycles in schema
  --coverage firstError|exhaustive         whether to collect all errors or stop on the first one
  --yaml-manifest file|URL                 JSON manifest
  --json-manifest file|URL                 JSON manifest
  --turtle-manifest file|URL               Turtle manifest
  --jsonld-manifest file|URL               JSON-LD manifest
  --test-name IRI                          what tests to run in the manifest (.name OR .schemaLabel/.dataLabel)
  -i, --invocation
  -N, --dry-run
  --regex-module js module                 what regular expression module to use

Examples

  validate local files by node and shape:   validate -x ../../shex.js/packages/shex-cli/test/cli/1dotOr2dot.shex -d ../../shex.js/packages/shex-cli/test/cli/p2p3.ttl -n x -s http://a.example/S1
  validate local files with a ShapeMap:     validate -x ../../shex.js/packages/shex-cli/test/cli/1dotOr2dot.shex -d ../../shex.js/packages/shex-cli/test/cli/p2p3.ttl -m '<x>@<http://a.example/S1>'
  validate local files with a QueryMap:     validate -x ../../shex.js/packages/shex-cli/test/cli/1dotOr2dot.shex -d ../../shex.js/packages/shex-cli/test/cli/p2p3.ttl -m '{FOCUS :p2 _}@<http://a.example/S1>'
  validate web resources:                   validate -x http://shex.io/examples/IssueSchema.shex -d http://shex.io/examples/Issue1.ttl -m '<#Issue1>@<#IssueShape>'
  validate schema:                          validate -x http://shex.io/examples/IssueSchema.shex --diagnose
  run as a server:                          validate -S http://localhost:8088/validate
                                            curl -i http://localhost:8088/validate -F "schema=@../../shex.js/packages/shex-cli/test/cli/1dotOr2dot.shex" -F "shape=http://a.example/S1" -F "data=@../../shex.js/packages/shex-cli/test/cli/p2p3.ttl"
                                            -F "node=x"
  run as a preloaded server:                validate -x ../../shex.js/packages/shex-cli/test/cli/1dotOr2dot.shex -s http://a.example/S1 -S http://localhost:8088/validate
                                            curl -i http://localhost:8088/validate -F "data=@../../shex.js/packages/shex-cli/test/cli/p2p3.ttl" -F "node=x"

  Project home: https://github.com/shexSpec/shex.js
```