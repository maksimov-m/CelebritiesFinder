using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace BackendWEB.wwwroot.home
{
    [IgnoreAntiforgeryToken]
    public class FaceDetectModel : PageModel
    {
        public void OnGet()
        {
        }

        
        public void OnPost(IFormFile file)
        {
            Console.WriteLine("Работает");
        }


    }
}
