
Launchbear -- The extensible program launcher
=============================================

* (c) 2012-2022 P. S. Clarke.
* Contribute via <https://github.com/pscl4rke/launchbear>.
* Licensed under the GNU Public Licence version 3.

Launchbear's goal is to make it very quick to launch graphical
applications in your desktop environment, and to do so in a way
that is painless for a power user to enhance.

It interacts with the user through a "frontend".  Currently the
main frontend it knows how to use is
[dmenu](https://tools.suckless.org/dmenu/).
There is some support for `wofi` too.

It knows what is available to launch by running all the executables
in `~/.launchbear/backends/`.  They are expected to emit options in
a format similar to calling commands in a shell script.

A number of scripts are included.  For example:

* `xdg-apps` finds all the XDG `.desktop` files for installed applications.
* `linkbear` uses `linkbear` to search websites.
* `gtk-bookmarks` finds the locations bookmarked in the file manager.
* `aisleriot` has an option for each card game available.
