using BackendWEB.Options;
using BackendWEB.Services.PhotoDetect.Interfaces;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using System.Text;

namespace Labs.Controllers
{
    [Route("api")]
    public class DetectController : Controller
    {
        private string SavePhotoPath { get; set; }
        private string SaveVideoPath { get; set; }
        private readonly IFaceDetectService faceDetectPhotoService;
        private readonly ILogger<DetectController> logger;
        public DetectController(
            IOptions<FaceDetectPhotoOption> options,
            IFaceDetectService serv,
            ILogger<DetectController> logger) 
        {
            this.logger = logger;
            SavePhotoPath = options.Value.ImagePath;
            SaveVideoPath = options.Value.VideoPath;
            faceDetectPhotoService = serv;
            if (SavePhotoPath != null)
                Directory.CreateDirectory(SavePhotoPath);
            if(SaveVideoPath != null)
                Directory.CreateDirectory(SaveVideoPath);
        }
        public class ResultMessage
        {
            public bool? isReady { get; set; }
            public string? data { get; set; }
            public string? message { get; set; }
        }
        [HttpPost("isReady")]
        public ResultMessage IsReady([FromQuery]Guid id)
        {
            logger.LogInformation($"#Session {HttpContext.Session.Id} IsReady {id}");
            var data = faceDetectPhotoService.Get(id);
            return new ResultMessage() { 
                isReady = data != null,
                data = data
            };
        }
        [HttpPost("sendPhoto")]
        public async Task<Guid?> Detect(IFormFile file)
        {
            logger.LogInformation($"#Session {HttpContext.Session.Id} Detect");
            if (file == null) return null;
            Guid? id = Guid.NewGuid();
            StringBuilder pathBuilder = new StringBuilder();
            if(Path.GetExtension(file.FileName).Contains(".mp4"))
                pathBuilder.Append(SaveVideoPath);
            else
                pathBuilder.Append(SavePhotoPath);
            pathBuilder.Append(HttpContext.Session.Id);
            pathBuilder.Append(id.ToString());
            pathBuilder.Append(Path.GetExtension(file.FileName));
            string path = pathBuilder.ToString();
            // Сохраняем файл
            using (var fileStream = new FileStream(path, FileMode.OpenOrCreate))
                file.CopyTo(fileStream);

            logger.LogInformation($"#Session {HttpContext.Session.Id} Detect Сохранение файла в{path}");

            Task.Factory.StartNew(async () => {
                // Строим путь до нужной нам фотографии
                if (HttpContext.Session.Get("IK") != null)
                {
                    id = await faceDetectPhotoService.DetectAsync(path, id.Value);
                    HttpContext.Session?.Set("IK", id.Value.ToByteArray());
                }
                else
                {
                    id = await faceDetectPhotoService.DetectAsync(path, id.Value);
                    if (id.HasValue)
                        HttpContext.Session.Set("IK", id.Value.ToByteArray());
                }
                logger.LogInformation($"#Session {HttpContext.Session.Id} Detect Сохранение файла в{id}");

            }).ConfigureAwait(false);
            
            return id;
        }
        private void RemoveFile(Guid? id)
        {
            if (id.HasValue)
                return;
            string path = "./images/" + id.ToString() + ".jpg";
            if (Path.Exists(path))
            {
                System.IO.File.Delete(path);
            }
        }
    }
}
