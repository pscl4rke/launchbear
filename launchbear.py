#!/usr/bin/python3

"""
//  LAUNCHBEAR

Launchbear is a piece of middleware designed to launch applications
in a GUI environment.  It takes selectable items from plugins, and
allows them to be picked using a front-end.
"""


import argparse
import os
import shlex
import subprocess
import pickle
import sys


class HistoryFile:
    """Tracks what has been launched to order by popularity."""

    max_history = 500

    def __init__(self):
        self.location = os.path.join(os.environ['HOME'], ".launchbear", "history")
        self.history = []
        try:
            with open(self.location) as infile:
                for line in infile:
                    self.history.append(line.strip())
        except IOError:
            pass # presumably doesn't exist yet

    def update(self, choice_id):
        self.history.append(choice_id)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        with open(self.location, 'w') as outfile:
            for choice_id in self.history:
                outfile.write("%s\n" % choice_id)

    def score(self, choice_id):
        score = 0
        for previous in self.history:
            if previous == choice_id:
                score += 1
        return score


class ChoiceGenerator:
    """A backend that provides a number of choices."""

    def __init__(self, backend_location):
        """Create a new ChoiceGenerator."""
        self._backend_location = backend_location
        self._choices = []

    def choices(self):
        """Returns a set of choices."""
        choices_available = {}
        for choice in self._choices:
            if "id" not in choice:
                continue
            choices_available[choice["id"]] = choice
        return choices_available

    def run_until_loaded(self):
        # these two parts could be separated so that each Popen is
        # run in parallel for improved responsiveness
        self.process = subprocess.Popen(self._backend_location,
                    stdout=subprocess.PIPE, shell=True)
        self.parse(self.process.stdout)

    def parse(self, stream):
        """Build a set of choices from a file stream."""
        for line in stream.readlines():
            arguments = shlex.split(line.decode(), comments=True)
            if len(arguments) == 0:
                continue
            handler_name = "handle_%s" % arguments[0]
            if not hasattr(self, handler_name):
                print("Unknown directive '%s'" % arguments[0])
            else:
                getattr(self, handler_name)(arguments[1:])

    def load(self, cached_data):
        """Build a set of choices from previously cached data."""
        if 'choices' in cached_data:
            self._choices = cached_data['choices']
        else:
            self._choices = {}

    def save(self):
        """Returns the cache form that can be loaded."""
        return {
            'choices': self._choices,
        }

    def handle_addchoice(self, arguments):
        choice_properties = {}
        for argument in arguments:
            if not argument.startswith("--"):
                continue
            dashed_key, equals, value = argument.partition("=")
            if equals != "=":
                continue
            choice_properties[dashed_key[2:]] = value
        self._choices.append(choice_properties)


class DmenuFrontend:
    """A picker based around dmenu."""

    def pick(self, choices):
        """Presents the choices and returns the id chosen or None."""
        lines = []
        for choice in choices:
            parts = []
            if 'title' in choice:
                parts.append(choice['title'])
            if 'cmd' not in choice:
                continue
            parts.append("(%s)" % choice['cmd'])
            if 'id' not in choice:
                continue
            parts.append("||| %s" % choice['id'])
            lines.append(" ".join(parts))
        command = [
            "dmenu", "-i", "-l", "6",
            "-fn", "-*-arial-*-r-*-*-*-*-*-*-*-*-*",
            "-nb", "#444", "-nf", "#DDD", "-sb", "#757",
            "-p", "Run:",
        ]
        process = subprocess.Popen(command,
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = process.communicate(("\n".join(lines)).encode())
        if len(stdout) == 0:
            return None
        rest, bars, choice_id = stdout.strip().decode().partition("||| ")
        return choice_id


def default_cache_path():
    homedir = os.environ['HOME']
    return os.path.join(homedir, ".launchbear/cache.pkl")


def load_cachefile(cache_path=None):
    """Return the cached data, or blank data."""
    if cache_path is None:
        cache_path = default_cache_path()
    try:
        with open(cache_path, "rb") as cache_file:
            return pickle.load(cache_file)
    except Exception:
        return {'generators': {}}


def save_cachefile(cache, cache_path=None):
    """Saves the given cache to disk."""
    if cache_path is None:
        cache_path = default_cache_path()
    with open(cache_path, "wb") as cache_file:
        pickle.dump(cache, cache_file)


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--backend-dir", default="~/.launchbear/backends")
    return parser.parse_args(args)


def main():
    opts = parse_args(sys.argv[1:])
    backend_names = os.listdir(os.path.expanduser(opts.backend_dir))
    cache = load_cachefile()
    history = HistoryFile()
    all_choices = {}
    for backend_name in backend_names:
        backend_location = os.path.join(opts.backend_dir, backend_name)
        generator = ChoiceGenerator(backend_location)
        if backend_name in cache['generators']:
            generator.load(cache['generators'][backend_name])
        else:
            generator.run_until_loaded()
            cache['generators'][backend_name] = generator.save()
        choices_available = generator.choices()
        all_choices.update(choices_available)
    save_cachefile(cache)
    frontend = DmenuFrontend()
    #sortable_choices = [(history.score(x['id']), x) for x in all_choices.values()]
    #sortable_choices.sort(reverse=True, key=lambda (a, b): a)
    choices_for_picking = [x for x in all_choices.values()]
    choices_for_picking.sort(reverse=True, key=lambda x: history.score(x))
    choice_id = frontend.pick(choices_for_picking)
    if choice_id is not None:
        history.update(choice_id)
        command = "%s &" % all_choices[choice_id]['cmd']
        subprocess.call(command, shell=True)


if __name__ == '__main__':
    main()
