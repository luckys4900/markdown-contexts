@echo off
chcp 65001 >nul
cd /d "C:\Users\user\Desktop\cursor\context"

echo Organizing MD files...
python context_organizer.py

echo.
echo Rebuilding vector index...
cd pipeline
python -c "from embedding_store import store; store.rebuild_index(Path('..'))"
cd ..

echo.
echo Checking git status...
git status

echo.
echo Adding files...
git add .

echo.
echo Committing changes...
git commit -m "Update context: %date% %time%"

echo.
echo Pushing to GitHub...
git push

echo.
echo Done!
pause
