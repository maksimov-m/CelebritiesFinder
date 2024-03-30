using BackendWEB.Options;
using BackendWEB.Python;
using BackendWEB.Repositories;
using BackendWEB.Services.PhotoDetect.Interfaces;
using IronPython.Hosting;
using IronPython.Runtime.Operations;
using Microsoft.Extensions.Options;
using System.Diagnostics;
using System.Text.Json;
using static IronPython.Modules._ast;

namespace BackendWEB.Services.PhotoDetect
{
    public class FaceDetectService : IFaceDetectService
    {
        private string ExecutingFileNamePhotoPath { get; set; }
        private string ExecutingFileNameVideoPath { get; set; }
        private IDetectionRepository detectionRepository { get; set; }
        private ILogger<FaceDetectService> logger { get; set; }
        public FaceDetectService(IOptions<FaceDetectPhotoOption> config,
            IDetectionRepository detectionRepository,
            ILogger<FaceDetectService> logger)
        {
            this.logger = logger;
            ExecutingFileNamePhotoPath = config.Value.ExecutingFileNamePhotoPath;
            ExecutingFileNameVideoPath = config.Value.ExecutingFileNameVideoPath;
            this.detectionRepository = detectionRepository;
        }
        public async Task<Guid?> DetectAsync(string pathToFile)
        {
            return await DetectAsync(pathToFile, Guid.NewGuid());
        }
        public async Task<Guid?> DetectAsync(string pathToFile, Guid withid)
        {
            logger.LogInformation($"#Function Detect path: {pathToFile} {withid}");
            var executingFileNamePath = this.ExecutingFileNamePhotoPath;
            if (Path.GetExtension(pathToFile).Contains( ".mp4"))
            {
                executingFileNamePath = this.ExecutingFileNameVideoPath;
            }
            logger.LogInformation($"#Function ExecFile: {executingFileNamePath} {pathToFile}");
            PythonProcess process = new PythonProcess(executingFileNamePath);
            process.Create(pathToFile);
            string? str = await process.ExecTask(pathToFile);
            if (string.IsNullOrWhiteSpace(str))
                return null;
            var id = withid;
            detectionRepository.Set(id, str);
            return id;
        }
        public string? Get(Guid guid)
        {
            logger.LogInformation($"#Function Get {guid}");
            return detectionRepository.Get(guid);
        }
        public string? Remove(Guid guid)
        {
            logger.LogInformation($"#Function Remove {guid}");
            return detectionRepository.Remove(guid);
        }
    }
}
