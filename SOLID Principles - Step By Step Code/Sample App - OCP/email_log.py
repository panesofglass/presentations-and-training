import sys
import socket
from email_sender import EmailSender

def main(argv):
  try:
    sender = EmailSender()
    filename = argv[0]
    sender.Filename = filename
    sender.readFile()
    sender.sendEmail()
    print "Successfully sent your message."
  except IndexError:
    print "You must specify a file to send."
  except socket.gaierror:
    print "Couldn't connect to the SMTP server."
  except TypeError:
    print "Couldn't find the specified file."

if __name__ == "__main__":
  main(sys.argv[1:])
