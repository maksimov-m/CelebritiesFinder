using Microsoft.Scripting.Interpreter;
using System.Collections.Concurrent;

namespace BackendWEB.Repositories
{
    public class SimpleDetectionRepository : IDetectionRepository
    {
        ConcurrentDictionary<Guid, string> detectedValues = new();
        public SimpleDetectionRepository() 
        {
        }

        public string? Get(Guid id)
        {
            string? input = null;
            detectedValues.TryGetValue(id, out input);
            return input;
        }

        public bool Set(Guid key, string name)
        {
            return detectedValues.TryAdd(key, name);
        }

        public string? Remove(Guid key)
        {
            string? input = null;
            detectedValues.TryRemove(key, out input);
            return input;
        }
    }
}
