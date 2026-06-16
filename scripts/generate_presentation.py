from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "presentation"
PDF_PATH = OUT_DIR / "last_mile_logistics_auditor_presentation.pdf"

AUTHOR_NAME = "Irigenera Alliance"
STUDENT_AFFILIATION = "AIMS Rwanda"
PROGRAM_CONTEXT = "AmaliTech Rwanda Exam Task"

SLIDE_SIZE = landscape((13.333 * inch, 7.5 * inch))
W, H = SLIDE_SIZE

BLUE = colors.HexColor("#2563eb")
NAVY = colors.HexColor("#111827")
MUTED = colors.HexColor("#64748b")
LINE = colors.HexColor("#d9e2ec")
GREEN = colors.HexColor("#15803d")
AMBER = colors.HexColor("#f59e0b")
RED = colors.HexColor("#dc2626")
TEAL = colors.HexColor("#0f766e")
PANEL = colors.white
BG = colors.HexColor("#f3f6fa")


def draw_bg(c, title, subtitle="", page=1):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(PANEL)
    c.roundRect(0.42 * inch, 0.38 * inch, W - 0.84 * inch, H - 0.76 * inch, 8, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.roundRect(0.42 * inch, 0.38 * inch, W - 0.84 * inch, H - 0.76 * inch, 8, fill=0, stroke=1)
    c.setFillColor(BLUE)
    c.rect(0.42 * inch, H - 0.82 * inch, W - 0.84 * inch, 0.08 * inch, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(0.75 * inch, H - 1.18 * inch, title)
    if subtitle:
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 10)
        c.drawString(0.75 * inch, H - 1.42 * inch, subtitle)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawRightString(W - 0.75 * inch, 0.58 * inch, f"{AUTHOR_NAME} | {PROGRAM_CONTEXT} | {page}")


def textbox(c, x, y, width, lines, size=12, color=NAVY, leading=16, bullet=False):
    c.setFillColor(color)
    c.setFont("Helvetica", size)
    current_y = y
    for line in lines:
        if bullet:
            c.setFillColor(BLUE)
            c.circle(x + 0.05 * inch, current_y + 0.04 * inch, 2.1, fill=1, stroke=0)
            c.setFillColor(color)
            c.drawString(x + 0.18 * inch, current_y, line)
        else:
            c.drawString(x, current_y, line)
        current_y -= leading


def kpi(c, x, y, w, h, label, value, note, color):
    c.setFillColor(colors.white)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 7, fill=1, stroke=1)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 0.16 * inch, y + h - 0.26 * inch, label.upper())
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(x + 0.16 * inch, y + 0.42 * inch, value)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(x + 0.16 * inch, y + 0.2 * inch, note)


def panel(c, x, y, w, h, title, body_lines=None):
    c.setFillColor(colors.white)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 7, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 0.18 * inch, y + h - 0.32 * inch, title)
    if body_lines:
        textbox(c, x + 0.18 * inch, y + h - 0.66 * inch, w - 0.36 * inch, body_lines, size=10, leading=15, bullet=True)


def image_fit(c, path, x, y, w, h):
    img = Image.open(path)
    iw, ih = img.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(str(path), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, mask="auto")


