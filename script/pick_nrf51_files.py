#!/usr/bin/env python

import os, shutil, json, pprint, sys
from collections import OrderedDict

help_text = "Usage: python {} <full-noridc-sdk-path> <nrf51-sdk-yotta-module-path>".format(os.path.basename(__file__))

# exclude path to avoid confusion over files of the same name
exclude_path = ["examples", "SVD", "s110", "s120", "s210", "nrf_soc_nosd", "serialization/connectivity",
                'components/libraries/hci/config', 'components/libraries/bootloader_dfu/ble_transport']

if __name__ == "__main__":
    # define source and destination of copy
    arg_valid = True
    if len(sys.argv) != 3:
        arg_valid = False
    else:
        src_folder = sys.argv[1]
        yt_module_dir = sys.argv[2]

        for d in [src_folder, yt_module_dir]:
            if not os.path.isdir(d):
                arg_valid = False
                print src_folder, "is not a folder"

    if not arg_valid:
        print help_text
        sys.exit(1)

    dst_folder = os.path.join(yt_module_dir, "source/nordic_sdk")

    # build a file_list from required_files.txt
    file_list = []
    with open("required_files.txt", "r") as fd:
        for line in fd:
            if not line.strip().startswith("#") and line.strip() != '':
                file_list.append(os.path.basename(line).strip())

    def find(name, path):
        paths = []
        for root, dirs, files in os.walk(path):
            if True not in [x in root for x in exclude_path]:
                if isinstance(name, list):
                    for nm in [x for x in name if x in files]:
                        paths.append(os.path.join(root, nm))
                elif name in files:
                    paths.append(os.path.join(root, name))

        if len(paths) == 0:
            print "-"*30
            print "Warning! No {} found!!!!".format(name)
            print "-"*30
            return None
        elif len(paths) > 1:
            print "-"*30
            print "Warning! More than one {} found!!!!".format(name)
            print paths
            print "-"*30
            return None
        else:
            return paths[0]

    # remove everything from the destination folder
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)

    # find files and copy them
    extra_includes = []
    for fn in file_list:
        src = find(fn, src_folder)
        if src:
            rel_dst = os.path.relpath(src, src_folder)
            dst = os.path.join(dst_folder, rel_dst)
            print src, "->", dst
            #print dst
            directory = os.path.dirname(dst)
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.isfile(dst):
                pass
                shutil.copyfile(src, dst)

            # build a list of extra includes to be added to module.json
            if dst.endswith(".h"):
                inc_rel_path = os.path.relpath(dst, yt_module_dir)
                inc_dir_path = os.path.dirname(inc_rel_path)
                if inc_dir_path not in extra_includes:
                    extra_includes.append(inc_dir_path)

    # write extraIncludes in the module.json file
    mod_json = os.path.join(yt_module_dir, "module.json")
    print "-"*30
    print "Writing extra_includes to {}".format(mod_json)
    print "-"*30
    for n in sorted(extra_includes):
        print n

    with open(mod_json, 'r+') as fd:
        jobj = json.loads(fd.read(), object_pairs_hook=OrderedDict)
        jobj['extraIncludes'] = sorted(extra_includes)
        jdump = json.dumps(jobj, indent=2, separators=(',', ': '))
        fd.seek(0)
        fd.write(jdump)
        fd.write("\n")
        fd.truncate()
