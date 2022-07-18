import os
from PIL import Image
import io, base64
import requests
def create_xml_annotations(dir_path: str, image_path: str):
    class_name = image_path.split("/")[-2]  
    file_name = image_path.split("/")[-1]  

    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]

    class_name = image_path.split("/")[-2]
    if not os.path.exists(dir_path + "/" +  class_name + "/" ):
        os.makedirs(dir_path + "/" +  class_name + "/")
        
#     _file = "{}_{}".format(class_name, file_name)
    
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
    annotation_file = basename_no_ext + ".xml"
    image = Image.open(image_path).convert("RGB")
    buffered = io.BytesIO()
    image.save(buffered, quality=90, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    img_str = img_str.decode("ascii")
    upload_url = "".join([
    "https://api.roboflow.com/object-detection-birds/upload",
    "?api_key=3FwtnbYidT77HWLyw7Ks",
    "&name={}".format(file_name),
    "&split=train"
    ])
    r = requests.post(upload_url, data=img_str, headers={
    "Content-Type": "application/x-www-form-urlencoded"
    })
    print(r.text)
    
    img_id = r.json()['id']
    
    upload_url = "".join([
    "https://api.roboflow.com/dataset/object-detection-birds/annotate/{}".format(img_id),
    "?api_key=3FwtnbYidT77HWLyw7Ks",
    "&name=",annotation_file
    ])
    r = requests.post(upload_url, data=annotation, headers={
    "Content-Type": "text/plain"
    })
    print(r.text)