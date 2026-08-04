using System;
using System.Windows;
using System.Windows.Controls;

namespace WebX
{
    public partial class BookmarksWindow : Window
    {
        private readonly BookmarksManager _manager;
        public event EventHandler<string>? BookmarkActivated;

        public BookmarksWindow(BookmarksManager manager)
        {
            InitializeComponent();
            _manager = manager;
            Loaded += BookmarksWindow_Loaded;
        }

        private void BookmarksWindow_Loaded(object sender, RoutedEventArgs e)
        {
            BookmarksList.Items.Clear();
            foreach (var b in _manager.Bookmarks)
            {
                var item = new ListBoxItem { Content = b.Title + "\n" + b.Url, Tag = b.Url };
                BookmarksList.Items.Add(item);
            }
        }

        private void BookmarksList_MouseDoubleClick(object sender, System.Windows.Input.MouseButtonEventArgs e)
        {
            if (BookmarksList.SelectedItem is ListBoxItem item && item.Tag is string url)
            {
                BookmarkActivated?.Invoke(this, url);
                Close();
            }
        }
    }
}
