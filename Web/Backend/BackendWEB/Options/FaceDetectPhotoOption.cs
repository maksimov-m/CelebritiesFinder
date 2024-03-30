namespace BackendWEB.Options
{
    public class FaceDetectPhotoOption
    {
        /// <summary>
        /// Путь к исполняемомоу файлу с нейронкой
        /// </summary>
        public string ExecutingFileNamePhotoPath { get; set; }

        /// <summary>
        /// Путь к исполняемомоу файлу с нейронкой
        /// </summary>
        public string ExecutingFileNameVideoPath { get; set; }

        /// <summary>
        /// Путь куда сохраняються фото
        /// </summary>
        public string ImagePath { get; set; }

        /// <summary>
        /// Путь куда сохраняються видео
        /// </summary>
        public string VideoPath { get; set; }


    }
}