def title_slide(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(0, H - 0.18 * inch, W, 0.18 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 38)
    c.drawString(0.82 * inch, 4.55 * inch, "Last Mile Logistics Auditor")
    c.setFont("Helvetica", 15)
    c.setFillColor(colors.HexColor("#cbd5e1"))
    c.drawString(0.86 * inch, 4.12 * inch, "Delivery promise accuracy and customer sentiment audit")
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(0.86 * inch, 3.64 * inch, AUTHOR_NAME)
    c.setFillColor(colors.HexColor("#cbd5e1"))
    c.setFont("Helvetica", 12)
    c.drawString(0.86 * inch, 3.34 * inch, f"{STUDENT_AFFILIATION} | {PROGRAM_CONTEXT}")
    c.setFillColor(colors.white)
    kpi(c, 0.86 * inch, 2.35 * inch, 2.4 * inch, 1.0 * inch, "Delivered Orders", "96,476", "analysis base", colors.white)
    kpi(c, 3.48 * inch, 2.35 * inch, 2.4 * inch, 1.0 * inch, "Late Rate", "8.1%", "late or super late", colors.white)
    kpi(c, 6.1 * inch, 2.35 * inch, 2.4 * inch, 1.0 * inch, "Worst State", "AL", "23.9% late", colors.white)
    c.setFillColor(colors.HexColor("#cbd5e1"))
    c.setFont("Helvetica", 10)
    c.drawString(0.86 * inch, 0.75 * inch, "Prepared for Veridi Logistics | Olist Brazilian E-Commerce Dataset")


def build_pdf():
    OUT_DIR.mkdir(exist_ok=True)
    c = canvas.Canvas(str(PDF_PATH), pagesize=SLIDE_SIZE)
    c.setTitle("Last Mile Logistics Auditor")
    c.setAuthor(f"{AUTHOR_NAME} | {STUDENT_AFFILIATION}")
    c.setSubject(PROGRAM_CONTEXT)

    title_slide(c)
    c.showPage()

    draw_bg(c, "Executive Summary", "Answering whether delivery failures are regional or nationwide", 2)
    kpi(c, 0.8 * inch, 4.95 * inch, 2.75 * inch, 1.0 * inch, "Late Rate", "8.1%", "7,827 late or super late", AMBER)
    kpi(c, 3.8 * inch, 4.95 * inch, 2.75 * inch, 1.0 * inch, "Worst Region", "AL", "23.9% late rate", RED)
    kpi(c, 6.8 * inch, 4.95 * inch, 2.75 * inch, 1.0 * inch, "Review Damage", "-2.51", "on time vs super late", RED)
    kpi(c, 9.8 * inch, 4.95 * inch, 2.75 * inch, 1.0 * inch, "Category Risk", "Audio", "12.9% late rate", TEAL)
    panel(c, 0.8 * inch, 1.55 * inch, 5.7 * inch, 2.75 * inch, "Main Finding", [
        "Delivery failures are concentrated in specific states.",
        "AL, MA, PI, CE, and SE have late rates well above the national average.",
        "Super-late orders are associated with a steep drop in customer review score.",
    ])
    panel(c, 6.85 * inch, 1.55 * inch, 5.7 * inch, 2.75 * inch, "Business Meaning", [
        "The CEO's over-promising concern is supported by the data.",
        "Regional promise recalibration should be prioritized.",
        "Product-category risk gives an extra operational repair path.",
    ])
    c.showPage()

    draw_bg(c, "Data Model and Cleaning", "Schema builder acceptance criteria", 3)
    panel(c, 0.8 * inch, 3.95 * inch, 3.8 * inch, 1.55 * inch, "Core Joins", [
        "Orders to customers on customer_id.",
        "Aggregated reviews to orders on order_id.",
        "Products and translations added for category analysis.",
    ])
    panel(c, 4.9 * inch, 3.95 * inch, 3.8 * inch, 1.55 * inch, "Duplicate Control", [
        "Reviews are grouped to one row per order before joining.",
        "Row counts and unique order IDs are checked after joins.",
    ])
    panel(c, 9.0 * inch, 3.95 * inch, 3.55 * inch, 1.55 * inch, "Delay Logic", [
        "Days_Difference = estimated date - actual date.",
        "Undelivered orders are flagged separately.",
    ])
    panel(c, 1.2 * inch, 1.5 * inch, 10.9 * inch, 1.6 * inch, "Delivery Status Rules", [
        "On Time: delivered on or before the estimated date.",
        "Late: delivered 1 to 5 days after the estimated date.",
        "Super Late: delivered more than 5 days after the estimated date.",
    ])
    c.showPage()

    draw_bg(c, "National Delivery Performance", "Delivery promise accuracy overview", 4)
    kpi(c, 0.8 * inch, 5.05 * inch, 2.2 * inch, 0.9 * inch, "Delivered", "96,476", "orders", NAVY)
    kpi(c, 3.25 * inch, 5.05 * inch, 2.2 * inch, 0.9 * inch, "On Time", "91.9%", "88,649 orders", GREEN)
    kpi(c, 5.7 * inch, 5.05 * inch, 2.2 * inch, 0.9 * inch, "Late", "3.7%", "3,615 orders", AMBER)
    kpi(c, 8.15 * inch, 5.05 * inch, 2.2 * inch, 0.9 * inch, "Super Late", "4.4%", "4,212 orders", RED)
    kpi(c, 10.6 * inch, 5.05 * inch, 2.0 * inch, 0.9 * inch, "Avg Review", "4.09", "delivered", BLUE)
    image_fit(c, ROOT / "outputs" / "sentiment_by_status.png", 1.05 * inch, 1.15 * inch, 5.0 * inch, 3.35 * inch)
    image_fit(c, ROOT / "outputs" / "delay_bucket_sentiment.png", 6.45 * inch, 1.15 * inch, 5.25 * inch, 3.35 * inch)
    c.showPage()

    draw_bg(c, "Regional Delivery Risk", "Geographic heatmap story shown as ranked state performance", 5)
    image_fit(c, ROOT / "outputs" / "late_rate_by_state.png", 0.9 * inch, 1.2 * inch, 7.1 * inch, 4.8 * inch)
    panel(c, 8.45 * inch, 3.2 * inch, 3.9 * inch, 2.25 * inch, "Highest Late Rates", [
        "AL: 23.9%",
        "MA: 19.7%",
        "PI: 16.0%",
        "CE: 15.3%",
        "SE: 15.2%",
    ])
    panel(c, 8.45 * inch, 1.25 * inch, 3.9 * inch, 1.45 * inch, "Interpretation", [
        "The problem is concentrated regionally.",
        "Repair work should start in states above the national benchmark.",
    ])
    c.showPage()

    draw_bg(c, "Customer Sentiment Impact", "Delivery delay vs average review score", 6)
    kpi(c, 0.9 * inch, 4.85 * inch, 2.8 * inch, 1.0 * inch, "On Time Review", "4.29/5", "best experience", GREEN)
    kpi(c, 4.05 * inch, 4.85 * inch, 2.8 * inch, 1.0 * inch, "Late Review", "3.46/5", "moderate damage", AMBER)
    kpi(c, 7.2 * inch, 4.85 * inch, 2.8 * inch, 1.0 * inch, "Super Late Review", "1.79/5", "severe damage", RED)
    kpi(c, 10.35 * inch, 4.85 * inch, 1.85 * inch, 1.0 * inch, "Gap", "2.51", "points", RED)
    panel(c, 1.0 * inch, 1.55 * inch, 5.35 * inch, 2.4 * inch, "Evidence", [
        "Average review score falls as delivery performance worsens.",
        "Super-late orders perform far below on-time orders.",
        "This supports the CEO's concern about over-promising.",
    ])
    panel(c, 6.75 * inch, 1.55 * inch, 5.35 * inch, 2.4 * inch, "Careful Language", [
        "This is observational analysis, so use associated with rather than caused by.",
        "The pattern is still strong enough to guide operations.",
    ])
    c.showPage()

    draw_bg(c, "Candidate's Choice: Product Category Risk", "Translated English category analysis", 7)
    image_fit(c, ROOT / "outputs" / "category_late_rate.png", 0.9 * inch, 1.1 * inch, 7.2 * inch, 4.85 * inch)
    panel(c, 8.55 * inch, 3.45 * inch, 3.65 * inch, 1.85 * inch, "Top Category Risk", [
        "Audio has the highest late rate at 12.9%.",
        "Fashion underwear beach follows at 12.8%.",
        "Home comfort follows at 11.0%.",
    ])
    panel(c, 8.55 * inch, 1.35 * inch, 3.65 * inch, 1.55 * inch, "Business Value", [
        "Category analysis reveals product and fulfillment complexity.",
        "It adds an improvement path beyond geography.",
    ])
    c.showPage()

    draw_bg(c, "Dashboard Walkthrough", "Public Streamlit audit tool", 8)
    panel(c, 0.85 * inch, 4.35 * inch, 3.65 * inch, 1.35 * inch, "Executive KPIs", [
        "Delivered volume, promise accuracy, late rate, super-late rate, and review damage.",
    ])
    panel(c, 4.85 * inch, 4.35 * inch, 3.65 * inch, 1.35 * inch, "Regional Drilldown", [
        "State selector, regional late-rate ranking, and risk matrix.",
    ])
    panel(c, 8.85 * inch, 4.35 * inch, 3.35 * inch, 1.35 * inch, "Category Drilldown", [
        "Category risk ranking, impact matrix, and leaderboards.",
    ])
    panel(c, 0.85 * inch, 1.6 * inch, 11.35 * inch, 1.85 * inch, "Dashboard Link", [
        "https://amalitech-pzzepkval4rfh3phyyf2jh.streamlit.app/",
        "Built from summary CSVs only, so the raw Kaggle dataset is not required for deployment.",
    ])
    c.showPage()

    draw_bg(c, "Recommendations", "Operational actions for Veridi Logistics", 9)
    panel(c, 0.8 * inch, 4.35 * inch, 5.75 * inch, 1.55 * inch, "1. Prioritize Regional Repair", [
        "Start investigations in AL, MA, PI, CE, and SE.",
        "Compare carrier, routing, and fulfillment processes in these states.",
    ])
    panel(c, 6.85 * inch, 4.35 * inch, 5.45 * inch, 1.55 * inch, "2. Recalibrate Delivery Promises", [
        "Use more conservative estimates in high-risk states.",
        "Track promise accuracy as an executive KPI.",
    ])
    panel(c, 0.8 * inch, 2.05 * inch, 5.75 * inch, 1.55 * inch, "3. Track Super-Late Separately", [
        "Super-late orders are associated with the steepest review damage.",
        "Escalate orders once they pass five days late.",
    ])
    panel(c, 6.85 * inch, 2.05 * inch, 5.45 * inch, 1.55 * inch, "4. Review Product Categories", [
        "Investigate audio and other high-risk categories.",
        "Check packaging, seller behavior, and carrier handling.",
    ])
    c.showPage()

    draw_bg(c, "Submission Checklist", "Final reviewer-facing deliverables", 10)
    panel(c, 0.9 * inch, 3.65 * inch, 5.6 * inch, 2.2 * inch, "Included in Repository", [
        "README with executive summary and technical notes.",
        "Notebook and HTML notebook export.",
        "Streamlit app and requirements file.",
        "Dashboard-ready outputs and static chart exports.",
    ])
    panel(c, 6.85 * inch, 3.65 * inch, 5.25 * inch, 2.2 * inch, "Public Links to Test", [
        "GitHub repository.",
        "Streamlit dashboard.",
        "Presentation PDF.",
        "Optional video walkthrough if created.",
    ])
    panel(c, 1.05 * inch, 1.3 * inch, 11.0 * inch, 1.15 * inch, "Final CEO Answer", [
        "Delivery failures are concentrated in specific regions and are strongly associated with lower customer reviews, especially when orders become super late.",
    ])
    c.showPage()

    c.save()


if __name__ == "__main__":
    build_pdf()
    print(PDF_PATH)
