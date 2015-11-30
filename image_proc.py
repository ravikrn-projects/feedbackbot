from PIL import Image

filename1 = "a.png"
filename2 = "b.png"
filename3 = "a.png"
filename4 = "b.png"

frame_x2_input = "Frame_2.png"
frame_x4_input = "Frame_4.png"
frame_x2_output = "inframe_2.png"
frame_x4_output = "inframe_4.png"

def fill_x2_frame():
    frame = Image.open(frame_x2_input)
    img1 = Image.open(filename1)
    img2 = Image.open(filename2)
    new_size = (frame.size[0]/2-80, frame.size[1]-80) 
    img1 = img1.resize(new_size)
    img2 = img2.resize(new_size) 
    frame.paste(img1, (70, 40))
    frame.paste(img2, (frame.size[0]/2+10, 40))
    frame.save(frame_x2_output)


def fill_x4_frame():
    frame = Image.open(frame_x4_input)
    img1 = Image.open(filename1)
    img2 = Image.open(filename2)
    img3 = Image.open(filename3)
    img4 = Image.open(filename4)
    new_size = (frame.size[0]/2-80, frame.size[1]/2-80) 
    img1 = img1.resize(new_size)
    img2 = img2.resize(new_size) 
    img3 = img3.resize(new_size) 
    img4 = img4.resize(new_size) 
    frame.paste(img1, (70, 40))
    frame.paste(img2, (frame.size[0]/2+10, 40))
    frame.paste(img3, (70, frame.size[1]/2+40))
    frame.paste(img4, (frame.size[0]/2+10, frame.size[1]/2+40))
    frame.save(frame_x4_output)

fill_x2_frame()
fill_x4_frame()


