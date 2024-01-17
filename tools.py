from fpdf import FPDF
import base64
import urllib.parse


def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    filename = urllib.parse.quote(filename)
    return f"data:application/octet-stream;base64,{b64.decode()}"


def getDownloadURI(text, fileName="AnalysisReport.pdf"):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_right_margin(3)
    pdf.set_font(family="Arial", size=16)
    pdf.set_font_size(24)
    pdf.cell(200, 10, "Analysis Report", ln=1, align="C")
    pdf.ln(20)
    pdf.set_font_size(14)
    for t in text.split("\n"):
        pdf.multi_cell(200, 10, t)
    return create_download_link(pdf.output(dest="S").encode("latin-1"), fileName)


def prepareResponse(st):
    if "response" in st.session_state:
        return st.session_state.response
    else:
        return "Hello World"
