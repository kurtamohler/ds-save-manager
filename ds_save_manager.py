#!/usr/bin/env python
import argparse
import os
import sys
import distutils.dir_util
import datetime
import warnings

game_dir = os.path.join(os.environ["HOME"], ".steam/steam/steamapps/compatdata/570940/pfx/drive_c/users/steamuser/My Documents/NBGI/DARK SOULS REMASTERED")
saves_dir = os.path.join(os.environ["HOME"], "Documents/ds1_backups")

def get_saves():
    return os.listdir(saves_dir)

def list_saves():
    saves = get_saves()
    print('Existing saves in dir "%s":' % saves_dir)
    for save in sorted(saves):
        print("  %s" % save)

def parse_save_name(save_name):
    save_name_split = save_name.split('.')
    save_name_idx = int(save_name_split[1].split('-')[0])
    return save_name_split[0], save_name_idx

def save(label):
    cur_date = datetime.datetime.today().strftime('%Y_%m_%d')
    cur_ind = 0
    # If any other saves exist for this date, make sure to use a unique index
    for save in get_saves():
        save_date, save_ind = parse_save_name(save)
        if save_date == cur_date:
            if save_ind >= cur_ind:
                cur_ind = save_ind + 1
    new_save = cur_date + '.%03d' % cur_ind
    if label:
        new_save += '-' + label
    new_save_path = os.path.join(saves_dir, new_save)
    print('Saving under name: %s' % new_save)
    print('Saving to directory: %s' % new_save_path)
    distutils.dir_util.copy_tree(game_dir, new_save_path)

def load(save_name):
    save_path = os.path.join(saves_dir, save_name)
    print('Loading from directory: %s' % save_path)
    distutils.dir_util.copy_tree(save_path, game_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = 'Manage Dark Souls save files'
    )
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--save', action='store_true')
    parser.add_argument('--label', type=str)
    parser.add_argument('--load', type=str)
    args = parser.parse_args()
    if args.load and args.save:
        raise RuntimeError("Cannot load and save")
    if args.load and args.list:
        raise RuntimeError("Cannot load and list")
    if args.save and args.list:
        raise RuntimeError("Cannot save and list")

    if args.list:
        if args.label:
            warnings.warn('"--label" arg is only used when saving')
        list_saves()
    elif args.save:
        save(args.label)
    elif args.load:
        if args.label:
            warnings.warn('"--label" arg is only used when saving')
        load(args.load)
    else:
        parser.print_help(sys.stderr)
