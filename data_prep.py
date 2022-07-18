import glob
import os
import xml.etree.ElementTree as ET
from typing import List


data_dir = "datasets/images"
base_dir = "datasets"
classes = os.listdir(data_dir)



def get_images_in_dir(dir_path: str) -> List[str]:
    images = []
    for classname in classes:
        for filename in glob.glob(dir_path + "/" + classname + "/"+ "*.jpg"):
            images.append(filename)
    return images

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(dir_path: str, image_path: str):

    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]
    

    class_name = image_path.split("/")[-2]

    if not os.path.exists(base_dir + "/labels/" +  class_name ):
        os.makedirs(base_dir + "/labels/" +  class_name )

    if not os.path.exists(dir_path + "/" +  class_name + "/" ):
        os.makedirs(dir_path + "/" +  class_name + "/")
    
    input_file = open(dir_path + "/" +  class_name + "/" + basename_no_ext + ".xml")
    output_file = open(base_dir + "/labels/"  + class_name + "/" +basename_no_ext + ".txt", "w")
    tree = ET.parse(input_file)
    root = tree.getroot()
    size = root.find("size")
    w = int(size.find("width").text)
    h = int(size.find("height").text)

    for obj in root.iter('object'):
        cls = obj.find("name").text

        if cls not in classes:
            continue
    
        cls_id = classes.index(cls)
        xmlbox = obj.find("bndbox")
        b = (float(xmlbox.find("xmin").text), float(xmlbox.find("xmax").text), float(xmlbox.find("ymin").text), float(xmlbox.find("ymax").text))
        bb = convert((w,h), b)
        output_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

def extract_xml_to_json(xml_file: str):
    root = ET.parse(xml_file).getroot()
    
    # Initialise the info dict 
    info_dict = {}
    info_dict['bboxes'] = []

    # Parse the XML Tree
    for elem in root:
        # Get the file name 
        if elem.tag == "filename":
            info_dict['filename'] = elem.text
            
        # Get the image size
        elif elem.tag == "size":
            image_size = []
            for subelem in elem:
                image_size.append(int(subelem.text))
            
            info_dict['image_size'] = tuple(image_size)
        
        # Get details of the bounding box 
        elif elem.tag == "object":
            bbox = {}
            for subelem in elem:
                if subelem.tag == "name":
                    bbox["class"] = subelem.text
                    
                elif subelem.tag == "bndbox":
                    for subsubelem in subelem:
                        bbox[subsubelem.tag] = int(subsubelem.text)            
            info_dict['bboxes'].append(bbox)
    
    return info_dict

def create_xml_annotations(dir_path: str, image_path: str):
    class_name = image_path.split("/")[-2]  
    file_name = image_path.split("/")[-1]  

    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]

    class_name = image_path.split("/")[-2]
    if not os.path.exists(dir_path + "/" +  class_name + "/" ):
        os.makedirs(dir_path + "/" +  class_name + "/")
    annotation = """<annotation>
            <folder>train</folder>
            <filename>{}</filename>
            <size>
                <width>224</width>
                <height>224</height>
                <depth>3</depth>
            </size>
            <object>
                <name>{}</name>
                <bndbox>
                    <xmin>11</xmin>
                    <ymin>10</ymin>
                    <xmax>203</xmax>
                    <ymax>203</ymax>
                </bndbox>
            </object>
    </annotation>""".format(file_name, class_name)
    with open(dir_path + "/" +  class_name + "/" + basename_no_ext + ".xml", "w") as f:
        f.write(annotation)
        f.close()

output_path = base_dir + "/labels"

if not os.path.exists(output_path):
    os.makedirs(output_path)

images_paths = get_images_in_dir(data_dir)
list_file = open('' + '.txt', 'w')

for image_path in images_paths:
    create_xml_annotations(data_dir, image_path)

for image_path in images_paths:
    list_file.write(image_path + '\n')
    convert_annotation(data_dir, image_path)
list_file.close()
