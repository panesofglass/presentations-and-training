import sys
import os.path
import socket
import mailer

def main(argv):
  try:
    filepath = argv[0]
  except IndexError:
    print "You must specify a file to send."

  # Test to ensure the file is valid.
  if not (os.path.exists(filepath) and os.path.isfile(filepath)):
    print "Couldn't find the specified file."
    return

  # Create the message.
  message = mailer.Message(From="system@example.com",
			   To="admin@example.com",
			   Subject="Log file")
  message.Body = open(filepath, "rb").read()

  try:
    # Connect to the mail server and send the message.
    sender = mailer.Mailer('mail.example.com')
    sender.send(message)
    
    print "Successfully sent your message."
  except socket.gaierror:
    print "Couldn't connect to the SMTP server."

if __name__ == "__main__":
  main(sys.argv[1:])
