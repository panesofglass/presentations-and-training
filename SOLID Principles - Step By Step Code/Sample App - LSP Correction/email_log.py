import sys
import socket
from email_sender import EmailSender

def main(argv):
  try:
    sender = EmailSender()
    filename = argv[0]
    sender.Filename = filename
    sender.readfile()
    # sender.readdatabase()
    # if this were a legit app, we'd either have a gui
    # with a button for reading from a file or database,
    # or we'd accept args from the command line.
    sender.sendemail()
    print "Successfully sent your message."
  except IndexError:
    print "You must specify a file to send."
  except socket.gaierror:
    print "Couldn't connect to the SMTP server."
  except TypeError:
    print "Couldn't find the specified file."

if __name__ == "__main__":
  main(sys.argv[1:])
