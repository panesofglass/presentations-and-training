namespace SOLID.SampleApp
{
    public class ProcessingService
    {
    
        private readonly IEmailSender _emailSender;
        private readonly IMessageInfoRetriever _messageInfoRetriever;

        // The IMessageInfoRetriever could be passed to the emailSender if the emailSender were not a singleton.
        public ProcessingService(IEmailSender emailSender, IMessageInfoRetriever messageInfoRetriever)
        {
            _emailSender = emailSender;
            _messageInfoRetriever = messageInfoRetriever;
        }

        public string SendMessage()
        {
            string messageBody = _messageInfoRetriever.GetMessageBody();
            _emailSender.SendEmail(messageBody);
            return "Send Email With Body: " + messageBody;
        }
        
    }

    public static class IEmailSenderExtensions
    {
        public static string SendMessage(this IEmailSender emailSender, IMessageInfoRetriever messageInfoRetriever)
        {
            string messageBody = messageInfoRetriever.GetMessageBody();
            emailSender.SendEmail(messageBody);
            return "Send Email With Body: " + messageBody;
        }
    }
}
