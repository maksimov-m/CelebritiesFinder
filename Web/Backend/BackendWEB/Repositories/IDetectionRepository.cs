namespace BackendWEB.Repositories
{
    /// <summary>
    /// Интрефейс описывающий элементы, сохранаяющие значения 
    /// </summary>
    public interface IDetectionRepository
    {
        public string? Get(Guid id);

        public bool Set(Guid key, string name);

        public string? Remove(Guid key);
    }
}
