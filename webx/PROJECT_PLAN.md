# WebX Project Plan

Goal: Ship an MVP browser "WebX" with tabs, address bar, bookmarks, history, incognito mode, DevTools toggle and basic settings.

Architecture (MVP):
- WebView2 WPF (native Windows): C# .NET WPF host uses Microsoft.Web.WebView2 control. Handles tabs via TabControl, persisted bookmarks/history (SQLite or JSON), settings file (JSON).
- Electron (alternate): Electron main process manages BrowserWindows/BrowserViews. Renderer uses a small UI (vanilla JS/React later).

MVP tasks (2-3 week sprint):
1. Project scaffolding (this commit) — create directories, READMEs, minimal runnable shells (1 day).
2. WebView2: implement single-window with address bar, navigation buttons, and one tab (2 days).
3. Tabs: add TabControl, create/close/switch tabs (2 days).
4. Bookmarks & History: simple JSON storage, UI to add/remove/list (2 days).
5. Settings & Incognito: homepage, search engine, and incognito mode (2 days).
6. Packaging & Installer: MSIX or NSIS build (2 days).
7. Electron parity (parallel): scaffold then implement core features (4–6 days).

Milestones & timeline (estimates):
- Week 1: scaffolding + single-window WebView2 navigation + basic Electron starter.
- Week 2: tabs, bookmarks/history, settings, incognito.
- Week 3: packaging, polish, tests, docs.

Risks & notes:
- WebView2 runtime requirement on end-user machines (Edge WebView2 Runtime). Consider evergreen distribution or bootstrapper.
- Electron increases bundle size and memory usage.

Next steps I took: created this scaffold and will add minimal runnable example files for WebView2 and Electron in feature/webx-mvp branch.
