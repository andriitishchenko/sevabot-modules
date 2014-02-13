#!/sevabot
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from sevabot.bot.stateful import StatefulSkypeHandler
from sevabot.utils import ensure_unicode, get_chat_id

import re
import logging
# import requests
from bs4 import BeautifulSoup
import urllib2
import logging

logger = logging.getLogger("url_title")
logger.setLevel(logging.INFO)
# logger.setLevel(logging.INFO)
logger.debug("Url Title module level load import")

class Tess(StatefulSkypeHandler):
    """
    Base class for stateful handlers.

    All exceptions slip through are caught and logged.
    """

    def init(self, sevabot):
        """
        Set-up our state. This is called every time module is (re)loaded.

        You can get Skype4Py instance via ``sevabot.getSkype()``.

        :param sevabot: Handle to Sevabot instance
        """
        self.sevabot = sevabot

    def handle_message(self, msg, status):

     
        """Override this method to have a customized handler for each Skype message.

        :param msg: ChatMessage instance https://github.com/awahlig/skype4py/blob/master/Skype4Py/chat.py#L409

        :param status: -

        :return: True if the message was handled and should not be further processed
        """

        if status == 'SENT':
           # Avoid infinite loop caused by self-reproducing code
           return True

        test = None
        body = ensure_unicode(msg.Body)

        # Parse the chat message to commanding part and arguments
        # words = body.split('(\s+|\n)')
        words = re.split('(\s+|\n)', body, flags=re.M)
        lower = body.lower()
        a = re.compile(r'''http[s]?://''')

        if len(words) == 0:
            return False

        # if len(words) >= 2:
        hasLink = a.search(lower)
        if hasLink != None:
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', lower)
            for item in urls:
                test = self.get_link_title(item)
                if test != None:
                    msg.Chat.SendMessage("%s" % (test))

        return False

    def shutdown(self):
        """ Called when the module is reloaded.

        In ``shutdown()`` you must

        * Stop all created threads

        * Unregister all event handlers

        ..note ::

            We do *not* guaranteed to be call when Sevabot process shutdowns as
            the process may terminate with SIGKILL.

        """

    def register_callback(self, skype, event, callback):
        """
        Register any callable as a callback for a skype event.

        Thin wrapper for RegisterEventHandler https://github.com/awahlig/skype4py/blob/master/Skype4Py/utils.py

        :param skype: Skype4Py instance

        :param event: Same as Event

        :param callback: Same as Target

        :return: Same as RegisterEventHandler
        """

        return skype.RegisterEventHandler(event, callback)

    def unregister_callback(self, skype, event, callback):
        """
        Unregister a callback previously registered with register_callback.

        Thin wrapper for UnregisterEventHandler https://github.com/awahlig/skype4py/blob/master/Skype4Py/utils.py

        :param skype: Skype4Py instance

        :param event: Same as Event

        :param callback: Same as Target

        :return: Same as UnregisterEventHandler
        """

        return skype.UnregisterEventHandler(event, callback)

    # @staticmethod
    def get_link_title(e,url):
        try:
            logger.debug("call");
            content = urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)
            return soup.title.string        
        except:
            return None



# Export the instance to Sevabot
sevabot_handler = Tess()

__all__ = ['sevabot_handler']