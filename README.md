# StoryDB by Brett Kromkamp

StoryDB is a formalization of complex events with an accompanying persistence store. StoryDB is ideally
suited for things like story development and investigative journalism. With StoryDB it is straightforward
to (procedurally) create complex events and the precise relationships between events. StoryDB’s event model describes an event in terms of what is happening, when and where it is happening, who its participants are and why it is taking place.

## Install the Development Version

If you have [Git](https://git-scm.com/) installed on your system, it is possible to install the development version of StoryDB.

Before installing the development version, you may need to uninstall the standard version of StoryDB using ``pip``:

    $ pip uninstall story-db

Then do:

    $ git clone https://github.com/brettkromkamp/story-db
    $ cd story-db
    $ pip install -e .

The ``pip install -e .`` command allows you to follow the development branch as it changes by creating links in the right places and installing the command line scripts to the appropriate locations.

Then, if you want to update StoryDB at any time, in the same directory do:

    $ git pull

## How to Contribute

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork the [repository](https://github.com/brettkromkamp/story-db) on GitHub to start making your changes to the **master** branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request and bug the maintainer until it gets merged and published :)