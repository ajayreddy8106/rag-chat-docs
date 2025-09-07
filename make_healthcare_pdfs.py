# make_healthcare_pdfs.py
# Creates 4 healthcare PDFs into the docs/ folder.
# Requires: pip install reportlab

import os
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from textwrap import wrap

DOCS_DIR = "docs"
os.makedirs(DOCS_DIR, exist_ok=True)

docs = {
    "clinic_overview.pdf": """
ACME Health Clinic — Overview
--------------------------------
Mission: Provide affordable, high-quality primary care and preventive services.

Services:
• Primary care visits
• Preventive screenings (blood pressure, diabetes, cholesterol)
• Vaccinations (influenza, Tdap, MMR, COVID-19)
• Women’s health (Pap smear, prenatal counseling)
• Behavioral health (short-term counseling, referrals)
• Telehealth (video visits Mon–Fri)

Hours & Locations:
• Downtown Campus: Mon–Fri 8:00 AM–6:00 PM, Sat 9:00 AM–1:00 PM
• Westside Campus: Mon–Fri 9:00 AM–5:00 PM
• Closed Sundays and federal holidays

Contact:
• Phone: (555) 010-1000
• Email: care@acmehealth.org
• Emergencies: Dial 911
""",

    "patient_faq.pdf": """
Patient FAQ — ACME Health Clinic
--------------------------------
Q: How do I book an appointment?
A: Call (555) 010-1000 or use the Patient Portal. Same-day slots open at 7:30 AM.

Q: Do you accept walk-ins?
A: Limited walk-ins for urgent symptoms; otherwise please schedule.

Q: What should I bring?
A: Photo ID, insurance card (if any), current medications list, and prior records if available.

Q: Do you offer telehealth?
A: Yes, Mon–Fri during business hours. Stable internet and a camera-enabled device required.

Q: What if I need a prescription refill?
A: Request via Patient Portal or call. Allow 2 business days for processing.

Q: How do I access my lab results?
A: Results post to the Portal within 1–3 business days. Your clinician will message you.

Q: What if I can’t afford care?
A: We offer sliding-scale fees, payment plans, and help applying for assistance programs.
""",

    "insurance_billing_guide.pdf": """
Insurance & Billing Guide — ACME Health Clinic
----------------------------------------------
Insurance Plans Accepted:
• Most major commercial plans
• Medicaid and Medicare
• Select marketplace plans (see website for current list)

Before Your Visit:
• Verify eligibility and co-pay with your insurer
• Add your insurance to the Patient Portal
• Bring a photo ID and insurance card

At Check-In:
• Co-pay due at time of service
• Inform us of changes in address, phone, or coverage

After Your Visit (Billing):
• You’ll receive an Explanation of Benefits (EOB) from your insurer
• If a balance remains, ACME Health will send a statement
• Payment options: online portal, phone, in person, or by mail
• Questions? billing@acmehealth.org or (555) 010-2000

No Insurance?
• Sliding-scale pricing available
• Upfront estimates on request
""",

    "hipaa_privacy_summary.pdf": """
HIPAA Privacy Summary — ACME Health Clinic
------------------------------------------
Your Rights:
• Access your medical record
• Request corrections
• Receive a list of disclosures
• Request confidential communications
• File a complaint without retaliation

Our Responsibilities:
• Maintain the privacy and security of your PHI (Protected Health Information)
• Inform you if a breach compromises your information
• Follow the duties and privacy practices described here

Uses & Disclosures (Examples):
• Treatment: sharing PHI with other providers involved in your care
• Payment: submitting claims to your insurer
• Operations: quality assessment, training, audits

Contact:
• Privacy Officer: privacy@acmehealth.org
• Address: 100 Health Way, Metro City, ST 12345
"""
}

def write_pdf(path, text, max_width_chars=90, leading=14):
    c = canvas.Canvas(path, pagesize=LETTER)
    width, height = LETTER
    x_margin = 0.75 * inch
    y = height - 0.75 * inch
    # Break into lines and wrap long lines
    for paragraph in text.strip().split("\n"):
        lines = wrap(paragraph, width=max_width_chars) if paragraph.strip() else [""]
        for line in lines:
            if y < 0.75 * inch:
                c.showPage()
                y = height - 0.75 * inch
            c.drawString(x_margin, y, line)
            y -= leading
        # extra spacing between paragraphs
        y -= 4
    c.save()

def main():
    for filename, content in docs.items():
        out_path = os.path.join(DOCS_DIR, filename)
        write_pdf(out_path, content)
        print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
