using Microsoft.Web.WebView2.Core;
using System;
using System.Windows;
using System.Windows.Input;

namespace WebX
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            InitializeAsync();
        }

        async void InitializeAsync()
        {
            await WebView.EnsureCoreWebView2Async();
            WebView.CoreWebView2.NavigationCompleted += CoreWebView2_NavigationCompleted;
            AddressBar.Text = "https://www.bing.com";
            WebView.Source = new Uri(AddressBar.Text);
        }

        private void CoreWebView2_NavigationCompleted(object? sender, CoreWebView2NavigationCompletedEventArgs e)
        {
            ForwardButton.IsEnabled = WebView.CoreWebView2.CanGoForward;
            BackButton.IsEnabled = WebView.CoreWebView2.CanGoBack;
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            if (WebView.CoreWebView2.CanGoBack) WebView.CoreWebView2.GoBack();
        }

        private void ForwardButton_Click(object sender, RoutedEventArgs e)
        {
            if (WebView.CoreWebView2.CanGoForward) WebView.CoreWebView2.GoForward();
        }

        private void ReloadButton_Click(object sender, RoutedEventArgs e)
        {
            WebView.Reload();
        }

        private void GoButton_Click(object sender, RoutedEventArgs e)
        {
            Navigate(AddressBar.Text);
        }

        private void AddressBar_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter) Navigate(AddressBar.Text);
        }

        private void Navigate(string text)
        {
            if (!text.StartsWith("http", StringComparison.OrdinalIgnoreCase)) text = "https://" + text;
            try
            {
                WebView.Source = new Uri(text);
            }
            catch { }
        }
    }
}
