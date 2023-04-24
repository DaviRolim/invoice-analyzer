# https://qqqa42fizadtlmz5ry7htvs3rm0cmrjy.lambda-url.us-east-1.on.aws/
import requests
from PIL import Image
import PIL
'''Compressing image
https://understandingdata.com/python-for-seo/image-resizing-in-python/'''
base_width = 360
image = Image.open('receipt2.jpg')
width_percent = (base_width / float(image.size[0]))
hsize = int((float(image.size[1]) * float(width_percent)))
image = image.resize((base_width, hsize), PIL.Image.ANTIALIAS)
image.save('resized_compressed_image.jpg')

'''Sending compressed image to lambda in bytes'''
document_name = 'resized_compressed_image.jpg'
with open(document_name, 'rb') as file:
    img_test = file.read()
    bytes_test = bytearray(img_test)
    print('Image loaded', document_name)
res = requests.post('https://qqqa42fizadtlmz5ry7htvs3rm0cmrjy.lambda-url.us-east-1.on.aws/', data=bytes_test)
print(res.text)