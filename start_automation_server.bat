@echo off
echo 🤖 Trading Project 002 - Automation Server
echo ================================================
echo.

REM בדוק אם Python מותקן
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python לא מותקן במערכת
    echo 💡 התקן Python מ: https://python.org
    pause
    exit /b 1
)

echo ✅ Python זמין
echo.

REM עבור לתיקיית הפרויקט
cd /d "%~dp0"

echo 📁 תיקייה נוכחית: %CD%
echo.

REM בדוק אם יש תיקיית automation
if not exist "automation" (
    echo ❌ תיקיית automation לא נמצאה
    echo 💡 ודא שאתה בתיקייה הנכונה
    pause
    exit /b 1
)

echo 🔍 בודק ספריות Python נדרשות...

REM בדוק requests
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ מתקין ספריית requests...
    pip install requests
)

REM בדוק markdown
python -c "import markdown" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ מתקין ספריית markdown...
    pip install markdown
)

echo ✅ כל הספריות זמינות
echo.

echo 🚀 מפעיל Automation Server...
echo.
echo 💡 לעצירת השרת - לחץ Ctrl+C
echo 📋 השרת יופעל על http://localhost:8080
echo 🔗 הדשבורד יוכל להשתמש בכפתורי העדכון
echo.

REM הפעל השרת
python automation/automation_server.py

echo.
echo 🛑 השרת הופסק
pause