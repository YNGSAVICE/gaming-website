using Microsoft.Web.WebView2.Core;
using Microsoft.Web.WebView2.Wpf;
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace WebX
{
    public partial class MainWindow : Window
    {
        private readonly Dictionary<TabItem, WebView2> _tabMap = new();
        private readonly BookmarksManager _bookmarks = new();

        public MainWindow()
        {
            InitializeComponent();
            Loaded += MainWindow_Loaded;
        }

        private async void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            await _bookmarks.LoadAsync();
            await NewTab("https://www.bing.com");
        }

        private async Task NewTab(string? url = null)
        {
            var tab = new TabItem { Header = "New Tab" };
            var webview = new WebView2();
            tab.Content = webview;
            TabControl.Items.Add(tab);
            TabControl.SelectedItem = tab;
            _tabMap[tab] = webview;

            await webview.EnsureCoreWebView2Async();
            webview.CoreWebView2.NavigationCompleted += CoreWebView2_NavigationCompleted;

            if (!string.IsNullOrEmpty(url)) NavigateTo(webview, url);
        }

        private void CloseCurrentTab()
        {
            if (TabControl.SelectedItem is TabItem tab)
            {
                TabControl.Items.Remove(tab);
                _tabMap.Remove(tab);
            }
        }

        private void NavigateTo(WebView2 webview, string text)
        {
            if (!text.StartsWith("http", StringComparison.OrdinalIgnoreCase)) text = "https://" + text;
            try
            {
                webview.Source = new Uri(text);
            }
            catch { }
        }

        private WebView2? CurrentWebView()
        {
            if (TabControl.SelectedItem is TabItem tab && _tabMap.TryGetValue(tab, out var wv)) return wv;
            return null;
        }

        private void CoreWebView2_NavigationCompleted(object? sender, CoreWebView2NavigationCompletedEventArgs e)
        {
            var wv = sender as CoreWebView2;
            // Update address bar and buttons for current tab
            var current = CurrentWebView();
            if (current != null && current.CoreWebView2 != null)
            {
                AddressBar.Text = current.CoreWebView2.Source;
                BackButton.IsEnabled = current.CoreWebView2.CanGoBack;
                ForwardButton.IsEnabled = current.CoreWebView2.CanGoForward;
                if (TabControl.SelectedItem is TabItem tab)
                    tab.Header = current.CoreWebView2.DocumentTitle ?? current.CoreWebView2.Source;

                // log history (append)
                _ = HistoryLogger.LogAsync(current.CoreWebView2.Source, current.CoreWebView2.DocumentTitle);
            }
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            var current = CurrentWebView();
            if (current?.CoreWebView2 != null && current.CoreWebView2.CanGoBack) current.CoreWebView2.GoBack();
        }

        private void ForwardButton_Click(object sender, RoutedEventArgs e)
        {
            var current = CurrentWebView();
            if (current?.CoreWebView2 != null && current.CoreWebView2.CanGoForward) current.CoreWebView2.GoForward();
        }

        private void ReloadButton_Click(object sender, RoutedEventArgs e)
        {
            CurrentWebView()?.Reload();
        }

        private async void GoButton_Click(object sender, RoutedEventArgs e)
        {
            var current = CurrentWebView();
            if (current != null) NavigateTo(current, AddressBar.Text);
        }

        private void AddressBar_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter) _ = GoButton_ClickAsync();
        }

        private Task GoButton_ClickAsync()
        {
            var current = CurrentWebView();
            if (current != null) NavigateTo(current, AddressBar.Text);
            return Task.CompletedTask;
        }

        private async void NewTabButton_Click(object sender, RoutedEventArgs e)
        {
            await NewTab("https://www.bing.com");
        }

        private void CloseTabButton_Click(object sender, RoutedEventArgs e)
        {
            CloseCurrentTab();
        }

        private async void BookmarkButton_Click(object sender, RoutedEventArgs e)
        {
            var current = CurrentWebView();
            if (current?.CoreWebView2 != null)
            {
                var url = current.CoreWebView2.Source;
                var title = current.CoreWebView2.DocumentTitle ?? url;
                _bookmarks.Add(new Bookmark { Title = title, Url = url, AddedAt = DateTime.UtcNow });
                await _bookmarks.SaveAsync();
                MessageBox.Show($"Bookmarked: {title}", "WebX");
            }
        }

        private void ShowBookmarksButton_Click(object sender, RoutedEventArgs e)
        {
            var win = new BookmarksWindow(_bookmarks);
            win.BookmarkActivated += (s, url) =>
            {
                var current = CurrentWebView();
                if (current != null) NavigateTo(current, url);
            };
            win.Owner = this;
            win.Show();
        }
    }
}
