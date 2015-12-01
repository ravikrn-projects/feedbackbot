from PIL import Image

frame_x2_input = "Frame_2.png"
frame_x4_input = "Frame_4.png"
frame_x2_output = "inframe_2.png"
frame_x4_output = "inframe_4.png"

files = ["a.png", "b.png", "b.png", "a.png"]


def fill_frame(frame, output_frame, file_count, coordinates, x_scale_factor, y_scale_factor):
    img_objects = [Image.open(file_name) for file_name in files[:file_count]]
    new_size = (frame.size[0]/x_scale_factor-80, frame.size[1]/y_scale_factor-80) 
    new_img_objects = [obj.resize(new_size) for obj in img_objects]
    for img_num in range(len(new_img_objects)):
        frame.paste(new_img_objects[img_num], coordinates[img_num])
    frame.save(output_frame)


def fill_x2_frame():
    frame = Image.open(frame_x2_input)
    coordinates = [(70, 40), (frame.size[0]/2+10, 40)]
    fill_frame(frame, frame_x2_output, 2, coordinates, 2, 1)


def fill_x4_frame(): 
    frame = Image.open(frame_x4_input)
    coordinates = [(70, 40), (frame.size[0]/2+10, 40), (70, frame.size[1]/2+40), (frame.size[0]/2+10, frame.size[1]/2+40)]
    fill_frame(frame, frame_x4_output, 4, coordinates, 2, 2)


fill_x2_frame()
fill_x4_frame()


