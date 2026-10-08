from pathlib import Path
import xml.etree.ElementTree as ET

data_dir = Path(__file__).parent.parent / "data"
xml_file = data_dir / "megt90n000fb.xml"

print("XML File: ",xml_file)
print("Exists: ",xml_file.exists())

tree = ET.parse(xml_file)
root = tree.getroot()

PDS_NAMESPACE = "http://pds.nasa.gov/pds4/pds/v1"
namespaces = {
    "pds": PDS_NAMESPACE
}

element_array = root.find(
    ".//pds:Element_Array", namespaces
)
print("\n Element Array:")
print(element_array)



for child in element_array:
    print("Tag:", child.tag)
    print("Value:", child.text)
    print()