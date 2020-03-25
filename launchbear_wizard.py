#!/usr/bin/python3


import os
import subprocess
import sys


class Wizard:

    def __init__(self):
        HOME = os.environ['HOME']
        self.config_dir = os.path.join(HOME, '.launchbear')
        self.backend_dir = os.path.join(HOME, '.launchbear', 'backends')
        self.changes_made = []

    def print_welcome(self):
        print()
        print("This script will take the user through setting")
        print("up their personal preferences for launchbear.")
        print()

    def create_config_dirs(self):
        if os.path.isdir(self.config_dir):
            print("%s already exists" % self.config_dir)
        else:
            os.mkdir(self.config_dir)
            print("created %s" % self.config_dir)
        if os.path.isdir(self.backend_dir):
            print("%s already exists" % self.backend_dir)
        else:
            os.mkdir(self.backend_dir)
            print("created %s" % self.backend_dir)

    def offer_to_symlink_backends_from(self, backend_src):
        for backend_name in os.listdir(backend_src):
            src = os.path.join(backend_src, backend_name)
            dest = os.path.join(self.backend_dir, backend_name)
            if os.path.exists(dest):
                print()
                print("You already have %s: Skipping" % backend_name)
                continue
            answer = ''
            while answer not in ('y', 'n'):
                print()
                print("Do you want to install %s?" % backend_name)
                prt = "[y]es, [n]o or use pager to [v]iew script or [p]review output? "
                answer = input(prt).lower()[:1]
                if answer == 'v':
                    PAGER = os.environ.get('PAGER', 'less')
                    subprocess.call([PAGER, src])
                if answer == 'p':
                    PAGER = os.environ.get('PAGER', 'less')
                    preview = subprocess.Popen(src, stdout=subprocess.PIPE)
                    subprocess.call([PAGER, "-"], stdin=preview.stdout)
            if answer == 'y':
                os.symlink(src, dest)
                self.changes_made.append(backend_name)
                print("Created %s" % dest)

    def wipe_the_cache(self):
        print()
        if len(self.changes_made) == 0:
            print("No changes made, so will not touch the cache file")
            return
        cache_file = os.path.join(self.config_dir, 'cache.pkl')
        if os.path.exists(cache_file):
            os.remove(cache_file)
            print("Removed cache file %s" % cache_file)
        else:
            print("There is no cache file that needs removing")
        print()

    def main(self):
        self.print_welcome()
        self.create_config_dirs()
        if len(sys.argv) == 2:
            backend_src = os.path.realpath(sys.argv[1])
        else:
            backend_src = "/usr/share/launchbear/backends"
        self.offer_to_symlink_backends_from(backend_src)
        self.wipe_the_cache()


if __name__ == '__main__':
    Wizard().main()
