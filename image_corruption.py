def image_corruption(image):
  with open(image, 'rb') as f:
      contents = f.read().hex()
  contents = contents.replace("3", "0")
  with open(image, 'wb') as f:
      f.write(bytes.fromhex(contents))
