import qrcode
from qrcode import constants
import uuid

# Generate the QR code
i = 5
for i in range(1, i):

    data = str(uuid.uuid4())
    qr = qrcode.QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    filename = f'qr_code{i}.png'

    qr_image.save(filename)

