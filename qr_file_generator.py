import uuid
import qrcode
from qrcode import constants
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
import tempfile
import os
import itertools

def generate_id():
    total_ids = 50
    filename = 'idfile.csv'

    with open(filename, 'w') as file:
        for _ in range(total_ids):
            data = str(uuid.uuid4())
            file.write(data + '\n')

    return filename

def generate_qr_code(data, filename, folder):
    qr = qrcode.QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image.save(os.path.join(folder, filename))

def generate_qr_code_pdfs(folder):
    filename = generate_id()

    with open(filename, 'r') as file:
        content = file.readlines()

    qr_codes_per_pdf = 10
    pdf_files = 5

    for file_num in range(1, pdf_files + 1):
        pdf_filename = f'qr_code{file_num}.pdf'
        pdf_path = os.path.join(folder, pdf_filename)
        c = canvas.Canvas(pdf_path, pagesize=letter)

        chunk = content[(file_num - 1) * qr_codes_per_pdf:file_num * qr_codes_per_pdf]

        for qr_num, qr_code in enumerate(chunk, start=1):
            data = qr_code.strip()
            temp_filename = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
            generate_qr_code(data, temp_filename, folder)

            # qr_width = width * 0.75
            # qr_height = height * 0.75

            x = 120
            y = 200

            c.drawImage(temp_filename, x, y, width=400, height=400)

            os.remove(temp_filename)

            c.showPage()

        c.save()

folder = 'qr_codes_folder'
os.makedirs(folder, exist_ok=True)
generate_qr_code_pdfs(folder)
