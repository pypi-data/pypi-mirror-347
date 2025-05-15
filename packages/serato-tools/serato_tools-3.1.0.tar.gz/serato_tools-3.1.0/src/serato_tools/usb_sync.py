import sys
import os
import filecmp
import shutil

if __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from serato_tools.database_v2 import DatabaseV2
from serato_tools.utils import DataTypeError, SERATO_FOLDER as LOCAL_SERATO_FOLDER
from serato_tools.crate import Crate

DEST_PARENT_DIR = "E:\\"
TRACK_FOLDER = "Tracks"
SERATO_DIR = "_Serato_"


def _uniq_by_basename(paths: list[str]):
    basenames: list[str] = []
    return_paths: list[str] = []
    for path in paths:
        basename = os.path.basename(path)
        if basename not in basenames:
            basenames.append(basename)
            return_paths.append(path)
    return return_paths


def copy_crates_to_usb(crate_files: list[str], dest_parent_dir: str, dest_tracks_folder: str):
    # copy the crate file, and get the filenames from it
    tracks_to_copy: list[str] = []
    crate_dir = os.path.join(dest_parent_dir, SERATO_DIR, "Subcrates")
    if not os.path.exists(crate_dir):
        os.mkdir(crate_dir)
    for crate_file in crate_files:
        crate = Crate(crate_file)

        new_crate_data: Crate.Struct = []
        this_crate_tracks: list[str] = []
        for field, value in crate.data:
            if isinstance(value, list):
                new_crate_value: Crate.Struct = []
                for f, v in value:
                    if f == Crate.Fields.TRACK_PATH:
                        if not isinstance(v, str):
                            raise DataTypeError(v, str, f)
                        if v not in tracks_to_copy:
                            tracks_to_copy.append(v)
                        v = Crate.format_filepath(
                            os.path.join(dest_parent_dir, dest_tracks_folder, os.path.basename(v))
                        )
                        if v not in this_crate_tracks:
                            this_crate_tracks.append(v)
                            new_crate_value.append((f, v))
                    else:
                        new_crate_value.append((f, v))
                value = new_crate_value
            new_crate_data.append((field, value))

        crate.data = new_crate_data
        crate._dump()  # pylint: disable=protected-access
        crate.save(os.path.join(crate_dir, os.path.basename(crate_file)))

    # create the db file
    db = DatabaseV2()
    tracks_to_copy = _uniq_by_basename(tracks_to_copy)
    tracks_to_copy_basenames = [os.path.basename(f) for f in tracks_to_copy]
    new_db_data: DatabaseV2.Struct = []
    for field, value in db.data:
        if isinstance(value, list):
            if field == DatabaseV2.Fields.TRACK:
                for f, v in value:
                    if f == DatabaseV2.Fields.FILE_PATH:
                        if not isinstance(v, str):
                            raise DataTypeError(v, str, f)
                        if os.path.basename(v) in tracks_to_copy_basenames:
                            value = DatabaseV2._modify_data_item(v)
                            new_db_data.append((field, os.path.join(dest_tracks_folder, os.path.basename(v))))
                            # todo: check a list for dupe
            else:
                new_db_data.append((field, value))
        else:
            new_db_data.append((field, value))

    db.data = new_db_data
    db._dump()  # pylint: disable=protected-access
    db.save(os.path.join(dest_parent_dir, SERATO_DIR, "database V2"))
    drive = os.path.splitdrive(LOCAL_SERATO_FOLDER)[0]
    if drive:
        tracks_to_copy = [os.path.join(drive + ":", t) for t in tracks_to_copy]

    for t in tracks_to_copy:
        src_path = os.path.join(drive + ":", t)
        dst_path = os.path.join(dest_parent_dir, dest_tracks_folder, os.path.basename(t))
        copy = True if os.path.exists(dst_path) else filecmp.cmp(src_path, dst_path, shallow=True)
        if copy:
            shutil.copy2(src_path, dst_path)


copy_crates_to_usb(
    crate_files=[
        "C:\\Users\\bvand\\Music\\_Serato_\\Subcrates\\crate 1.crate",
        "C:\\Users\\bvand\\Music\\_Serato_\\Subcrates\\crate 2.crate",
    ],
    dest_parent_dir=DEST_PARENT_DIR,
    dest_tracks_folder=TRACK_FOLDER,
)
