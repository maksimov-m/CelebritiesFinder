using BackendWEB.Options;
using BackendWEB.Repositories;
using BackendWEB.Services.PhotoDetect;
using BackendWEB.Services.PhotoDetect.Interfaces;

namespace BackendWEB.Extensions
{
    public static class FaceDetectPhotoExtension
    {
        public static IServiceCollection AddFaceDetectPhotoExtension(this IServiceCollection services, IConfiguration configuration)
        {
            var config = configuration
                .GetSection("FaceDetectPhotoOption")
                .Get<FaceDetectPhotoOption>();
            services.AddSingleton<IDetectionRepository, SimpleDetectionRepository>();
            services.Configure<FaceDetectPhotoOption>(x => {
                x.ExecutingFileNamePhotoPath = config.ExecutingFileNamePhotoPath;
                x.ExecutingFileNameVideoPath = config.ExecutingFileNameVideoPath;
                x.ImagePath = config.ImagePath;
                x.VideoPath = config.VideoPath;
                
            });
            services.AddSingleton<IFaceDetectService, FaceDetectService>();
            return services;
        }
    }
}
