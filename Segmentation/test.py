from PIL import Image, ImageDraw

im = Image.open("Testing Images/test.JPG")
draw = ImageDraw.Draw(im)
draw.rectangle([593, 46, 675, 109], outline = "red")
draw.rectangle([490, 46, 545, 110], outline = "red")
draw.rectangle([723, 46, 779, 110], outline = "red")
draw.rectangle([236, 46, 292, 110], outline = "red")
draw.rectangle([139, 24, 189, 109], outline = "red")
draw.rectangle([444, 108, 444, 108], outline = "red")
draw.rectangle([374, 24, 441, 109], outline = "red")
draw.rectangle([27, 24, 94, 110], outline = "red")
im.show()


# {"startRow": 24, "startCol": 139, "endRow": 109, "endCol": 189}, 
# {"startRow": 108, "startCol": 444, "endRow": 108, "endCol": 444}, 
# {"startRow": 24, "startCol": 374, "endRow": 109, "endCol": 441}, 
# {"startRow": 24, "startCol": 27, "endRow": 109, "endCol": 94}]