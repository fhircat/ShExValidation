import os
import re
import utils
from dotenv import load_dotenv


def initialize():
    utils.delete_files(manifests_absolute_path, ".yaml")
    utils.delete_files(readme_path, ".md")
    utils.delete_files(scripts_dir, ".sh")


def append_readme(text):
    with open(manifests_readme_path, 'a+') as readme:
        readme.write(text)


def append_script(text):
    with open(script_name, 'a+') as script:
        script.write(text)


def create_script():
    append_script('\nSHEXJS=~/A123/git/research/FHIRCat/shex.js')
    append_script('\nVALIDATE=$SHEXJS/packages/shex-cli/bin')
    append_script('\nexport PATH=$VALIDATE:$PATH')
    append_script('\nSCHEMAS=/Users/DKS02/A123/git/research/FHIRCat/ShExValidation/fhir_rdf_validation/')
    append_script('\nEXAMPLES=/Users/DKS02/A123/git/research/FHIRCat/ShExValidation/fhir_rdf_validation/')
    append_script('\nLOGS=/Users/DKS02/A123/git/research/FHIRCat/ShExValidation/logs/rdfs/')
    # make file executable
    os.chmod(script_name, 0o755)


def create_readme(example_dict):
    my_keys = list(example_dict.keys())
    my_keys.sort()
    sorted_examples = {i: example_dict[i] for i in my_keys}

    append_readme('# Validate FHIR RDF Examples with ShEx Schemas \n\n| Resource | Examples |\n| --- | --- |')
    for shex, link in sorted_examples.items():
        parts = link.split('---')
        append_readme(f'\n| [{shex}]({shex_validator_prefix}{parts[1]}) | {parts[0]} |')


def update_manifest(shex_name, yaml_file_name):
    val = '1---' + yaml_file_name
    if shex_name in manifests:
        val = manifests[shex_name]
        vals = val.split("---")
        # if an entry exists, it means this is another example
        # for the same schema; increase the count
        ct = 1 + int(vals[0])
        val = f'{ct}---{vals[1]}'

    # update the dictionary of manifests
    manifests[shex_name] = val


def process_examples():
    exdir = os.listdir(rdf_examples_absolute_path)
    processed = []
    errors = []
    skip = []
    total = len(exdir)

    for rdf_file in exdir:
        if rdf_file.endswith(".ttl"):
            print(f'Processing file: {rdf_file}')
            with open(os.path.join(rdf_examples_absolute_path, rdf_file), "r") as rdf_example:
                contents = rdf_example.read()
                # the content of the RDF example file starts with type arc:
                # a fhir: <shex schema name>
                m = re.search('a fhir:(.+?);', contents)
                if m:
                    processed.append(rdf_file)
                    # matching name will indicate the shex schema name
                    matching_name = m.group(1)

                    # Entries for manifest block
                    shex_name = matching_name.strip()
                    schema_url = os.path.join(shex_schemas_url_prefix, shex_name + '.shex')
                    data_label = rdf_file.split(".")[0]
                    data_url = os.path.join(data_url_prefix, rdf_file)

                    # Append this example into appropriate manifest file
                    manifest_file_name = shex_name + '.yaml'
                    spacing = "\n  "
                    yaml_file_to_write = os.path.join(manifests_absolute_path, manifest_file_name)
                    with open(yaml_file_to_write, 'a+') as yf:
                        yf.write(
                            f"\n- schemaLabel: {shex_name}"
                            f"{spacing}schemaURL: {schema_url}"
                            f"{spacing}dataLabel: {data_label}"
                            f"{spacing}dataURL: {data_url}"
                            f"{spacing}queryMap: \"{{FOCUS a fhir:{shex_name}}}@<{shex_name}>\""
                            f"{spacing}status: conformant{spacing}")

                    # Create Entry in the dictionary of manifests
                    yaml_file_name = os.path.join(manifests_relative_path, manifest_file_name)
                    update_manifest(shex_name, yaml_file_name)

                    # if len(processed) < 3:
                    log_file = f"{shex_name}-{rdf_file}.log"
                    append_script(f"\nset -x; validate --human -x ${{SCHEMAS}}{schema_url} -d ${{EXAMPLES}}{data_url} -m \"{{FOCUS a fhir:{shex_name}}}@<{shex_name}>\" > ${{LOGS}}{log_file} ; set +x; ")
                else:
                    print(f'---------- ERROR! Could not map for File: {rdf_file} ------------')
                    errors.append(rdf_file)
        else:
            skip.append(rdf_file)
    return manifests, processed, errors, skip, total


if __name__ == '__main__':
    project_base_path = os.path.dirname(os.path.realpath(__file__))
    load_dotenv()
    project_path = utils.get_project_root()

    readme_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # scripts directory
    scripts_dir = os.path.join(project_path, utils.get_env_val('SCRIPTS_DIR'))
    script_name = os.path.join(scripts_dir, utils.get_env_val('SCRIPT_NAME_TO_GENERATE'))
    log_dir = os.path.join(project_path, utils.get_env_val('LOG_DIR'))

    # ShEx Schemas - schemaURL
    shex_schemas_url_prefix = utils.get_env_val('SCHEMAS_URL_PREFIX')

    # RDF Examples - dataURL
    data_url_prefix = utils.get_env_val('DATA_URL_PREFIX')

    # Turtle Examples
    rdf_examples_relative_path = utils.get_env_val('RDF_EXAMPLES_DIR')
    rdf_examples_absolute_path = utils.get_env_path('RDF_EXAMPLES_DIR')

    # Manifest Files
    manifests_relative_path = utils.get_env_val('MANIFEST_FILES_DIR')
    manifests_absolute_path = utils.get_env_path('MANIFEST_FILES_DIR')
    manifests_readme_path = os.path.join(readme_path, 'README.md')

    # ShEx Validator
    shex_validator_prefix = utils.get_env_val('SHEX_VALIDATOR_URL_PREFIX')

    print(f'* Project Path: {project_path}')
    print(f"* RDF Examples are at: {rdf_examples_absolute_path}")
    print(f"* Manifests are at: {manifests_absolute_path}")
    print(f"* README.md is at: {manifests_readme_path}")
    print(f"* ShEx Validator prefix: {shex_validator_prefix}")
    print(f"* Script to validate rdf examples one by one is: {script_name}")
    print(f"* Log directory for the Script run -  to validate rdf examples one by one is: {log_dir}")

    manifests = {}
    initialize()
    create_script()
    example_list, success, fails, rest, whole = process_examples()
    succeed = len(success)
    failed = len(fails)
    skipped = len(rest)
    create_readme(example_list)

    print(f"* Pass: {success}")
    print(f"* Fail: {fails}")
    print(f"* Skipped: {rest}")

    print(f"* Pass: {succeed}")
    print(f"* Fail: {failed}")
    print(f"* Skipped: {skipped}")
    print(f"* Total: {whole}")
