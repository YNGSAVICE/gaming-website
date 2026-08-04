using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;

namespace WebX
{
    public record Bookmark
    {
        public string Title { get; init; } = "";
        public string Url { get; init; } = "";
        public DateTime AddedAt { get; init; }
    }

    public class BookmarksManager
    {
        private readonly List<Bookmark> _bookmarks = new();
        private string GetPath()
        {
            var dir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "WebX");
            Directory.CreateDirectory(dir);
            return Path.Combine(dir, "bookmarks.json");
        }

        public IReadOnlyList<Bookmark> Bookmarks => _bookmarks.AsReadOnly();

        public async Task LoadAsync()
        {
            var path = GetPath();
            if (!File.Exists(path)) return;
            try
            {
                var s = await File.ReadAllTextAsync(path);
                var items = JsonSerializer.Deserialize<List<Bookmark>>(s);
                if (items != null)
                {
                    _bookmarks.Clear();
                    _bookmarks.AddRange(items);
                }
            }
            catch { }
        }

        public async Task SaveAsync()
        {
            var path = GetPath();
            var s = JsonSerializer.Serialize(_bookmarks, new JsonSerializerOptions { WriteIndented = true });
            await File.WriteAllTextAsync(path, s);
        }

        public void Add(Bookmark b)
        {
            _bookmarks.Add(b);
        }
    }
}
