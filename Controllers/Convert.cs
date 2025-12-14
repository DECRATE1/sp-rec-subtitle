using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Microsoft.OpenApi.Any;

public class FormModel
{
    public required IFormFile Video {get; set;}
}

[ApiController]
[Route("api/[controller]")]
public class Convert: ControllerBase
{
    [HttpPost("AddSubtitle")]
    public async Task<IActionResult> Subtitle([FromForm] FormModel formData)
    {
        //Сохранение файла
        IFormFile file = formData.Video;
        Console.WriteLine(file);
        string tempDir = Path.GetTempPath();
        string path = Path.Combine(tempDir, Guid.NewGuid().ToString() + ".mp4");
        using(var streamFile = System.IO.File.Create(path))
        {
            await file.CopyToAsync(streamFile);
        }

        //Старт процесса
        var start = new ProcessStartInfo
        {
            FileName = "python",
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true
        };

        string scriptFile = "D:/Projects/sp-backend/model/sp-rec-subtitle/main.py";

        start.ArgumentList.Add(scriptFile);
        start.ArgumentList.Add(path);
        start.ArgumentList.Add("D:/Projects/sp-backend/model/");

        using var process = Process.Start(start) ?? throw new InvalidOperationException("Cannot start process");
        var outTask = process.StandardOutput.ReadToEndAsync();
        var errTask = process.StandardError.ReadToEndAsync();
        await process.WaitForExitAsync();
        var stdout = (await outTask).Trim();
        var stderr = (await errTask).Trim();
        if (process.ExitCode != 0) return StatusCode(500, $"Exit {process.ExitCode}: {stderr}");
        if (string.IsNullOrEmpty(stdout)) return StatusCode(500, "Empty output from python");
        var stream = System.IO.File.OpenRead(stdout);
        return File(stream, "video/mp4", Path.GetFileName(stdout));
    }
}