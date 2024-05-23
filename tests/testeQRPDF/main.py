import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Image

def generate_qrcode(data, output_path):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)

def insert_qrcode_into_pdf(input_pdf_path, qrcode_path, output_pdf_path):
    # Abra o PDF existente e crie um novo PDF
    input_pdf = PdfReader(input_pdf_path)
    output_pdf = PdfWriter()

    # Copie todas as páginas do PDF original para o novo PDF
    for page in input_pdf.pages:
        output_pdf.add_page(page)

    # Obtenha o número total de páginas no PDF
    total_pages = len(input_pdf.pages)

    # Adicione o QR code à última página do PDF
    qr_code_img = Image(qrcode_path)
    qr_code_img.drawHeight = 100
    qr_code_img.drawWidth = 100

    doc = SimpleDocTemplate("temp.pdf", pagesize=letter)
    doc.build([qr_code_img])

    temp_pdf = PdfReader("temp.pdf")

    # Salve o novo PDF
    with open(output_pdf_path, "wb") as output_file:
        output_pdf.write(output_file)
        output_pdf.add_page(temp_pdf.pages[0])

# Exemplo de uso
input_pdf_path = "comprovativo.pdf"
data_for_qrcode = "Testando agora"
qrcode_path = "qrCode.png"
output_pdf_path = "documento_com_qrcode.pdf"

generate_qrcode(data_for_qrcode, qrcode_path)
insert_qrcode_into_pdf(input_pdf_path, qrcode_path, output_pdf_path)