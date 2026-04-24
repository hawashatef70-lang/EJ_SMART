import os
from django.conf import settings
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_contract_pdf(contract):
    """
    Generate a PDF file for a contract and save it to MEDIA_ROOT.
    Returns the file URL.
    """

    # =========================
    # 📁 Ensure directory exists
    # =========================
    contracts_dir = os.path.join(settings.MEDIA_ROOT, "contracts")
    os.makedirs(contracts_dir, exist_ok=True)

    file_name = f"contract_{contract.id}.pdf"
    file_path = os.path.join(contracts_dir, file_name)

    # =========================
    # 📄 PDF setup
    # =========================
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    # =========================
    # 📄 CONTRACT CONTENT
    # =========================
    content.append(Paragraph(f"Contract #{contract.id}", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(
        f"Tenant: {contract.booking.tenant.username}",
        styles["Normal"]
    ))

    content.append(Paragraph(
        f"Owner: {contract.booking.property.owner.username}",
        styles["Normal"]
    ))

    content.append(Paragraph(
        f"Property: {contract.booking.property.title}",
        styles["Normal"]
    ))

    content.append(Paragraph(
        f"Rent Amount: {contract.rent_amount}",
        styles["Normal"]
    ))

    content.append(Paragraph(
        f"Deposit: {contract.deposit}",
        styles["Normal"]
    ))

    content.append(Paragraph(
        f"Start Date: {contract.start_date}",
        styles["Normal"]
    ))

    content.append(Paragraph(
        f"End Date: {contract.end_date}",
        styles["Normal"]
    ))

    # =========================
    # 📦 BUILD PDF
    # =========================
    doc.build(content)

    # =========================
    # 💾 SAVE TO MODEL
    # =========================
    contract.contract_file.name = f"contracts/{file_name}"
    contract.save(update_fields=["contract_file"])

    return contract.contract_file.url
    