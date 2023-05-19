# ShExValidation
A Project to generate artifacts to help in ShEx Schema validation and RDF data validation with ShEx Schemas


### Configuration - only if you want to generate new set of manifest files and other scripts
- Create `.env` file or define following environment variables
```
RDF_EXAMPLES_DIR=fhir_rdf_validation/FHIR_RDF_Examples/R5
DATA_URL_PREFIX=FHIR_RDF_Examples/R5
SCHEMAS_URL_PREFIX=ShExSchemas/R5Plus
MANIFEST_FILES_DIR=fhir_rdf_validation
SHEX_VALIDATOR_URL_PREFIX=https://shex.io/webapps/packages/extension-map/doc/shexmap-simple?manifestURL=https://fhircat.github.io/ShExValidation/
```
### Usage:
View the table on the page [fhir_rdf_validation](..) and choose which resource examples you want to validate.