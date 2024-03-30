using IronPython.Runtime.Operations;
using System.Diagnostics;
using System.Reflection.Metadata.Ecma335;
using System.Runtime.ExceptionServices;
using System.Runtime.InteropServices;
using System.Text;
using static IronPython.Modules._ast;

namespace BackendWEB.Python
{
    public class PythonProcess
    {
        private string ExecutFilePath { get; set; }
        public Process? process { get; protected set; }
        public PythonProcess(string executinFilePath)
        {
            ExecutFilePath = executinFilePath;
        }

        ~PythonProcess()
        {
            process?.Close();
        }
        public PythonProcess Create(string arguments)
        {
            if (process != null)
            {
                return this;
            }
            ProcessStartInfo start = new ProcessStartInfo();
            Encoding.UTF8.GetString(arguments.MakeByteArray());
            string argument = " -f " + arguments;
            start.Arguments = ExecutFilePath + argument;
            start.FileName = "python";
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            start.RedirectStandardInput = true;
            start.CreateNoWindow = false;
            start.StandardInputEncoding = Console.InputEncoding;
            process = Process.Start(start);
            return this;
        }
        public async Task<string?> ExecTask(string input)
        {
            if (process == null)
                throw new ArgumentNullException("Процесс ещё не был создан");
            
            process.OutputDataReceived += (s, e) => { 
                Console.WriteLine("From python" + (!string.IsNullOrEmpty(e.Data) ? e.Data : string.Empty));
            };

            var clock = DateTime.Now;
            string? output = string.Empty;
            while (DateTime.Now - clock < TimeSpan.FromSeconds(300))
            {
                output = process.StandardOutput.ReadLine();
                Console.WriteLine(output);
                if (string.IsNullOrEmpty(output) || output.Contains("end:"))
                {
                    break;
                }
            }
            if (!string.IsNullOrEmpty(output) && output.Contains("end:")) {
                output = output.Replace("end:", "");
                output.Trim();
            }
            Console.WriteLine(output);
            return output;
        }

        
    }
}
