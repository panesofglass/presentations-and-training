import sys
import socket
from email_sender import EmailSender

def sendfromfile(filename):
  filereaderservice = FileReaderService()
  filereaderservice.register(XmlFileFormatReader())
  filereaderservice.register(FlatFileFormatReader())

  messagebody = formatreaderservice.getmessagebodyfromfile(filename)
  
  sender = EmailSender()
  sender.sendemail(messagebody)
  print "Successfully sent your message from a file."

def sendfromdatabase():
  service = DatabaseReaderService()

  messagebody = service.getmessagebody()

  sender = EmailSender()
  sender.sendemail(messagebody)
  print "Successfully sent your message from the database."

def findfile(self, filename):
  # Test to ensure the file is valid.
  if os.path.exists(filename) and os.path.isfile(filename):
    return filename
  else:
    return None # Should probably throw an exception.

def main(argv):
  try:
    filename = findfile(argv[0])
    sendfromfile(filename)
    # sendfromdatabase()
    # if this were a legit app, we'd either have a gui
    # with a button for reading from a file or database,
    # or we'd accept args from the command line.
  except IndexError:
    print "You must specify a file to send."
  except socket.gaierror:
    print "Couldn't connect to the SMTP server."
  except TypeError:
    print "Couldn't find the specified file."

if __name__ == "__main__":
  main(sys.argv[1:])
