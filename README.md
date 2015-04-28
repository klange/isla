# Isla

**Isla** is an IRC bot using `irc.bot` and implementing a regex-based response architecture with automatically reloading modules.

**Isla** is loosely based on concepts from Hubot.

## Installation

This isn't a proper Python package yet, so you'll need to do some manual gruntwork:

* Set up a virtualenv and `pip install irc`.
* Write a `config.py` in the root:

    ```python
    nickserver_password = 'hunter2'
    autojoin = ['#some-channel']
    server = ('irc.freenode.net', 6667)
    ```

* Start Isla: `python isla.py`
