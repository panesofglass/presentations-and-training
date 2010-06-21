import os.path
import xml.parsers.expat
from xml.etree import ElementTree
from mailer import Mailer, Message

class IFileFormatReader(object):
  """
  This is the File Format Reader interface.

  There is some debate as to whether or not this should be done
  or if so, how it should be done. You can read some opinions at
  http://bytes.com/topic/python/answers/24317-pythonic-abstract-base-class-interface

  This interface and its implementations replace the following from the SRP version:
  class FormatReader(object):
    def getmessagebody(self, fileContents):
      try:
	tree = ElementTree.fromstring(fileContents)
      except xml.parsers.expat.ExpatError:
	return fileContents
      else:
	return tree.findtext("email/body")

  This interface cannot be created or used.

  >>> reader = IFileFormatReader()
  Traceback (most recent call last):
      ...
  NotImplementedError
  """

  def __init__(self):
    if self.__class__ is IFileFormatReader:
      raise NotImplementedError

  def canhandle(self, filecontents):
    raise NotImplementedError

  def getmessagebody(self, filecontents):
    raise NotImplementedError


class FlatFileFormatReader(IFileFormatReader):
  """
  This is the File Format Reader for flat files.
  """
  
  def canhandle(self, filecontents):
    """
    >>> FlatFileFormatReader().canhandle("some file contents")
    True
    """
    return True

  def getmessagebody(self, filecontents):
    """
    >>> FlatFileFormatReader().getmessagebody("some file contents")
    'some file contents'
    """
    return filecontents


class XmlFileFormatReader(IFileFormatReader):
  """
  This is the File Format Reader for xml files.
  """
  
  def canhandle(self, filecontents):
    """
    >>> XmlFileFormatReader().canhandle("blah blah blah")
    False
    >>> XmlFileFormatReader().canhandle("<test><text>Hello World!</text></test>")
    True
    """
    try:
      ElementTree.fromstring(filecontents)
    except xml.parsers.expat.ExpatError:
      return False
    else:
      return True
    
  def getmessagebody(self, filecontents):
    """
    >>> XmlFileFormatReader().getmessagebody("blah blah blah")
    Traceback (most recent call last):
	...
    ExpatError: syntax error: line 1, column 0
    >>> XmlFileFormatReader().getmessagebody("<test><text>Hello World!</text></test>")
    >>> XmlFileFormatReader().getmessagebody("<email><body>Hello World!</body></email>")
    >>> XmlFileFormatReader().getmessagebody("<data><email><body>Hello World!</body></email></data>")
    'Hello World!'
    """
    xmldoc = ElementTree.fromstring(filecontents)
    return xmldoc.findtext("email/body")


class IMessageInfoRetriever(object):
  def __init__(self):
    raise NotImplementedError
  def getmessagebody(self):
    raise NotImplementedError


class FileReaderService(IMessageInfoRetriever):
  def __init__(self, filename):
    self._filename = filename
    self._formatreaders = []

  def register(self, fileformatreader):
    """
    Adds a reader to the collection.

    Note that no tests are needed as then we would be testing Python, not our code.
    """
    self._formatreaders.append(fileformatreader)

  def getmessagebody(self):
    """
    Returns the result of the first reader to return a response.
    >>> service = FileReaderService("./Files/log.xml")
    >>> service.register(XmlFileFormatReader())
    >>> service.getmessagebody()
    'Hello World!'
    >>> service = FileReaderService("./Files/log.txt")
    >>> service.register(FlatFileFormatReader())
    >>> service.getmessagebody()
    'Hello world!\\n'
    """
    filecontents = self.__getfilecontents(self._filename)
    return self.__parsefilecontents(filecontents)

  def __getfilecontents(self, filename):
    file = open(filename)
    filecontents = file.read()
    file.close()
    return filecontents

  def __parsefilecontents(self, filecontents):
    messagebody = ''
    for r in self._formatreaders:
      if r.canhandle(filecontents):
	messagebody = r.getmessagebody(filecontents)
	break
    return messagebody


class DatabaseReaderService(IMessageInfoRetriever):
  """ A database reader service """
  def __init__(self, connectionstring):
    self._connectionstring = connectionstring

  def getmessagebody(self):
    """
    >>> DatabaseReaderService('server=myserver;database=data').getmessagebody()
    'Pretend this came from a database!'
    """
    # Connect to a database.
    # Get the log information.
    return 'Pretend this came from a database!'


class IEmailSender(object):
  def __init__(self):
    raise NotImplementedError
  def sendemail(self, messagebody):
    raise NotImplementedError

class EmailSender(IEmailSender):
  def sendemail(self, messagebody):
    # Create the message.
    message = Message(From="system@example.com",
		     To="admin@example.com",
		     Subject="Log file",
		     Body=messagebody)

    # Connect to the mail server and send the message.
    sender = Mailer('mail.example.com')
    sender.send(message)


class ProcessingService(object):
  def __init__(self, emailsender, messageinforetriever):
    self._emailsender = emailsender
    self._messageinforetriever = messageinforetriever

  def sendmessage(self):
    messagebody = self._messageinforetriever.getmessagebody()
    self._emailsender.sendemail(messagebody)
    return "Sent email with body: " + messagebody


if __name__ == "__main__":
  import doctest
  doctest.testmod()
