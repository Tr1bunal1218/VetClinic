import numpy as np
import tensorflow.lite as tflite
from flask import Flask, request, jsonify, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import io
import os
from lxml import etree
from datetime import datetime

app = Flask(__name__)

CDA_STORAGE_DIR = "medical_records"
if not os.path.exists(CDA_STORAGE_DIR):
    os.makedirs(CDA_STORAGE_DIR)

interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

BREED_NORMS = {
    "labrador": {"blood_glucose": (70, 120), "xray_density": (0.5, 1.5)},
    "poodle": {"blood_glucose": (65, 115), "xray_density": (0.4, 1.4)}
}

BREED_ENCODER = {"labrador": 0, "poodle": 1}


def analyze_result(test_type, value, breed):
    breed_encoded = BREED_ENCODER.get(breed.lower(), 0)
    input_data = np.array([[value, breed_encoded]], dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    prediction = interpreter.get_tensor(output_details[0]['index'])[0][0]

    norm_range = BREED_NORMS.get(breed, {}).get(test_type, (0, 0))
    status = "normal" if norm_range[0] <= value <= norm_range[1] else "abnormal"
    return {"prediction": float(prediction), "status": status, "norm_range": norm_range}


def create_cda_document(pet_id, test_type, value, date, breed):
    NS = "urn:hl7-org:v3"
    root = etree.Element("{%s}ClinicalDocument" % NS, nsmap={None: NS})

    doc_id = etree.SubElement(root, "id", root="2.16.840.1.113883.19.5")
    effective_time = etree.SubElement(root, "effectiveTime", value=date.replace("-", ""))

    custodian = etree.SubElement(root, "custodian")
    assigned_custodian = etree.SubElement(custodian, "assignedCustodian")
    organization = etree.SubElement(assigned_custodian, "representedCustodianOrganization")
    org_name = etree.SubElement(organization, "name")
    org_name.text = "PetLab Inc."

    patient_role = etree.SubElement(root, "patientRole")
    patient_id = etree.SubElement(patient_role, "id", root="2.16.840.1.113883.19.5", extension=str(pet_id))
    patient = etree.SubElement(patient_role, "patient")
    patient_name = etree.SubElement(patient, "name")
    patient_name.text = f"Pet {pet_id}"
    patient_breed = etree.SubElement(patient, "breed")
    patient_breed.text = breed

    component = etree.SubElement(root, "component")
    structured_body = etree.SubElement(component, "structuredBody")
    body_component = etree.SubElement(structured_body, "component")
    section = etree.SubElement(body_component, "section")
    entry = etree.SubElement(section, "entry")
    observation = etree.SubElement(entry, "observation", classCode="OBS", moodCode="EVN")

    code = etree.SubElement(observation, "code", code=test_type.upper(),
                            displayName=test_type.replace("_", " ").title())
    value_elem = etree.SubElement(observation, "value",
                                  attrib={"{http://www.w3.org/2001/XMLSchema-instance}type": "PQ", "value": str(value),
                                          "unit": "mg/dL" if test_type == "blood_glucose" else "g/cm³"})
    obs_time = etree.SubElement(observation, "effectiveTime", value=date.replace("-", ""))

    analysis = analyze_result(test_type, value, breed)
    status = analysis["status"]
    interpretation = etree.SubElement(observation, "interpretationCode", code=status.upper())

    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")


@app.route('/store_result', methods=['POST'])
def store_result():
    data = request.json
    pet_id = data['pet_id']
    test_type = data['test_type']
    value = data['value']
    date = data['date']
    breed = data['breed']

    cda_xml = create_cda_document(pet_id, test_type, value, date, breed)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"result_{pet_id}_{timestamp}.xml"
    filepath = os.path.join(CDA_STORAGE_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(cda_xml)

    analysis = analyze_result(test_type, value, breed)
    return jsonify({"message": "Result stored in Medical Records", "analysis": analysis})


@app.route('/generate_report/<int:pet_id>', methods=['GET'])
def generate_report(pet_id):
    results = []
    breed = None
    for filename in os.listdir(CDA_STORAGE_DIR):
        if filename.startswith("result_"):
            filepath = os.path.join(CDA_STORAGE_DIR, filename)
            with open(filepath, "rb") as f:
                try:
                    tree = etree.parse(f)
                    root = tree.getroot()
                    current_pet_id = \
                    root.xpath("//v3:patientRole/v3:id/@extension", namespaces={"v3": "urn:hl7-org:v3"})[0]
                    if int(current_pet_id) == pet_id:
                        test_type = \
                        root.xpath("//v3:observation/v3:code/@displayName", namespaces={"v3": "urn:hl7-org:v3"})[0]
                        value = float(
                            root.xpath("//v3:observation/v3:value/@value", namespaces={"v3": "urn:hl7-org:v3"})[0])
                        date = \
                        root.xpath("//v3:observation/v3:effectiveTime/@value", namespaces={"v3": "urn:hl7-org:v3"})[0]
                        date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
                        unit = root.xpath("//v3:observation/v3:value/@unit", namespaces={"v3": "urn:hl7-org:v3"})[0]
                        status = \
                        root.xpath("//v3:observation/v3:interpretationCode/@code", namespaces={"v3": "urn:hl7-org:v3"})[
                            0]
                        if breed is None:
                            breed = root.xpath("//v3:patientRole/v3:patient/v3:breed/text()",
                                               namespaces={"v3": "urn:hl7-org:v3"})[0]
                        results.append((test_type, value, date, unit, status))
                except Exception as e:
                    print(f"Error parsing {filename}: {e}")
                    continue

    if not results:
        return jsonify({"error": "No data found for this Pet ID in Medical Records"}), 404

    print(f"Results for pet_id {pet_id}: {results}")  # Логирование для отладки
    results.sort(key=lambda x: x[2])

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y_position = height - 70  # Начинаем ниже заголовка

    # Header with updated style
    c.setFillColor(colors.navy)
    c.rect(0, height - 70, width, 70, fill=True, stroke=False)
    c.setFont("Times-Roman", 20)  # Используем Times-Roman вместо Helvetica
    c.setFillColor(colors.gold)
    c.drawCentredString(width / 2, height - 50, f"Lab Results Report for Pet ID: {pet_id}")

    # Add a watermark
    c.setFont("Times-Roman", 40)
    c.setFillAlpha(0.2)
    c.setFillColor(colors.grey)
    c.rotate(45)
    c.drawCentredString(width / 2, height / 4, "PetLab Inc.")
    c.rotate(-45)
    c.setFillAlpha(1.0)

    y_position = height - 150

    # Chart with updated style
    c.setFont("Times-Roman", 14)
    c.setFillColor(colors.black)
    c.drawString(100, y_position, f"Trend Analysis: {results[0][0]}")
    y_position -= 40

    dates = [r[2] for r in results]
    values = [r[1] for r in results]

    drawing = Drawing(400, 200)
    lc = HorizontalLineChart()
    lc.x = 50
    lc.y = 50
    lc.height = 125
    lc.width = 300
    lc.data = [values]
    lc.categoryAxis.categoryNames = dates if len(dates) <= 3 else [dates[0], dates[len(dates) // 2], dates[-1]]
    lc.categoryAxis.labels.angle = 45
    lc.categoryAxis.labels.boxAnchor = 'ne'
    lc.valueAxis.valueMin = min(values) * 0.9
    lc.valueAxis.valueMax = max(values) * 1.1
    lc.lines[0].strokeColor = colors.forestgreen
    lc.lines[0].strokeWidth = 2
    lc.fillColor = colors.mintcream
    lc.valueAxis.strokeColor = colors.darkgrey
    lc.categoryAxis.strokeColor = colors.darkgrey
    drawing.add(lc)
    drawing.drawOn(c, 100, y_position - 200)
    y_position -= 250

    # New table: Comparison with breed norms
    c.setFont("Times-Roman", 12)
    c.drawString(100, y_position, "Comparison with Breed Norms")
    y_position -= 40

    norm_range = BREED_NORMS.get(breed.lower(), {}).get(results[0][0].replace(" ", "_").lower(), (0, 0))
    norm_comparison_data = [
        ["Date", "Value", "Unit", "Status", "Normal Range", "Within Range"],
    ]
    for test_type, value, date, unit, status in results:
        within_range = "Yes" if norm_range[0] <= value <= norm_range[1] else "No"
        norm_comparison_data.append(
            [date, f"{value:.2f}", unit, status.title(), f"{norm_range[0]} - {norm_range[1]}", within_range])

    norm_comparison_table = Table(norm_comparison_data, colWidths=[80, 60, 60, 60, 80, 70])
    norm_comparison_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.teal),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.palegreen),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.darkgrey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.palegreen]),
    ]))
    table_width, table_height = norm_comparison_table.wrap(0, 0)
    if y_position - table_height < 50:  # Проверка на выход за пределы страницы
        c.showPage()
        y_position = height - 50
    norm_comparison_table.drawOn(c, 100, y_position - table_height)

    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"report_{pet_id}.pdf", mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)