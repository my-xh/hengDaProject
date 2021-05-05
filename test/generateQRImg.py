import qrcode
from PIL import Image

def create_qrcode(url, file_name):
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.ERROR_CORRECT_H,
                       box_size=10,
                       border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.convert('RGBA')
    
    icon = Image.open(file_name)
    w, h = img.size
    factor = 4
    icon_w, icon_h = min(icon.size[0], int(
        w / factor)), min(icon.size[1], int(h / factor))
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS).convert('RGBA')

    x, y = int((w - icon_w) / 2), int((h - icon_h) / 2)
    blank = Image.new('RGBA', (icon_w + 8, icon_h + 8), color=(255, 255, 255))

    img.paste(blank, (x - 4, y - 4), blank)
    img.paste(icon, (x, y), icon)
    img.save('../static/img/qr.png', quality=95)

if __name__ == '__main__':
    create_qrcode('http://192.168.1.101:8000', 'logo.png')
    print('成功')
