namespace SOLID.SampleApp
{
    public interface IEmailSender
    {
        void SendEmail(IMessageInfoRetriever messageInfoRetriever);
    }
}