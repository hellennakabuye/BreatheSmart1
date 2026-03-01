import bcrypt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from io import BytesIO

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def calculate_risk(data):
    score = 0
    if data["wheezing"]: score += 2
    if data["chest"]: score += 2
    if data["night_symptoms"]: score += 2
    if data["inhaler_used"]: score += 2
    if data["dust_exposure"]: score += 1
    if data["smoke_exposure"]: score += 1
    if data["cold_weather"]: score += 1
    if data["runny_nose"] or data["itchy_eyes"]: score += 1
    if data["cough"]: score += 1
    if data["chest"]: score += 1
    if data["congestion"]: score += 1
    if data["others"]: score += 1
    return score
'''
def generate_pdf_report(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Kampala Respiratory Monthly Report", styles["Heading1"]))
    elements.append(Spacer(1, 12))

    total_users = data["user_id"].nunique()
    avg_risk = round(data["risk_score"].mean(), 2)

    summary = [
        ["Metric", "Value"],
        ["Total Active Users", total_users],
        ["Average Risk Score", avg_risk],
    ]

    table = Table(summary)
    table.setStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
    ])

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer
'''
