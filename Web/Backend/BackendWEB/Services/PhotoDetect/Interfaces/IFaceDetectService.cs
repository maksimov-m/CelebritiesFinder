using System.Diagnostics;

namespace BackendWEB.Services.PhotoDetect.Interfaces
{
    public interface IFaceDetectService
    {
        public Task<Guid?> DetectAsync(string pathToFile);

        public Task<Guid?> DetectAsync(string pathToFile, Guid withid);

        public string Get(Guid guid);

        public string? Remove(Guid guid);
    }
}
