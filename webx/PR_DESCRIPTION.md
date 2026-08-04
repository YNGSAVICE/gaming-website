Title: WebX MVP — WebView2 + Electron starters, tabs & bookmarks

This PR adds scaffolding and a first-pass implementation of the WebX browser MVP. It contains two starter apps:

- webview2-wpf: native Windows WPF app using Microsoft Edge WebView2. Includes tabbing, address bar, navigation, bookmarks (JSON persistence), and a bookmarks window.
- electron: cross-platform Electron starter with a tabbed iframe-based UI and localStorage bookmarks.

Other additions:
- PROJECT_PLAN.md with architecture, milestones, and risks.
- README and .gitignore for the webx folder.

Changes are contained within webx/ and should not affect existing site code in the repo.

Notes for reviewers:
- WebView2 requires the Edge WebView2 runtime on user machines.
- The Electron starter is a minimal prototype using iframes and is not production hardened.

Next steps after merge:
- Implement history persistence and UI.
- Add incognito mode and settings UI.
- Create packaging/installer workflows (MSIX/NSIS) and CI builds.
