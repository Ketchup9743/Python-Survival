using System;
using System.Diagnostics;
using System.IO;
using System.Windows;
using System.Windows.Input;

namespace GameLoader
{
    public partial class MainWindow : Window
    {
        private Process? _pythonProcess;
        private StreamWriter? _pythonInput;
        private bool _isGameRunning = false;

        public MainWindow()
        {
            InitializeComponent();
        }

        private void TerminalInput_Loaded(object sender, RoutedEventArgs e)
        {
            TerminalInput.Focus();
        }

        private void TerminalInput_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                string input = TerminalInput.Text;
                TerminalInput.Clear();

                if (_isGameRunning)
                {
                    if (_pythonInput != null && _pythonProcess != null && !_pythonProcess.HasExited)
                    {
                        _pythonInput.WriteLine(input);
                    }
                }
                else
                {
                    string command = input.Trim();
                    if (string.IsNullOrEmpty(command)) return;

                    AppendToTerminal($"> {command}");

                    if (command.Equals("Start", StringComparison.OrdinalIgnoreCase))
                    {
                        AppendToTerminal("Locating engine binaries...\n--- GAME START ---");
                        StartTerminalGame();
                    }
                    else if (command.Equals("Clear", StringComparison.OrdinalIgnoreCase))
                    {
                        TerminalOutput.Text = "";
                    }
                    else
                    {
                        AppendToTerminal($"Error: Command '{command}' not recognized. Type 'Start' to execute game.");
                    }
                }
            }
        }

        private void StartTerminalGame()
        {
            try
            {
                string baseDir = AppDomain.CurrentDomain.BaseDirectory;
                string pythonScriptPath = Path.GetFullPath(Path.Combine(baseDir, @"..\..\..\..\Game Code\game.py"));

                if (!File.Exists(pythonScriptPath))
                {
                    AppendToTerminal($"[CRITICAL] Could not locate game file at path:\n{pythonScriptPath}");
                    return;
                }

                ProcessStartInfo start = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = $"-u \"{pythonScriptPath}\"", 
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardInput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                };

                _pythonProcess = new Process { StartInfo = start };

                _pythonProcess.OutputDataReceived += (s, e) => { if (e.Data != null) AppendToTerminal(e.Data); };
                _pythonProcess.ErrorDataReceived += (s, e) => { if (e.Data != null) AppendToTerminal($"[PYTHON ERROR] {e.Data}"); };

                _pythonProcess.Start();
                _isGameRunning = true;
                _pythonInput = _pythonProcess.StandardInput;

                _pythonProcess.BeginOutputReadLine();
                _pythonProcess.BeginErrorReadLine();

                _pythonProcess.EnableRaisingEvents = true;
                _pythonProcess.Exited += (s, e) =>
                {
                    _isGameRunning = false;
                    _pythonInput = null;
                    AppendToTerminal("\n--- GAME OVER ---\nProcess disconnected. Return code 0.");
                };
            }
            catch (Exception ex)
            {
                AppendToTerminal($"Process Binding Failure: {ex.Message}");
                _isGameRunning = false;
            }
        }

        private void AppendToTerminal(string message)
        {
            Dispatcher.BeginInvoke(new Action(() =>
            {
                TerminalOutput.Text += $"\n{message}";
                
                DependencyObject border = System.Windows.Media.VisualTreeHelper.GetChild(TerminalOutput, 0);
                if (border is System.Windows.Controls.ScrollViewer viewer)
                {
                    viewer.ScrollToEnd();
                }
            }));
        }
    }
}
