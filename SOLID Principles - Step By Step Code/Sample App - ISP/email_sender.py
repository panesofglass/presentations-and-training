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


class FileReaderService(object):
  def __init__(self):
    self._formatreaders = []

  def register(self, fileformatreader):
    """
    Adds a reader to the collection.

    Note that no tests are needed as then we would be testing Python, not our code.
    """
    self._formatreaders.append(fileformatreader)

  def getmessagebodyfromfile(self, filename):
    """
    Returns the result of the first reader to return a response.
    >>> service = FileReaderService()
    >>> service.register(XmlFileFormatReader())
    >>> service.register(FlatFileFormatReader())
    >>> service.getmessagebodyfromfile("./Files/log.xml")
    'Hello World!'
    >>> service.getmessagebodyfromfile("./Files/log.txt")
    'Hello world!\\n'
    """
    filecontents = self.__getfilecontents(filename)
    return self.__getmessagebody(filecontents)

  def __getmessagebody(self, filecontents):
    messagebody = ''
    for r in self._formatreaders:
      if r.canhandle(filecontents):
	messagebody = r.getmessagebody(filecontents)
	break
    return messagebody

  def __getfilecontents(self, filename):
    file = open(filename)
    filecontents = file.read()
    file.close()
    return filecontents


class DatabaseReaderService(object):
  """ A database reader service """

  def getmessagebody(self):
    """
    >>> DatabaseReaderService().getmessagebody()
    'Pretend this came from a database!'
    """
    # Connect to a database.
    # Get the log information.
    return 'Pretend this came from a database!'


class EmailSender(object):
  def sendemail(self, messagebody):
    # Create the message.
    message = Message(From="system@example.com",
		     To="admin@example.com",
		     Subject="Log file",
		     Body=messagebody)

    # Connect to the mail server and send the message.
    sender = Mailer('mail.example.com')
    sender.send(message)


if __name__ == "__main__":
  import doctest
  doctest.testmod()
