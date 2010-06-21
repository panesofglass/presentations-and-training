import os.path
import xml.parsers.expat
from xml.etree import ElementTree
from mailer import Mailer, Message

class FormatReader(object):
  def getmessagebody(self, fileContents):
    try:
      tree = ElementTree.fromstring(fileContents)
    except xml.parsers.expat.ExpatError:
      return fileContents
    else:
      return tree.findText("//email/body")


class EmailSender(object):
  def __init__(self):
    self._messagebody = None
    self._filename = None

  def _getmessagebody(self):
    return self._messagebody

  def _setmessagebody(self, messagebody):
    self._messagebody = messagebody

  MessageBody = property(_getmessagebody, _setmessagebody,
			 doc="""The message body""")

  def _getfilename(self):
    return self._filename

  def _setfilename(self, filename):
    # Test to ensure the file is valid.
    if os.path.exists(filename) and os.path.isfile(filename):
      self._filename = filename
    else:
      self._filename = None # Should probably throw an exception.

  Filename = property(_getfilename, _setfilename,
		      doc="""The file name""")

  def readFile(self):
    fileContents = open(self.Filename).read()
    formatReader = FormatReader()
    messagebody = formatReader.getmessagebody(fileContents)

  def sendEmail(self):
    # Create the message.
    message = Message(From="system@example.com",
		     To="admin@example.com",
		     Subject="Log file",
		     Body=self.MessageBody)

    # Connect to the mail server and send the message.
    sender = Mailer('mail.example.com')
    sender.send(message)
