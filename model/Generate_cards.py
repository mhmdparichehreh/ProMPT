from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Spacer
from reportlab.lib.units import inch
import os

# Structured data with the specific output you provided
impact_cards = [
    {
        "title": "AI-Assisted Medical Diagnostics",
        "use": "Enables remote diagnosis and detection of health issues in areas with overwhelmed or damaged healthcare systems.",
        "benefits": [
            "Expands access to care where medical professionals are scarce.",
            "Speeds up detection of post-conflict diseases such as cholera or birth complications."
        ],
        "risks_mitigations": [
            ("Misdiagnosis", "lack of current clinical data for war injuries and disease patterns may lead to inaccurate AI outputs + Human clinical sign-off on all AI diagnoses."),
            ("Tech Dependence", "power and connectivity disruptions can halt AI-based diagnosis, leaving patients untreated + Training programs and contingency plans for manual procedures."),
            ("Unauthorized Data Access", "health data could be exploited to discriminate against certain groups + Isolated servers and encryption for medical databases.")
        ]
    },
    {
        "title": "Autonomous Vehicles",
        "use": "Unmanned ground or aerial vehicles deliver aid where roads are unsafe or inaccessible.",
        "benefits": [
            "Ensures consistent aid delivery despite road insecurity or destroyed infrastructure.",
            "Reduces risk to human drivers in hostile environments."
        ],
        "risks_mitigations": [
            ("Electronic Interference", "GPS jamming/spoofing may misdirect vehicles + Anti-jamming measures and safe-mode fallback protocols."),
            ("Route Failures", "vehicles may be stranded due to damaged infrastructure + Up-to-date post-war maps and redundant sensors (LiDAR, radar)."),
            ("Military Exploitation", "platforms could be hacked or repurposed for surveillance or attacks + International norms separating civilian vs. military use.")
        ]
    },
    {
        "title": "Computer Vision (Object Detection & Segmentation)",
        "use": "Analyzes drone and satellite imagery to assess infrastructure damage and prioritize reconstruction.",
        "benefits": [
            "Accelerates needs assessments and damage mapping in inaccessible areas.",
            "Supports efficient planning for rebuilding and aid allocation."
        ],
        "risks_mitigations": [
            ("Invasive Surveillance", "civilian movement may be unintentionally tracked + Legal/geographic restrictions on camera and drone use in civilian zones."),
            ("Model Bias", "biased training data may skew rebuilding priorities + Diverse datasets and continuous bias-mitigation processes.")
        ]
    },
    {
        "title": "Data Analytics & Forecasting",
        "use": "Forecasts displacement, food insecurity, and other critical trends for humanitarian planning.",
        "benefits": [
            "Improves targeting of aid to the most affected populations.",
            "Enables anticipatory response to crises before they escalate."
        ],
        "risks_mitigations": [
            ("Exclusion of Groups", "marginalized communities may be underrepresented in data + Independent audits and transparent methodologies."),
            ("Faulty Predictions", "outdated data may produce incorrect forecasts + Continuous dataset updates and real-world validation."),
            ("Skewed Policymaking", "results may be politicized to justify biased decisions + Stakeholder involvement from local communities.")
        ]
    },
    {
        "title": "Natural Language Processing (NLP)",
        "use": "Analyzes media and reports to monitor peace agreement violations and community grievances.",
        "benefits": [
            "Identifies early warning signs of renewed conflict.",
            "Enhances transparency and responsiveness of peacekeeping efforts."
        ],
        "risks_mitigations": [
            ("Automated Propaganda", "systems could be misused to generate divisive content + Content-authenticity filters and AI-generated text detection."),
            ("Privacy Violations", "data scraping may expose sensitive information + Data-minimization policies and human oversight."),
            ("Sentiment Manipulation", "data on grievances could be exploited for surveillance + Algorithmic transparency and independent model audits.")
        ]
    },
    {
        "title": "Recommendation Systems",
        "use": "Connects displaced individuals to relevant support services such as shelter or legal aid.",
        "benefits": [
            "Streamlines access to life-saving assistance in unfamiliar environments.",
            "Supports reintegration and self-sufficiency of displaced populations."
        ],
        "risks_mitigations": [
            ("Filter Bubbles", "users may only receive limited service information + Explainable recommendations that show rationale."),
            ("Predatory Offers", "systems could be exploited to push scams or trafficking + Equity policies to prevent predatory targeting.")
        ]
    },
    {
        "title": "Speech Recognition & Voice Synthesis",
        "use": "Disseminates multilingual safety and aid information through voice-based systems.",
        "benefits": [
            "Reaches populations with low literacy or language barriers.",
            "Facilitates rapid dissemination of updates during emergencies."
        ],
        "risks_mitigations": [
            ("Critical Dependence", "failure during crises could halt communication + Redundant communication paths and manual fallback procedures."),
            ("Deep-voice Spoofing", "fake voices may spread panic or false orders + Digital watermarking and cryptographic signing of synthesized voice to verify origin."),
            ("Eavesdropping & Profiling", "intercepted voice data could be used for political repression + End-to-end encryption and strong authentication for voice channels.")
        ]
    }
]

output_dir = "AI_Impact_Cards"
os.makedirs(output_dir, exist_ok=True)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Heading', fontSize=14, leading=16, spaceAfter=10, spaceBefore=20, leftIndent=0, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='Body', fontSize=11, leading=14, spaceAfter=8, leftIndent=10, rightIndent=10))
styles.add(ParagraphStyle(name='CustomBullet', fontSize=11, leading=14, leftIndent=20, CustomBulletIndent=10))

# Create PDFs for each impact card
for card in impact_cards:
    filename = os.path.join(output_dir, f"{card['title'].replace(' ', '_')}.pdf")
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    frame = Frame(50, 50, width - 100, height - 100, showBoundary=0)

    story = []
    story.append(Paragraph(f"<b>{card['title']}</b>", styles['Heading']))
    story.append(Paragraph(f"<b>*Use*:</b> {card['use']}", styles['Body']))

    story.append(Paragraph("<b>*Benefits*:</b>", styles['Body']))
    for benefit in card["benefits"]:
        story.append(Paragraph(f"• {benefit}", styles['CustomBullet']))

    story.append(Paragraph("<b>*Risks and Mitigations*:</b>", styles['Body']))
    for risk, description in card["risks_mitigations"]:
        story.append(Paragraph(f"• <b>{risk}</b>: {description}", styles['CustomBullet']))

    frame.addFromList(story, c)
    c.save()

print(f"PDFs exported to: {output_dir}")
