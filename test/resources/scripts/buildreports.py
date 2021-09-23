import jinja2
import csv
import uuid

#Load all the templates
templateLoader = jinja2.FileSystemLoader(searchpath="../templates")
templateEnv = jinja2.Environment(loader=templateLoader,trim_blocks=True,lstrip_blocks=True)
patient_template = templateEnv.get_template("patient.xml.jinja")
requester_template = templateEnv.get_template("requester.xml.jinja")
performer_template = templateEnv.get_template("performer.xml.jinja")
request_template = templateEnv.get_template("procedurerequest.xml.jinja")
message_header_template = templateEnv.get_template("messageheader.xml.jinja")
bundle_template = templateEnv.get_template("reportbundle.xml.jinja")
diagnostic_report_template = templateEnv.get_template("diagnosticreport.xml.jinja")
specimen_template = templateEnv.get_template("specimen.xml.jinja")
observation_template = templateEnv.get_template("observation.xml.jinja")
#Open the test data csv
#For each row:
#generate uuids for patient,requester,performer,request,message header, bundle
#and identifiers
# build patient
# build requester
# build performer
# build request
# build message header
# build bundle

def load_test_data(report_data_csv="../templates/ReportsTestDataSetup.csv",request_data_csv="../templates/RequestsTestDataSetup.csv"):
    request_rows = []
    with open(request_data_csv,encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel')
        for row in reader:
            request_rows.append(row)
    with open(report_data_csv,encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel')
        counter = 0
        for row in reader:
            request_id = int(row["RequestId"])
            request = request_rows[request_id-1]
            #Drop the id from the request row
            if "Id" in request:
                del(request["Id"])
            yield {**row, **request} # N.B Python >=3.5
            counter = counter + 1

def build_patient(uuid,nhs_number,family_name,given_name,gender,birthdate):
    patient = patient_template.render(patient_uuid=uuid,
                                    nhs_number=nhs_number,
                                    family_name=family_name,
                                    given_name=given_name,
                                    gender=gender,
                                    birthdate=birthdate)
    return patient

def build_performer(uuid,identifier,name,address,city,district,postcode):
    performer = performer_template.render(performer_uuid=uuid,
                                        performer_identifier=identifier,
                                        performer_name=name,
                                        performer_address_line=address,
                                        performer_city=city,
                                        performer_district=district,
                                        performer_postcode=postcode)
    return performer

def build_requester(uuid,identifier,name,address,city,district,postcode):
    requester = requester_template.render(requester_uuid=uuid,
                                        requester_identifier=identifier,
                                        requester_name=name,
                                        requester_address_line=address,
                                        requester_city=city,
                                        requester_district=district,
                                        requester_postcode=postcode)
    return requester

def build_request(uuid,identifier,status,request_utl_code,request_utl_display,patient_uuid,patient_display,
            authored_on,requester_uuid,requester_display,performer_uuid,performer_display,request_utl_display_code,requisition_id=None):

    request = request_template.render(request_uuid=uuid,
                                        request_identifier=identifier,
                                        request_status=status,
                                        request_utl_code=request_utl_code,
                                        request_utl_display=request_utl_display,
                                        patient_uuid=patient_uuid,
                                        patient_display=patient_display,
                                        authored_on=authored_on,
                                        requester_agent_uuid=requester_uuid,
                                        requester_agent_display=requester_display,
                                        performer_uuid=performer_uuid,
                                        performer_display=performer_display,
                                        request_utl_display_code=request_utl_display_code,
                                        requisition_id=requisition_id)
    return request

def build_diagnostic_report(uuid,basedon_uuid,status,patient_uuid,patient_display,
            issuedon,performer_uuid,performer_display,specimen_uuids,result_uuids):

    diagnostic_report = diagnostic_report_template.render(report_uuid=uuid,
                                                            basedon_uuid=basedon_uuid,
                                                            status=status,
                                                            patient_uuid=patient_uuid,
                                                            patient_display=patient_display,
                                                            issuedon=issuedon,
                                                            performer_uuid=performer_uuid,
                                                            performer_display=performer_display,
                                                            specimen_uuids=specimen_uuids,
                                                            result_uuids=result_uuids)
    return diagnostic_report

def build_specimen(uuid,specimen_identifier,status,code,display,patient_uuid,patient_display,
                    received_time,collected_time,quantity_value,quantity_unit):
    
    specimen = specimen_template.render(specimen_uuid=uuid,
                                    specimen_identifier=specimen_identifier,
                                    status=status,
                                    code=code,
                                    display=display,
                                    patient_uuid=patient_uuid,
                                    patient_display=patient_display,
                                    received_time=received_time,
                                    collected_time=collected_time,
                                    quantity_value=quantity_value,
                                    quantity_unit=quantity_unit)
    return specimen

def build_values_dictionary(record):
    value_dict = {}
    if "value.quantity.value" in record:
        value_dict =  {"quantity":{"value":record["value.quantity.value"],
                "unit":record["value.quantity.unit"]}}
    if "value.codeable.system" in record:
        values_dict = {"codeable":
                        {"system":record["value.codeable.system"],
                        "code":record["value.codeable.code"],
                        "display":record["value.codeable.display"]}}
    if "value.string.value" in record:
        values_dict = {"string":{"value":record["value.string.value"]}}
    if "value.boolean.value" in record:
        values_dict = {"boolean":{"value":record["value.boolean.value"]}}
    if "value.range.low.value" in record:
        values_dict = {"range":
                        {"low":{"value":record["value.range.low.value"],
                                "unit":record["value.range.low.unit"]},
                        "high":{"value":record["value.range.high.value"],
                                "unit":record["value.range.high.unit"]}
                        }
        }
    if "value.ratio.numerator.value" in record:
        values_dict = {"ratio":
                        {"numerator":
                            {"value":record["value.ratio.numerator.value"]},
                        "denominator":
                            {"value":record["value.ratio.denominator.value"]}
                        }
        }
    if "value.sample.origin.value" in record:
        values_dict = {"sample":
                        {"origin":
                            {"value":record["value.sample.origin.value"],
                            "unit":record["value.sample.origin.unit"],
                            "system":record["value.sample.origin.system"],
                            "code":record["value.sample.origin.code"]},
                        "period":record["value.sample.period"],
                        "factor":record["value.sample.factor"]},
                        "sampled":{"dimensions":record["value.sampled.dimensions"],
                                    "data":record["value.sampled.data"]}
        }
    if "value.attachment.content_type" in record:
        values_dict = {"attachment":{"content_type":record["value.attachment.content_type"],
                                    "language":record["value.attachment.language"],
                                    "data":record["value.attachment.data"],
                                    "title":record["value.attachment.title"]}}
    if "value.time.value" in record:
        values_dict = {"time":{"value":record["value.time.value"]}}
    if "value.datetime.value" in record:
        values_dict = {"datetime":{"value":record["value.datetime.value"]}}
    if "value.period.start" in record:
        values_dict = {"period":{"start":record["value.period.start"],
                                "end":record["value.period.end"]}}
    if "value.reference.low_reference" in record:
        values_dict = {"reference":{"low_reference":record["value.reference.low_reference"],
                                    "high_reference":record["value.reference.high_reference"]}}

    return value_dict
"""
valuesDictionary is a single item dictionary which maps to the flexible value types in the observation. 
The key is one of:
quantity
codeable
string
boolean
range
ratio
sampled
attachement
time
period

and the value is a dictionary of items required to populate the value. 
See the observation template (or the FHIR spec) for a clue on what to include!

For example. To pass a valuePeriod one would use:
{"period":{"start":"somevalue","end":"somevalue"}}
"""
def build_observation(uuid,observation_identifier,status,code,display,patient_uuid,patient_display,
                        effective_datetime,performer_uuid,performer_display,specimen_uuid,
                        valuesDictionary,reference=None,related_uuids=[]):

    observation = observation_template.render(observation_uuid=uuid,observation_identifier=observation_identifier,
                                                status=status,
                                                code=code,
                                                display=display,
                                                patient_uuid=patient_uuid,
                                                patient_display=patient_display,
                                                effective_datetime=effective_datetime,
                                                performer_uuid=performer_uuid,
                                                performer_display=performer_display,
                                                specimen_uuid=specimen_uuid,
                                                value=valuesDictionary,
                                                reference=reference,
                                                related_uuids=related_uuids)
    return observation


def build_message_header(uuid,receiver_uuid,sender_uuid,timestamp,endpoint,focus_uuid):
    header = message_header_template.render(message_header_uuid=uuid,
                                            receiver_uuid=receiver_uuid,
                                            sender_uuid=sender_uuid,
                                            timestamp=timestamp,
                                            endpoint=endpoint,
                                            focus_uuids=focus_uuid)
    return header

def build_bundle(uuid,identifier,header,header_uuid,requester,requester_uuid,
                    performer,performer_uuid,patient,patient_uuid,procedures,procedure_uuid,
                    diagnostic_report_uuid,diagnostic_report,specimens,specimen_uuid,observations,observation_uuid):
    bundle = bundle_template.render(bundle_uuid=uuid,
                                    bundle_identifier=identifier,
                                    message_header_resource=header,
                                    message_header_uuid=header_uuid,
                                    requester_resource=requester,
                                    requester_uuid=requester_uuid,
                                    performer_resource=performer,
                                    performer_uuid=performer_uuid,
                                    patient_resource=patient,
                                    patient_uuid=patient_uuid,
                                    procedure_request_resources=procedures,
                                    request_uuid=procedure_uuid,
                                    diagnostic_report_uuid=diagnostic_report_uuid,
                                    diagnostic_report=diagnostic_report,
                                    specimens=specimens,
                                    specimen_uuid=specimen_uuid,
                                    observations=observations,
                                    observation_uuid=observation_uuid
                                    )
    return bundle

def build_simple_report(record):
    patient_uuid = uuid.uuid4()
    requester_uuid = uuid.uuid4()
    performer_uuid = uuid.uuid4()
    request_uuid = uuid.uuid4()
    message_header_uuid = uuid.uuid4()
    bundle_uuid = uuid.uuid4()
    diagnostic_report_uuid = uuid.uuid4()
    specimen_uuid = uuid.uuid4()
    observation_uuid = uuid.uuid4()
    patient = build_patient(patient_uuid,record["NHS Number"],
                            record["Family Name"],
                            record["Given Name"],
                            record["Gender"],
                            record["Birthdate"])
    performer = build_performer(performer_uuid,
                                record["Performer Identifier"],
                                record["Performer Org"],
                                record["Performer Address"],
                                record["Performer City"],
                                record["Performer District"],
                                record["Performer Postcode"])
    requester = build_requester(requester_uuid,
                                record["Requester Identifier"],
                                record["Requester Org"],
                                record["Requester Address"],
                                record["Requester City"],
                                record["Requester District"],
                                record["Requester Postcode"])
    request = build_request(request_uuid,uuid.uuid4(),"active",
                            record["Code"],
                            record["Display"],
                            patient_uuid,
                            "%s,%s" % (record["Family Name"],record["Given Name"]),
                            "2019-06-04",
                            requester_uuid,
                            record["Requester Org"],
                            performer_uuid,
                            record["Performer Org"],
                            record["DisplayCode"])
    diagnostic_report = build_diagnostic_report(diagnostic_report_uuid,
                            request_uuid,
                            record["ReportStatus"],
                            patient_uuid,
                            "%s,%s" % (record["Family Name"].upper(),record["Given Name"]),
                            record["Issuedon"],
                            performer_uuid,
                            record["Requester Org"],
                            [specimen_uuid,],
                            [observation_uuid,])
    specimen = build_specimen(specimen_uuid, uuid.uuid4(), 
                                record["SpecimenStatus"], 
                                record["SpecimenCode"],
                                record["SpecimenDisplay"], 
                                patient_uuid, 
                                "%s,%s" % (record["Family Name"].upper(),record["Given Name"]), 
                                record["SpecimenReceivedTime"],
                                record["SpecimenCollectedTime"], 
                                record["SpecimenQuantityValue"],
                                record["SpecimenQuantityUnit"])

    observation_values = build_values_dictionary(record)

    observation = build_observation(observation_uuid, uuid.uuid4(),
                                record["ObservationStatus"],
                                record["ObservationCode"], 
                                record["ObservationDisplay"],
                                patient_uuid, 
                                "%s,%s" % (record["Family Name"].upper(),record["Given Name"]), 
                                record["ObservationEffectiveDatetime"],
                                performer_uuid,
                                record["Requester Org"], 
                                specimen_uuid, 
                                observation_values)

    header = build_message_header(message_header_uuid,performer_uuid,requester_uuid,
                            "2019-03-14T10:10:16+00:00","NOROT003",[request_uuid,])
    
    bundle = build_bundle(bundle_uuid,uuid.uuid4(),
                        header,message_header_uuid,
                        requester,requester_uuid,
                        performer,performer_uuid,
                        patient,patient_uuid,
                        [request,],[request_uuid,],
                        diagnostic_report_uuid, diagnostic_report,
                        [specimen],[specimen_uuid,],
                        [observation],[observation_uuid,])
    print(bundle)
    output_name = "../examples/reports/%s_report.xml" % (record["Report"].replace(" ","_"))
    f = open(output_name,"w",encoding="utf-8")
    f.write(bundle)       
    f.close()

def build_profile_reports(profile_records):
    for profile in profile_records:
        requests = []
        request_ids = []
        specimens = []
        specimen_ids = []
        specimen_groups = [] #A specimen is only included once per group
        observations = []
        observation_ids = []
        print(profile_records[profile])
        #Use the first request for patient etc.
        record = profile_records[profile][0]
        patient_uuid = uuid.uuid4()
        requester_uuid = uuid.uuid4()
        performer_uuid = uuid.uuid4()
        request_uuid = uuid.uuid4()
        message_header_uuid = uuid.uuid4()
        requisition_id = uuid.uuid4()
        bundle_uuid = uuid.uuid4()
        diagnostic_report_uuid = uuid.uuid4()
        patient = build_patient(patient_uuid,record["NHS Number"],
                                record["Family Name"],
                                record["Given Name"],
                                record["Gender"],
                                record["Birthdate"])
        performer = build_performer(performer_uuid,
                                    record["Performer Identifier"],
                                    record["Performer Org"],
                                    record["Performer Address"],
                                    record["Performer City"],
                                    record["Performer District"],
                                    record["Performer Postcode"])
        requester = build_requester(requester_uuid,
                                    record["Requester Identifier"],
                                    record["Requester Org"],
                                    record["Requester Address"],
                                    record["Requester City"],
                                    record["Requester District"],
                                    record["Requester Postcode"])
        #Loop the others to make the request
        for profile_part in profile_records[profile]:
            request_uuid = uuid.uuid4()
            observation_uuid = uuid.uuid4()
            request_ids.append(request_uuid)
            observation_ids.append(observation_uuid)
            request = build_request(request_uuid,uuid.uuid4(),"active",
                                    profile_part["Code"],
                                    profile_part["Display"],
                                    patient_uuid,
                                    "%s,%s" % (record["Family Name"],record["Given Name"]),
                                    "2019-06-04",
                                    requester_uuid,
                                    record["Requester Org"],
                                    performer_uuid,
                                    record["Performer Org"],
                                    profile_part["DisplayCode"],
                                    requisition_id)
            requests.append(request)
            if record["SpecimenGroup"] not in specimen_groups:
                specimen_uuid = uuid.uuid4()
                specimen = build_specimen(specimen_uuid, uuid.uuid4(), 
                                            record["SpecimenStatus"], 
                                            record["SpecimenCode"],
                                            record["SpecimenDisplay"], 
                                            patient_uuid, 
                                            "%s,%s" % (record["Family Name"].upper(),record["Given Name"]), 
                                            record["SpecimenReceivedTime"],
                                            record["SpecimenCollectedTime"], 
                                            record["SpecimenQuantityValue"],
                                            record["SpecimenQuantityUnit"])
                specimen_groups.append(record["SpecimenGroup"])
                specimen_ids.append(specimen_uuid)
                specimens.append(specimen)

            observation_values = build_values_dictionary(record)

            observation = build_observation(observation_uuid, uuid.uuid4(),
                                        record["ObservationStatus"],
                                        record["ObservationCode"], 
                                        record["ObservationDisplay"],
                                        patient_uuid, 
                                        "%s,%s" % (record["Family Name"].upper(),record["Given Name"]), 
                                        record["ObservationEffectiveDatetime"],
                                        performer_uuid,
                                        record["Requester Org"], 
                                        specimen_uuid, 
                                        observation_values)
            observations.append(observation)

        diagnostic_report = build_diagnostic_report(diagnostic_report_uuid,
                                request_ids[0],
                                record["ReportStatus"],
                                patient_uuid,
                                "%s,%s" % (record["Family Name"].upper(),record["Given Name"]),
                                record["Issuedon"],
                                performer_uuid,
                                record["Requester Org"],
                                specimen_ids,observation_ids)

        header = build_message_header(message_header_uuid,performer_uuid,requester_uuid,
                                "2019-03-14T10:10:16+00:00","NOROT003",request_ids)
        
        bundle = build_bundle(bundle_uuid,uuid.uuid4(),
                            header,message_header_uuid,
                            requester,requester_uuid,
                            performer,performer_uuid,
                            patient,patient_uuid,
                            requests,request_ids,
                            diagnostic_report_uuid, diagnostic_report,
                            specimens,specimen_ids,observations,observation_ids) 
        print(bundle)
        output_name = "../examples/reports/%s_report.xml" % (record["Report"].replace(" ","_"))
        f = open(output_name,"w",encoding="utf-8")
        f.write(bundle)       
        f.close()

def build():
    profiles = {}
    for record in load_test_data():
        print(record)
        if record["GroupId"].strip()=="":
            build_simple_report(record)
        else:
            #Build a list of the data we need for each profile test
            profileId = record["GroupId"].strip()
            if profileId in profiles:
                profiles[profileId].append(record)
            else:
                profiles[profileId] = [record,]
    build_profile_reports(profiles)

if __name__=="__main__":
    build()
"""
Make data file match test cases
Validate
Make README file
Commit
Merge to main
Make public
"""