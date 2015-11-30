from PIL import Image

frame = Image.open("Frame_2.png")
img1 = Image.open("a.png")
img2 = Image.open("b.png")
new_size = (frame.size[0]/2-80, frame.size[1]-80) 
img2 = img2.resize(new_size) 
img1 = img1.resize(new_size)
frame.paste(img1, (70, 40))
frame.paste(img2, (frame.size[0]/2+10, 40))
frame.save("inframe_2.png")



frame = Image.open("Frame_4.png")
img1 = Image.open("a.png")
img2 = Image.open("b.png")
img3 = Image.open("b.png")
img4 = Image.open("a.png")
new_size = (frame.size[0]/2-80, frame.size[1]/2-80) 
img1 = img1.resize(new_size)
img2 = img2.resize(new_size) 
img3 = img3.resize(new_size) 
img4 = img4.resize(new_size) 
frame.paste(img1, (70, 40))
frame.paste(img2, (frame.size[0]/2+10, 40))
frame.paste(img3, (70, frame.size[1]/2+40))
frame.paste(img4, (frame.size[0]/2+10, frame.size[1]/2+40))
frame.save("inframe_4.png")



