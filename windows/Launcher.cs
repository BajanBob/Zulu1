// Zulu 1 Tutor for Windows: a small program that carries the tutor page inside it.
// When run, it copies the page to the user's AppData folder (always the same place, so stars
// and words are kept) and opens it in Microsoft Edge as its own app window.
// Built on GitHub (see .github/workflows/publish-website.yml) with the .NET Framework compiler.
using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Windows.Forms;

static class ZuluTutor
{
    const string Edition = "EDITION_NAME";   // replaced when built: Shakai or Bubba

    [STAThread]
    static void Main()
    {
        try
        {
            string dir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Zulu1Tutor", Edition);
            Directory.CreateDirectory(dir);
            string page = Path.Combine(dir, "index.html");
            using (Stream src = Assembly.GetExecutingAssembly().GetManifestResourceStream("tutor.html"))
            using (FileStream dst = File.Create(page))
            {
                src.CopyTo(dst);
            }
            string url = new Uri(page).AbsoluteUri;
            try
            {
                ProcessStartInfo edge = new ProcessStartInfo("msedge", "--app=\"" + url + "\" --window-size=1100,850");
                edge.UseShellExecute = true;
                Process.Start(edge);
            }
            catch
            {
                // No Edge: open the page in the default browser instead.
                ProcessStartInfo any = new ProcessStartInfo(page);
                any.UseShellExecute = true;
                Process.Start(any);
            }
        }
        catch (Exception e)
        {
            MessageBox.Show("The tutor could not start: " + e.Message, "Zulu 1 Tutor", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }
    }
}
