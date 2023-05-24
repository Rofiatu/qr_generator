import qrcode
from qrcode import constants
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
import tempfile
import uuid
import os

# Create a PDF canvas
total_qrcodes = 50
qrcodes_per_pdf = 10
pdf_files = total_qrcodes // qrcodes_per_pdf

for file_num in range(1, pdf_files + 1):
    filename = f'qr_code{file_num}.pdf'
    c = canvas.Canvas(filename, pagesize=landscape(letter))

    for qr_num in range(1, qrcodes_per_pdf + 1):

        data = str(uuid.uuid4())

        # generate the QR code image
        qr = qrcode.QRCode(
            version=1,
            error_correction=constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # create a temporary png file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp:
            tempfilename = temp.name
            qr_image.save(tempfilename)

        # get the page size
        width, height = c._pagesize

        # calculate the position of the QR code on the page
        x = width / 2 # X-coordinate
        y = height / 2 # Y-coordinate

        qr_width = width * 0.75
        qr_height = height * 0.75

        # draw the QR code on the PDF canvas
        c.drawImage(tempfilename, x - qr_width / 2, y - qr_height / 2, width=qr_width, height=qr_height)

        # remove the temporary PNG file
        os.remove(tempfilename)

        c.showPage()

    # save the PDF document
    c.save()