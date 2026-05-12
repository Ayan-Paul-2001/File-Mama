╔══════════════════════════════════════════════════════╗
║             FILE MAMA — Quick Start Guide            ║
╚══════════════════════════════════════════════════════╝

HOW TO BUILD YOUR .EXE (one-time setup):
─────────────────────────────────────────
1. Make sure Python is installed (python.org)
   ✓ Tick "Add Python to PATH" during install!

2. Double-click  BUILD_TO_EXE.bat
   (It auto-installs everything & builds the .exe)

3. Your EXE will appear in:  dist\FileMama.exe

4. Copy FileMama.exe wherever you want — done!


HOW TO USE FileMama.exe:
─────────────────────────────────
METHOD 1 (Recommended):
  • Open any folder in Windows File Explorer
  • Double-click FileMama.exe from anywhere
  → It detects your active Explorer window & organises THAT folder

METHOD 2 (Fallback):
  • Drop FileMama.exe into the folder you want to organise
  • Double-click it
  → If no Explorer window is active, it organises its own folder


WHAT IT DOES:
─────────────
  ✓ Scans all files in the target folder
  ✓ Creates category sub-folders (only if they don't exist)
  ✓ If folder already exists → reuses it (no duplicates!)
  ✓ Moves files into matching folders
  ✓ Handles name collisions: file (1).ext, file (2).ext ...
  ✓ Writes a file_mama_log.txt with full details
  ✓ Shows a preview before moving anything


CATEGORIES CREATED:
────────────────────
  Images        → jpg, png, gif, webp, heic, svg, bmp ...
  Videos        → mp4, mkv, avi, mov, webm, flv ...
  Audio         → mp3, wav, flac, aac, ogg, m4a ...
  Documents     → pdf, docx, txt, rtf, odt, md ...
  Spreadsheets  → xlsx, csv, ods, numbers ...
  Slides        → pptx, ppt, key, odp
  Archives      → zip, rar, 7z, tar, gz, iso ...
  Code          → py, js, html, css, java, cpp, sql ...
  Executables   → exe, msi, apk, jar
  Fonts         → ttf, otf, woff, woff2
  Design        → psd, ai, fig, blend, obj, stl ...
  Ebooks        → epub, mobi, azw, djvu
  Others        → anything not matched above


NOTES:
───────
  • The .exe itself is NEVER moved
  • Works best in Downloads, Desktop, project folders
  • Avoid running in C:\Program Files (needs write access)
