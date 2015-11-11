# This file is a part of fedmsg-notify.
#
# Authors: Elan Ruusamäe <glen@pld-linux.org>

import logging

log = logging.getLogger('moksha.hub')

def get_installed_packages():
    """Retrieve the packages installed on the system"""
    return []

def get_user_packages(usernames):
    """Retrieve the packages maintained by `usernames`"""
    return []

def get_reported_bugs():
    """
    Not implemented on PLD Linux, just return empty set
    """

    return set()
