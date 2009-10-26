# The virtualenv "site.py"

import os, sys

# Welcome to virtualenv!

# The virtual environment logic is invested in the following function,
# rather than just running in the global scope of this module, because
# multiple virtual environments might be stacked on top of each other,
# and when each environment calls "execfile()" on its parent's "site.py"
# any global variables in this module are overwritten.

def virtualenv_init():
    
    # First, we determine where this present virtualenv is located, and
    # note what its native sys.prefix is.

    libpython = os.path.dirname(__file__)
    prefix = sys.prefix

    # Next, we read the cached sys.prefix of the Python installation
    # that was used to create this virtual environment.

    f = open(os.path.join(libpython, 'orig-prefix.txt'))
    sys.real_prefix = f.read().strip()
    f.close()

    # And, finally, we breathe a sign of relief!  Up to this point, the
    # virtual environment's Python has been running on the tiny set of
    # modules symlinked into its "lib/pythonX.Y" directory.  But now we
    # can rewrite sys.path to point at the package directories of the
    # parent Python environment.

    for i in range(len(sys.path)):
        sys.path[i] = sys.path[i].replace(prefix, sys.real_prefix, 1)

    clean_sys_path = list(sys.path)  # save a copy

    # Now that the parent environment's packages are available on
    # sys.path, we are ready to invoke its own "site.py" file.  To make
    # it run correctly, we have to temporarily set sys.prefix to the
    # value that the parent environment always expects, then set it back
    # when "site.py" is done working.

    real_site_py = os.path.join(sys.path[0], 'site.py')

    sys.prefix = sys.real_prefix
    execfile(real_site_py, globals())
    sys.prefix = prefix

    # Running the parent environment's "site.py" will not only have set
    # up things like OS-specific encodings, and defined functions for us
    # like "addsitedir()" (which we will use in a moment) in our own
    # globals (since we passed "globals()" to "execfile()"), but will
    # have supplemented sys.path with all of the directories that the
    # system Python uses for site packages.  If it turns out the creator
    # of this virtual environment does not want to use system-wide site
    # packages, then we revert sys.path back to the pristine value it
    # had before we let the system "site.py" monkey with it.

    if os.path.exists(os.path.join(libpython, 'no-global-site-packages.txt')):
        sys.path = clean_sys_path

    # Finally, we reach what is really the whole point of a virtual
    # environment: including, at the head of sys.path, the directories
    # of any and all packages installed under the virtual environment's
    # own "site-packages" directory.  We use the system Python's
    # "addsitedir()" routine to do this scanning, to make sure that
    # ".pth" files are discovered using the official logic of this
    # version of Python, and then move the newly-appended values to the
    # head of sys.path instead.

    n = len(sys.path)
    addsitedir(os.path.join(libpython, 'site-packages'))
    #sys.path = sys.path[n:] + sys.path[:n]

# Having defined the above function, we now run it.  If several virtual
# environments are stacked on top of each other, then the function gets
# re-defined anew for each of their "site.py" files that are processed;
# only the bottommost virtual environment's definition of the function
# survives.  (Which does not really matter, since we never use it again,
# but it seemed worth mentioning in case anyone ever experiments down
# here in the future.)

virtualenv_init()
