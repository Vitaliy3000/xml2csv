import csv
import glob
import os
import xml.etree.cElementTree as ET
import zipfile

import settings


def main():
    with open("levels.csv", "w") as csv_levels_file, open("objects.csv", "w") as csv_objects_file:

        levels_writer = csv.writer(csv_levels_file)
        levels_writer.writerow(["id", "level"])

        objects_writer = csv.writer(csv_objects_file)
        objects_writer.writerow(["id", "object_name"])

        zipfilenames = glob.glob(os.path.join(settings.DATA_PATH, "*.zip"))
        for zipfilename in zipfilenames:
            process_zipfile(
                zipfilename, levels_writer=levels_writer, objects_writer=objects_writer
            )


def process_zipfile(zipfilename, *, levels_writer, objects_writer):
    with zipfile.ZipFile(zipfilename) as zip:
        filenames = zip.namelist()
        for filename in filenames:
            id, level, objects = read_data(zip=zip, filename=filename)
            write_data(
                id=id,
                level=level,
                objects=objects,
                levels_writer=levels_writer,
                objects_writer=objects_writer,
            )


def read_data(*, zip, filename):
    with zip.open(filename) as f:
        return ET.fromstring(f.read())


def write_data(*, id, level, objects, levels_writer, objects_writer):
    levels_writer.writerow([id.get("value"), level.get("value")])

    for object in objects:
        objects_writer.writerow([id.get("value"), object.get("name")])


if __name__ == "__main__":
    main()
