import binascii
import struct
import os

def get_strings(data):
  strings = []
  offset = 0
  while offset < len(data):
    string_length = struct.unpack('<I', data[offset:offset + 4])[0]
    if string_length > 0:
      string = data[offset + 4:offset + 4 + string_length]
      strings.append(string)
    offset += 4 + string_length
  return strings

def get_magic_numbers(data):
  magic_numbers = []
  offset = 0
  while offset < len(data):
    magic_number = data[:2]
    if magic_number in [b'BM', b'II', b'P6', b'RGB', b'RGBA']:
      magic_numbers.append(magic_number)
    offset += 2
  return magic_numbers

def get_image_info(data):
  image_info = {}

  magic_number = data[:2]
  image_info['magic_number'] = magic_number

  width, height = struct.unpack('<II', data[14:22])
  image_info['width'] = width
  image_info['height'] = height

  compression = data[22]
  image_info['compression'] = compression

  if magic_number == b'BM':
    color_table_size = struct.unpack('<I', data[28:32])[0]
    image_info['color_table_size'] = color_table_size
  else:
    color_table_size = 0

  return image_info

def main():
  # Liste des images disponibles
  image_paths = ['image1.jpg', 'image2.png', 'image3.bmp']

  # Sélection de l'image à analyser
  image_path = input('Sélectionnez l\'image à analyser : ')
  if image_path not in image_paths:
    print('Image introuvable.')
    exit()

  # Lecture de l'image
  with open(image_path, 'rb') as f:
    data = f.read()

  # Récupération des informations sur l'image
  strings = get_strings(data)
  magic_numbers = get_magic_numbers(data)
  image_info = get_image_info(data)

  # Affichage des informations sur l'image
  print('Strings :')
  for string in strings:
    print(string)

  print('Magic numbers :')
  for magic_number in magic_numbers:
    print(magic_number)

  print('Informations sur l\'image :')
  for key, value in image_info.items():
    print('{}: {}'.format(key, value))

if __name__ == '__main__':
  main()
