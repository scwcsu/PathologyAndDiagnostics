import jinja2
import csv
import uuid

#Load all the templates
templateLoader = jinja2.FileSystemLoader(searchpath="../templates")
templateEnv = jinja2.Environment(loader=templateLoader)
patient_template = templateEnv.get_template("patient.xml.jinja")
requester_template = templateEnv.get_template("requester.xml.jinja")
performer_template = templateEnv.get_template("performer.xml.jinja")
request_template = templateEnv.get_template("procedurerequest.xml.jinja")
message_header_template = templateEnv.get_template("messageheader.xml.jinja")
bundle_template = templateEnv.get_template("requestbundle.xml.jinja")
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

def load_test_data(data_csv="../templates/RequestsTestDataSetup.csv"):
    with open(data_csv,encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel')
        for row in reader:
            yield row

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
            authored_on,requester_uuid,requester_display,performer_uuid,performer_display,request_utl_display_code):

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
                                        request_utl_display_code=request_utl_display_code)
    return request

def build_message_header(uuid,receiver_uuid,sender_uuid,timestamp,endpoint,focus_uuid):
    header = message_header_template.render(message_header_uuid=uuid,
                                            receiver_uuid=receiver_uuid,
                                            sender_uuid=sender_uuid,
                                            timestamp=timestamp,
                                            endpoint=endpoint,
                                            focus_uuid=focus_uuid)
    return header

def build_bundle(uuid,identifier,header,header_uuid,requester,requester_uuid,
                    performer,performer_uuid,patient,patient_uuid,procedure,procedure_uuid):
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
                                    procedure_request_resource=procedure,
                                    request_uuid=procedure_uuid)
    return bundle

def build():
    for record in load_test_data():
        patient_uuid = uuid.uuid4()
        requester_uuid = uuid.uuid4()
        performer_uuid = uuid.uuid4()
        request_uuid = uuid.uuid4()
        message_header_uuid = uuid.uuid4()
        bundle_uuid = uuid.uuid4()
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
        header = build_message_header(message_header_uuid,performer_uuid,requester_uuid,
                                "2019-03-14T10:10:16+00:00","NOROT003",request_uuid)
        
        bundle = build_bundle(bundle_uuid,uuid.uuid4(),
                            header,message_header_uuid,
                            requester,requester_uuid,
                            performer,performer_uuid,
                            patient,patient_uuid,
                            request,request_uuid)
        print(bundle)
        output_name = "../examples/requests/%s_request.xml" % (record["Request"].replace(" ","_"))
        f = open(output_name,"w",encoding="utf-8")
        f.write(bundle)       
        f.close()

if __name__=="__main__":
    build()