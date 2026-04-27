@echo off
chcp 65001 >nul
cd /d "C:\Users\user\Desktop\cursor\context"

echo ================================================================================
echo                          Context Management System
echo ================================================================================
echo.
echo Step 1: Organizing MD files...
echo ================================================================================
python context_organizer.py

echo.
echo ================================================================================
echo Step 2: Rebuilding vector index...
echo ================================================================================
cd pipeline
python -c "from embedding_store import store; count = store.rebuild_index(Path('..')); print(f'Indexed {count} documents')"
cd ..

echo.
echo ================================================================================
echo Step 3: Git synchronization...
echo ================================================================================
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
echo ================================================================================
echo                           All Steps Completed!
echo ================================================================================
echo.
pause
