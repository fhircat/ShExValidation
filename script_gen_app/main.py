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
    append_script('#!/bin/bash\n')
    append_script('\nsource ./utils/check_server.sh')
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

    list_of_valid_rdfs = ['ActivityDefinition-activitydefinition-servicerequest-example.ttl.log', 'ActorDefinition-actordefinition-client.ttl.log', 'ActorDefinition-actordefinition-server.ttl.log', 'AllergyIntolerance-allergyintolerance-nkda.ttl.log', 'Appointment-appointment-example2doctors.ttl.log', 'AppointmentResponse-appointmentresponse-example-loc.ttl.log', 'AppointmentResponse-appointmentresponse-example-req.ttl.log', 'AuditEvent-audit-event-example-login.ttl.log', 'AuditEvent-audit-event-example-vread.ttl.log', 'AuditEvent-auditevent-example-consent-authz.ttl.log', 'AuditEvent-auditevent-example-disclosure.ttl.log', 'AuditEvent-auditevent-example.ttl.log', 'Basic-basic-example-narrative.ttl.log', 'Binary-binary-example.ttl.log', 'BiologicallyDerivedProduct-biologicallyderivedproduct-example-autologousHCT.ttl.log', 'BiologicallyDerivedProductDispense-biologicallyderivedproductdispense-example.ttl.log', 'BodyStructure-bodystructure-example-fetus.ttl.log', 'BodyStructure-bodystructure-example-skin-patch.ttl.log', 'BodyStructure-bodystructure-example-tumor.ttl.log', 'Bundle-bundle-lipids.ttl.log', 'Bundle-bundle-request-medsallergies.ttl.log', 'Bundle-bundle-request-simplesummary.ttl.log', 'Bundle-diagnosticreport-example-f001-bloodexam.ttl.log', 'Bundle-diagnosticreport-example-ghp.ttl.log', 'Bundle-diagnosticreport-example.ttl.log', 'Bundle-document-example-dischargesummary.ttl.log', 'Bundle-message-response-link.ttl.log', 'Bundle-notification-full-resource-with-patient.ttl.log', 'Bundle-notification-id-only.ttl.log', 'Bundle-practitioner-examples-general.ttl.log', 'Bundle-practitionerrole-examples-general.ttl.log', 'Bundle-questionnaire-profile-example-ussg-fht.ttl.log', 'CarePlan-careplan-example-GPVisit.ttl.log', 'ChargeItemDefinition-chargeitemdefinition-ebm-example.ttl.log', 'Claim-claim-example-cms1500-medical.ttl.log', 'Claim-claim-example-institutional-rich.ttl.log', 'Claim-claim-example-oral-bridge.ttl.log', 'Claim-claim-example-oral-contained.ttl.log', 'Claim-claim-example-professional.ttl.log', 'Claim-claim-example-vision.ttl.log', 'ClaimResponse-claimresponse-example-2.ttl.log', 'ClaimResponse-claimresponse-example-vision-3tier.ttl.log', 'CodeSystem-codesystem-example-summary.ttl.log', 'Communication-communication-example.ttl.log', 'Composition-composition-example.ttl.log', 'ConceptMap-conceptmap-message-adt-a04-to-bundle.ttl.log', 'Condition-condition-example-f001-heart.ttl.log', 'Condition-condition-example-family-history.ttl.log', 'Condition-condition-example-stroke.ttl.log', 'Condition-condition-example2.ttl.log', 'Consent-consent-example-CDA.ttl.log', 'Consent-consent-example-Emergency.ttl.log', 'Consent-consent-example-notThem.ttl.log', 'Consent-consent-example-notTime.ttl.log', 'Consent-consent-example-pkb.ttl.log', 'Contract-contract-example-42cfr-part2.ttl.log', 'Contract-contract-example-ins-policy.ttl.log', 'Contract-pcd-example-notAuthor.ttl.log', 'Coverage-coverage-example-2.ttl.log', 'DetectedIssue-detectedissue-example-lab.ttl.log', 'DetectedIssue-detectedissue-example.ttl.log', 'Device-device-example-ANDThermometer.ttl.log', 'Device-device-example-AndroidGatewayPHG.ttl.log', 'Device-device-example-Nonin20601PulseOx.ttl.log', 'Device-device-example-PhilipsThermometer.ttl.log', 'Device-device-example-pacemaker.ttl.log', 'Device-device-example-specimen-container-lavender-vacutainer.ttl.log', 'DeviceDefinition-devicedefinition-example.ttl.log', 'DeviceDispense-devicedispense-example.ttl.log', 'DeviceMetric-devicemetric-example.ttl.log', 'DeviceRequest-devicerequest-example.ttl.log', 'DeviceRequest-devicerequest-left-lens.ttl.log', 'DeviceRequest-devicerequest-right-lens.ttl.log', 'DiagnosticReport-diagnosticreport-example-gingival-biopsy.ttl.log', 'DiagnosticReport-diagnosticreport-example-ultrasound.ttl.log', 'DocumentReference-DocumentReference-WES_FullSequencedRegion_GRCh38.ttl.log', 'DocumentReference-DocumentReference-genomicBEDfile.ttl.log', 'DocumentReference-DocumentReference-genomicFile3.ttl.log', 'DocumentReference-DocumentReference-genomicFile4.ttl.log', 'DocumentReference-DocumentReference-genomicFileGroupAsSubject.ttl.log', 'DocumentReference-DocumentReference-genomicFileMother.ttl.log', 'DocumentReference-DocumentReference-genomicVCFfile.ttl.log', 'DocumentReference-DocumentReference-genomicVCFfile_cnv.ttl.log', 'DocumentReference-DocumentReference-genomicVCFfile_simple.ttl.log', 'DocumentReference-documentreference-example-bundle.ttl.log', 'DocumentReference-documentreference-example-dicom.ttl.log', 'DocumentReference-documentreference-example-sound.ttl.log', 'Encounter-Encounter-denovoEncounter.ttl.log', 'Encounter-Encounter-genomicEncounter.ttl.log', 'Encounter-encounter-example-colonoscopy.ttl.log', 'Encounter-encounter-example-f003-abscess.ttl.log', 'EnrollmentRequest-enrollmentrequest-example.ttl.log', 'EnrollmentResponse-enrollmentresponse-example.ttl.log', 'EventDefinition-eventdefinition-example.ttl.log', 'Evidence-evidence-example-ASTRAL-12-alteplase-mRS3-6.ttl.log', 'Evidence-evidence-example-stroke-alteplase-fatalICH.ttl.log', 'EvidenceVariable-evidencevariable-example-alive-independent-90day.ttl.log', 'EvidenceVariable-evidencevariable-example-eligibility-criteria-ada-rec-bariatric.ttl.log', 'EvidenceVariable-evidencevariable-example-eligibility-criteria-adults-with-obesity.ttl.log', 'EvidenceVariable-evidencevariable-example-mRS3-6-at-90days.ttl.log', 'ExplanationOfBenefit-explanationofbenefit-example.ttl.log', 'FamilyMemberHistory-familymemberhistory-example-mother.ttl.log', 'FamilyMemberHistory-familymemberhistory-example-negation.ttl.log', 'Flag-flag-example-encounter.ttl.log', 'GenomicStudy-genomicstudy-example-lungMass.ttl.log', 'GenomicStudy-genomicstudy-example-trio2.ttl.log', 'Goal-goal-example.ttl.log', 'Group-Group-denovoFamily.ttl.log', 'Group-group-example-member.ttl.log', 'GuidanceResponse-guidanceresponse-example.ttl.log', 'ImagingSelection-imagingselection-example-basic-image-selection.ttl.log', 'ImagingSelection-imagingselection-example-dicom-sr-selection.ttl.log', 'ImagingSelection-imagingselection-example-segmentation-image-selection.ttl.log', 'ImagingStudy-imagingstudy-example.ttl.log', 'Immunization-immunization-example-historical.ttl.log', 'Immunization-immunization-example-protocol.ttl.log', 'Immunization-immunization-example-reaction.ttl.log', 'ImmunizationEvaluation-immunizationevaluation-example.ttl.log', 'ImmunizationRecommendation-immunizationrecommendation-example.ttl.log', 'InventoryReport-inventoryreport-example.ttl.log', 'Invoice-invoice-example.ttl.log', 'Linkage-linkage-example.ttl.log', 'List-list-example-long.ttl.log', 'List-list-example-medlist.ttl.log', 'List-list-example-xds.ttl.log', 'List-list-example.ttl.log', 'Location-location-example-room.ttl.log', 'Location-location-example.ttl.log', 'Medication-medicationexample0302.ttl.log', 'Medication-medicationexample0303.ttl.log', 'Medication-medicationexample0305.ttl.log', 'Medication-medicationexample0306.ttl.log', 'Medication-medicationexample0307.ttl.log', 'Medication-medicationexample0311.ttl.log', 'Medication-medicationexample0312.ttl.log', 'Medication-medicationexample0313.ttl.log', 'Medication-medicationexample0314.ttl.log', 'Medication-medicationexample0317.ttl.log', 'Medication-medicationexample15.ttl.log', 'MedicationAdministration-medicationadministration0304.ttl.log', 'MedicationAdministration-medicationadministration0308.ttl.log', 'MedicationAdministration-medicationadministration0310.ttl.log', 'MedicationAdministration-medicationadministrationexample3.ttl.log', 'MedicationStatement-medicationstatementexample8.ttl.log', 'MedicationStatement-medicationstatementexample9.ttl.log', 'MedicinalProductDefinition-medicinalproductdefinition-example-co-packaged-liquid-and-syringe-complete.ttl.log', 'MedicinalProductDefinition-medicinalproductdefinition-example.ttl.log', 'MessageDefinition-messagedefinition-example.ttl.log', 'NamingSystem-namingsystem-example.ttl.log', 'NutritionIntake-nutritionintake-example.ttl.log', 'NutritionOrder-nutritionorder-example-cardiacdiet.ttl.log', 'Observation-observation-example-10minute-apgar-score.ttl.log', 'Observation-observation-example-20minute-apgar-score.ttl.log', 'Observation-observation-example-2minute-apgar-score.ttl.log', 'Observation-observation-example-alcohol-type.ttl.log', 'Observation-observation-example-bgpanel.ttl.log', 'Observation-observation-example-bloodgroup.ttl.log', 'Observation-observation-example-bmd.ttl.log', 'Observation-observation-example-body-weight-with-arabic-code.ttl.log', 'Observation-observation-example-clinical-gender.ttl.log', 'Observation-observation-example-date-lastmp.ttl.log', 'Observation-observation-example-f003-co2.ttl.log', 'Observation-observation-example-f203-bicarbonate.ttl.log', 'Observation-observation-example-glasgow-qa.ttl.log', 'Observation-observation-example-glasgow.ttl.log', 'Observation-observation-example-rhstatus.ttl.log', 'Observation-observation-example-secondsmoke.ttl.log', 'Observation-observation-example-spirometry.ttl.log', 'Observation-observation-example-vp-oyster.ttl.log', 'Observation-observation-example.ttl.log', 'OperationOutcome-operationoutcome-example-allok.ttl.log', 'OperationOutcome-operationoutcome-example-break-the-glass.ttl.log', 'OperationOutcome-operationoutcome-example-validationfail.ttl.log', 'OperationOutcome-operationoutcome-example.ttl.log', 'Organization-organization-example-f201-aumc.ttl.log', 'Organization-organization-example-f203-bumc.ttl.log', 'Organization-organization-example-gastro.ttl.log', 'Organization-organization-example-good-health-care.ttl.log', 'OrganizationAffiliation-orgrole-example-hie.ttl.log', 'PackagedProductDefinition-packagedproductdefinition-example-co-packaged-liquid-and-syringe.ttl.log', 'Patient-Patient-denovoFather.ttl.log', 'Patient-Patient-genomicPatient.ttl.log', 'Patient-patient-example-animal.ttl.log', 'Patient-patient-example-f001-pieter.ttl.log', 'Patient-patient-example-infant-mom.ttl.log', 'Patient-patient-example-mom.ttl.log', 'Patient-patient-example-proband.ttl.log', 'Patient-patient-example-xds.ttl.log', 'Patient-patient-genetics-example1.ttl.log', 'PaymentNotice-paymentnotice-example.ttl.log', 'Permission-permission-example-vhdir.ttl.log', 'Permission-permission-example.ttl.log', 'Person-person-grahame.ttl.log', 'Person-person-patient-portal.ttl.log', 'Practitioner-practitioner-example-f004-rb.ttl.log', 'Practitioner-practitioner-example-f005-al.ttl.log', 'Practitioner-practitioner-example-f006-rvdb.ttl.log', 'Practitioner-practitioner-example-f201-ab.ttl.log', 'Practitioner-practitioner-example-f202-lm.ttl.log', 'Practitioner-practitioner-example-f204-ce.ttl.log', 'Practitioner-practitioner-example-prac4.ttl.log', 'Practitioner-practitioner-example-xcda-author.ttl.log', 'Practitioner-practitioner-example-xcda1.ttl.log', 'Procedure-procedure-example-appendectomy-narrative.ttl.log', 'Procedure-procedure-example-colon-biopsy.ttl.log', 'Procedure-procedure-example-colonoscopy.ttl.log', 'Procedure-procedure-example-education.ttl.log', 'Procedure-procedure-example-f001-heart.ttl.log', 'Procedure-procedure-example-f002-lung.ttl.log', 'Procedure-procedure-example-f003-abscess.ttl.log', 'Procedure-procedure-example-implant.ttl.log', 'Provenance-provenance-example-advanced.ttl.log', 'Provenance-provenance-example-biocompute-object.ttl.log', 'Provenance-provenance-example-import.ttl.log', 'Provenance-provenance-example.ttl.log', 'Questionnaire-questionnaire-child-rel-demo.ttl.log', 'Questionnaire-questionnaire-example-practitioner-info.ttl.log', 'RegulatedAuthorization-regulatedauthorization-example-basic-drug-auth.ttl.log', 'RegulatedAuthorization-regulatedauthorization-example.ttl.log', 'RelatedPerson-RelatedPerson-denovoFather.ttl.log', 'RelatedPerson-relatedperson-example-newborn-mom.ttl.log', 'RelatedPerson-relatedperson-example-peter.ttl.log', 'RelatedPerson-relatedperson-example.ttl.log', 'RiskAssessment-riskassessment-example.ttl.log', 'ServiceRequest-ServiceRequest-genomicSRFather.ttl.log', 'ServiceRequest-ServiceRequest-genomicSRProband.ttl.log', 'ServiceRequest-ServiceRequest-genomicServiceRequest2.ttl.log', 'ServiceRequest-ServiceRequest-genomicServiceRequest3.ttl.log', 'ServiceRequest-servicerequest-example-edu.ttl.log', 'ServiceRequest-servicerequest-example-implant.ttl.log', 'ServiceRequest-servicerequest-example-lipid.ttl.log', 'ServiceRequest-servicerequest-example-pt.ttl.log', 'ServiceRequest-servicerequest-example.ttl.log', 'Slot-slot-example-busy.ttl.log', 'Slot-slot-example-unavailable.ttl.log', 'Specimen-Specimen-denovo-1.ttl.log', 'Specimen-Specimen-denovo-2.ttl.log', 'Specimen-Specimen-denovo-3.ttl.log', 'Specimen-Specimen-specimenMother.ttl.log', 'Specimen-specimen-example-pooled-serum.ttl.log', 'SpecimenDefinition-specimendefinition-example-serum-plasma.ttl.log', 'StructureMap-structuremap-example.ttl.log', 'Substance-substance-example-f203-potassium.ttl.log', 'Substance-substance-example.ttl.log', 'SubstanceProtein-substanceprotein-example.ttl.log', 'SupplyDelivery-supplydelivery-example-mphodelivery.ttl.log', 'Task-task-example-fm-cancel.ttl.log', 'Task-task-example-fm-poll.ttl.log', 'Task-task-example2.ttl.log', 'Task-task-example3.ttl.log', 'Task-task-example4.ttl.log', 'TestPlan-testplan-example.ttl.log', 'Transport-transport-example.ttl.log', 'ValueSet-valueset-example-cpt-all.ttl.log', 'ValueSet-valueset-nhin-purposeofuse.ttl.log']
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
                    # append_script(f"\nset -x; validate --skipCycleCheck --human -x ${{SCHEMAS}}{schema_url} -d ${{EXAMPLES}}{data_url} -m \"{{FOCUS a fhir:{shex_name}}}@<{shex_name}>\" > ${{LOGS}}{log_file} ; set +x; ")

                    if log_file not in list_of_valid_rdfs:
                        append_script(f"\ncheck_validation_server; set -x; curl -i --max-time 180 http://localhost/validate -F \"data=@./fhir_rdf_validation/{data_url}\" -F \"queryMap={{FOCUS a fhir:{shex_name} }}@<{shex_name}>\" > ${{LOGS}}{log_file} ; set +x ;")
                    else:
                        print("found")

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
