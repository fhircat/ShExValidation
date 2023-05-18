import os
import re
import utils
from dotenv import load_dotenv
from pathlib import Path
from os import listdir


def initialize():
    utils.delete_files(manifests_absolute_path, ".yaml")
    utils.delete_files(manifests_absolute_path, ".md")


def append_readme(text):
    with open(manifests_readme_path, 'a+') as readme:
        readme.write(text)


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
                    schema_url = os.path.join(shex_schemas_relative_path, shex_name + '.shex')
                    data_label = rdf_file.split(".")[0]
                    data_url = os.path.join(rdf_examples_relative_path, rdf_file)

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
                            f"{spacing}status: conformant{spacing}");

                    # Create Entry in the dictionary of manifests
                    yaml_file_name = os.path.join(manifests_relative_path, manifest_file_name)
                    update_manifest(shex_name, yaml_file_name)
                else:
                    print(f'---------- ERROR! Could not map for File: {rdf_file} ------------')
                    errors.append(rdf_file)
        else:
            skip.append(rdf_file)
    return manifests, processed, errors, skip, total


if __name__ == '__main__':
    project_base_path = os.path.dirname(os.path.realpath(__file__))
    load_dotenv()
    project_path= utils.get_project_root()

    # ShEx Schemas
    shex_schemas_relative_path=utils.get_env_val('SHEX_SCHEMAS_DIR')
    shex_schemas_absolute_path=utils.get_env_path('SHEX_SCHEMAS_DIR')

    # Turtle Examples
    rdf_examples_relative_path=utils.get_env_val('RDF_EXAMPLES_DIR')
    rdf_examples_absolute_path=utils.get_env_path('RDF_EXAMPLES_DIR')

    # Manifest Files
    manifests_relative_path = utils.get_env_val('MANIFEST_FILES_DIR')
    manifests_absolute_path = utils.get_env_path('MANIFEST_FILES_DIR')
    manifests_readme_path = os.path.join(manifests_absolute_path, 'README.md')

    # ShEx Validator
    shex_validator_prefix = utils.get_env_val('SHEX_VALIDATOR_URL_PREFIX')

    print(f'* Project Path: {project_path}')
    print(f"* RDF Examples are at: {rdf_examples_absolute_path}")
    print(f"* Manifests are at: {manifests_absolute_path}")
    print(f"* Manifests are at: {manifests_readme_path}")
    print(f"* ShEx Validator prefix: {shex_validator_prefix}")

    manifests = {}
    initialize()
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

