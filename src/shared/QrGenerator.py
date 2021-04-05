import qrcode

class QrGenerator():


    @staticmethod
    def get_url(id):
        encodeUrl = 'http://192.168.0.118:8012/' + id
        return encodeUrl
        
    @staticmethod
    def generate(id):
        encodeUrl = 'http://192.168.0.118:8012/' + id

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(encodeUrl)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        return img
