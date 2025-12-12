using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public class Convert: ControllerBase
{
    [HttpGet("AddSubtitle")]
    public async Task<IActionResult> Subtitle()
    {
        var start = new ProcessStartInfo
        {
            FileName = "python",
            Arguments = "./sp-rec-model/main.py",
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true
        };

        using var process = Process.Start(start) ?? throw new InvalidOperationException("Cannot start process");
        var outTask = process.StandardOutput.ReadToEndAsync();
        var errTask = process.StandardError.ReadToEndAsync();
        await process.WaitForExitAsync();
        var stdout = (await outTask).Trim();
        var stderr = (await errTask).Trim();

        if (process.ExitCode != 0) return StatusCode(500, $"Exit {process.ExitCode}: {stderr}");
        if (string.IsNullOrEmpty(stdout)) return StatusCode(500, "Empty output from python");
        if (!System.IO.File.Exists(stdout)) return NotFound($"File not found: {stdout}");

        var stream = System.IO.File.OpenRead(stdout);
        return File(stream, "video/mp4", Path.GetFileName(stdout));
    }
}