# 🤖 מדריך מערכת העדכון האוטומטי - Trading Project 002

## 🎯 סקירה כללית

מערכת עדכון אוטומטי עם 3 כפתורים בדשבורד הראשי:
- **🗣️ עדכן שיחות** - מעדכן יומן שיחות מפעילות הטרמינל
- **📝 עדכן תיעוד** - ממיר קבצי MD ל-HTML ומעדכן file_map
- **🔗 סנכרן GitHub** - יוצר/מעדכן repository ב-GitHub

---

## 🚀 התחלה מהירה

### 1️⃣ הפעלת השרת
```bash
# לחץ כפול על הקובץ או הרץ בטרמינל:
start_automation_server.bat
```

**מה קורה:**
- השרת עולה על `http://localhost:8080`
- בודק ספריות Python נדרשות
- מתקין אוטומטית אם חסרות
- מציג הודעות סטטוס

### 2️⃣ שימוש בכפתורים
1. פתח את `project_dashboard.html` בדפדפן
2. ודא שהשרת רץ (חלון הטרמינל פתוח)
3. לחץ על הכפתורים בתיבה העליונה
4. עקב אחר ההתקדמות בהתראות

---

## 📋 תיאור מפורט של הכפתורים

### 🗣️ כפתור "עדכן שיחות"

**מה הוא עושה:**
- סורק היסטוריית PowerShell/CMD
- מחפש פעילות קשורה ל-Claude Code
- זיהוי שינויי קבצים מהזמן האחרון
- יוצר סשן חדש ביומן השיחות

**קבצים שמתעדכנים:**
- `conversation_log.md` - יומן השיחות
- `conversation_log.html` - גרסת HTML
- `automation/last_conversation_update.json` - מעקב זמן

**דוגמת פלט:**
```
🗣️ מתחיל עדכון יומן שיחות
📄 נמצאו 8 פעילויות חדשות
✅ יומן השיחות עודכן בהצלחה!
```

### 📝 כפתור "עדכן תיעוד"

**מה הוא עושה:**
- סורק כל קבצי `.md` בפרויקט
- בודק אילו השתנו מאז העדכון האחרון
- ממיר ל-HTML עם סגנון מתואם
- מעדכן `file_map.json` אוטומטית

**קבצים שמתעדכנים:**
- `*.html` (מכל קבצי MD)
- `file_map.json` - מיפוי קבצים מעודכן
- כל קבצי HTML עם קישורים מהירים אחידים

**דוגמת פלט:**
```
📝 מתחיל עדכון תיעוד
✓ עודכן: readme.html מתוך readme.md
✓ עודכן: tasks.html מתוך tasks.md
✅ הושלם! עודכנו 3 קבצים
```

### 🔗 כפתור "סנכרן GitHub"

**מה הוא עושה:**
- **אם אין repository:** יוצר חדש ב-GitHub
- **אם יש repository:** מסנכרן שינויים
- מבצע `git add`, `commit` ו-`push` אוטומטי
- יוצר commit messages מותאמים

**דרישות:**
- GitHub Token (ב-environment או בקובץ הגדרות)
- Git מותקן במערכת
- חיבור אינטרנט

**דוגמת פלט:**
```
🔗 מתחיל סינכרון GitHub
📂 יוצר repository: trading-project-002
✅ הפרויקט הועלה ל-GitHub בהצלחה!
🔗 Repository URL: https://github.com/username/trading-project-002
```

---

## ⚙️ הגדרות מתקדמות

### 🔐 הגדרת GitHub Token

**אופציה 1: משתנה סביבה**
```bash
set GITHUB_TOKEN=ghp_your_token_here
```

**אופציה 2: קובץ הגדרות**
יצור קובץ: `automation/github_config.json`
```json
{
  "github_token": "ghp_your_token_here",
  "repo_name": "trading-project-002"
}
```

### 🛠️ התאמת הגדרות

**שינוי פורט השרת:**
ערוך `automation/automation_server.py`, שורה:
```python
server = AutomationServer(port=8080)  # שנה לפורט אחר
```

**שינוי שם Repository:**
ערוך `automation/github_manager.py`, שורה:
```python
self.repo_name = "trading-project-002"  # שנה שם
```

---

## 🔧 פתרון בעיות נפוצות

### ❌ "Python לא מותקן"
**פתרון:** התקן Python מ-https://python.org

### ❌ "ספריה חסרה"
**פתרון:** 
```bash
pip install requests markdown
```

### ❌ "השרת לא עונה"
**פתרונות:**
1. בדוק שהשרת רץ (חלון טרמינל פתוח)
2. נסה לרענן את הדשבורד
3. בדוק firewall/antivirus

### ❌ "GitHub Token לא תקין"
**פתרונות:**
1. צור token חדש ב-GitHub Settings > Developer settings > Personal access tokens
2. ודא הרשאות: `repo`, `user`, `admin:repo_hook`
3. בדוק שהtoken לא פג תוקף

### ❌ "Git לא מותקן"
**פתרון:** התקן Git מ-https://git-scm.com

---

## 📊 מבנה קבצים

```
Trading Project 002/
├── automation/
│   ├── automation_server.py      # שרת HTTP
│   ├── update_conversations.py   # מעדכן יומן שיחות
│   ├── update_documentation.py   # ממיר MD→HTML
│   ├── github_manager.py         # מנהל GitHub
│   ├── github_config.json        # הגדרות GitHub
│   └── last_conversation_update.json # מעקב זמן
├── start_automation_server.bat   # הפעלת השרת
├── project_dashboard.html        # דשבורד עם הכפתורים
└── AUTOMATION_GUIDE.md          # המדריך הזה
```

---

## 🎨 התאמת ממשק

### שינוי צבעי כפתורים
ערוך `project_dashboard.html`, מצא:
```css
.auto-btn {
    background: linear-gradient(45deg, #6f42c1, #8e44ad); /* שנה צבעים */
}
```

### שינוי טקסט כפתורים
ערוך `project_dashboard.html`, מצא:
```html
<span class="btn-text">עדכן שיחות</span> <!-- שנה טקסט -->
```

---

## 📈 תכונות עתידיות

### 🔄 בתכנון
- **תזמון אוטומטי** - עדכונים יומיים/שבועיים
- **מעקב שגיאות** - לוג מפורט של כשלים
- **גיבויים** - שמירת גרסאות קודמות
- **הודעות אימייל** - התראות על עדכונים

### 💡 רעיונות לשיפור
- **עדכון סלקטיבי** - בחירת קבצים ספציפיים
- **תצוגת התקדמות** - progress bars מפורטים
- **היסטוריית פעילות** - מעקב כל העדכונים
- **שילוב Discord/Slack** - התראות אוטומטיות

---

## 🆘 תמיכה וקהילה

### 📞 איך לקבל עזרה
1. בדוק את הלוגים בחלון הטרמינל
2. הרץ עם `python -v` לדיבאג מפורט
3. צור issue ב-GitHub repository
4. פנה למפתח הראשי

### 🤝 תרומה לפרויקט
1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

---

**📅 עודכן אחרון:** 01 בספטמבר 2025  
**🤖 נוצר על ידי:** Claude Code Automation System  
**📝 גרסה:** 1.0.0