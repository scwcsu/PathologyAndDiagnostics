#!/bin/bash

wget --header="Accept: application/fhir+xml" https://fhir.hl7.org.uk/STU3/StructureDefinition/CareConnect-DiagnosticReport-1 -O ../structures/CareConnect-DiagnosticReport-1.xml
wget --header="Accept: application/fhir+xml" https://fhir.hl7.org.uk/STU3/StructureDefinition/CareConnect-ProcedureRequest-1 -O ../structures/CareConnect-ProcedureRequest-1.xml
wget --header="Accept: application/fhir+xml" https://fhir.hl7.org.uk/STU3/StructureDefinition/CareConnect-Specimen-1 -O ../structures/CareConnect-Specimen-1.xml
wget --header="Accept: application/fhir+xml" https://fhir.hl7.org.uk/STU3/StructureDefinition/CareConnect-Observation-1 -O ../structures/CareConnect-Observation-1.xml
wget --header="Accept: application/fhir+xml" https://fhir.nhs.uk/STU3/StructureDefinition/CareConnect-ITK-Header-Organization-1 -O ../structures/CareConnect-ITK-Header-Organization-1.xml
wget --header="Accept: application/fhir+xml" https://fhir.nhs.uk/STU3/StructureDefinition/CareConnect-ITK-Header-Practitioner-1 -O ../structures/CareConnect-ITK-Header-Practitioner-1.xml
wget --header="Accept: application/fhir+xml" https://fhir.nhs.uk/STU3/ValueSet/CareConnect-ObservationInterpretation-1 -O ../structures/CareConnect-ObservationInterpretation-1.xml

wget --header="Accept: application/fhir+xml" https://fhir.nhs.uk/STU3/StructureDefinition/Extension-ITK-MessageHandling-2 -O ../structures/ITK-MessageHandling-2.xml
wget --header="Accept: application/fhir+xml" https://fhir.nhs.uk/STU3/StructureDefinition/ITK-Message-Bundle-1 -O ../structures/ITK-Message-Bundle-1.xml
wget --header="Accept: application/fhir+xml" https://fhir.nhs.uk/STU3/StructureDefinition/ITK-Payload-Bundle-1 -O ../structures/ITK-Payload-Bundle-1.xml
wget --header="Accept: application/fhir+xml" https://fhir.nhs.uk/STU3/StructureDefinition/ITK-Response-OperationOutcome-1 -O ../structures/ITK-Response-OperationOutcome-1.xml

