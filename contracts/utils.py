from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_contract_pdf(contract):

    file_name = f"contract_{contract.id}.pdf"
    file_path = f"media/contracts/{file_name}"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(f"Contract #{contract.id}", styles["Title"]))
    content.append(Paragraph(f"Tenant: {contract.booking.tenant.username}", styles["Normal"]))
    content.append(Paragraph(f"Property: {contract.booking.property.title}", styles["Normal"]))
    content.append(Paragraph(f"Rent: {contract.rent_amount}", styles["Normal"]))

    doc.build(content)

    contract.contract_file = f"contracts/{file_name}"
    contract.save()
    
    