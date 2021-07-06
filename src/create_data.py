import os
import string
import random
import uuid
import xml.etree.cElementTree as ET
import zipfile

import settings


MIN_LEVEL = 1
MAX_LEVEL = 100
MIN_COUNT_OBJECTS = 1
MAX_COUNT_OBJECTS = 10
CHARS = string.ascii_letters + string.digits


def main():
    create_directory_force(settings.DATA_PATH)

    for i in range(settings.COUNT_ZIPFILES):
        zipfilename = os.path.join(settings.DATA_PATH, f"{i}.zip")
        with zipfile.ZipFile(zipfilename, "w") as zip:
            for j in range(settings.COUNT_XMLFILES):
                xml_root = create_xml_root()
                zip.writestr(f"{i}_{j}.txt", ET.tostring(xml_root).decode())


def create_directory_force(path):
    if os.path.exists(path):
        os.remove(path)

    os.mkdir(path)


def create_xml_root():
    root = ET.Element("root")
    id = ET.SubElement(root, "var", name="id", value=str(uuid.uuid4()))
    level = ET.SubElement(
        root, "var", name="level", value=str(random.randint(MIN_LEVEL, MAX_LEVEL))
    )
    objects = ET.SubElement(root, "objects")

    count_objects = random.randint(MIN_COUNT_OBJECTS, MAX_COUNT_OBJECTS)
    for _ in range(count_objects):
        ET.SubElement(objects, "object", name=random_string())

    return root


def random_string(size=10):
    return "".join(random.choice(CHARS) for _ in range(size))


if __name__ == "__main__":
    main()
