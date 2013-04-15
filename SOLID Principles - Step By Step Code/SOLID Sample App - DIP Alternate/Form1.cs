using System;
using System.Windows.Forms;

namespace SOLID.SampleApp
{

    public partial class Form1 : Form
    {
    
        private string _fileName;
        private IEmailSender _emailSender;

        public Form1()
        {
            InitializeComponent();
            _emailSender = new EmailSender();
        }

        private void Send_Click(object sender, EventArgs e)
        {
            try
            {
                Output.Text = string.Empty;

                FileReaderService fileReaderService = new FileReaderService(_fileName);
                fileReaderService.RegisterFormatReader(new XmlFormatReader());
                fileReaderService.RegisterDefaultFormatReader(new FlatFileFormatReader());

                _emailSender.SendEmail(fileReaderService);

                Output.Text = "Sent using file reader service.";
            }
            catch (Exception ex)
            {
                Output.Text = ex.ToString();
            }
        }

        private void SendFromDatabase_Click(object sender, EventArgs e)
        {
            try
            {
                Output.Text = string.Empty;
            
                IMessageInfoRetriever databaseReaderService = new DatabaseReaderService("server=foo; database=bar;");

                _emailSender.SendEmail(databaseReaderService);

                Output.Text = "Sent using database reader service";
            }
            catch (Exception ex)
            {
                Output.Text = ex.ToString();
            }
        }

        private void FindFile_Click(object sender, EventArgs e)
        {
            try
            {
                Output.Text = string.Empty;
                OpenFileDialog dlg = new OpenFileDialog();
                dlg.CheckFileExists = true;
                dlg.CheckPathExists = true;
                dlg.Filter = "Text Files (*.txt)|*.txt|XML Files (*.xml)|*.xml";
                if (dlg.ShowDialog() == DialogResult.OK)
                {
                    _fileName = dlg.FileName;
                    SelectedFile.Text = _fileName;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }
    }
    
}