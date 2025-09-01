# 📊 Project Requirements Document (PRD)
## Trading Project 002 - Statistical Trading Analysis System

---

## 📋 **פרויקט Overview**

### **מטרת הפרויקט:**
פיתוח מערכת ניתוח סטטיסטי מתקדמת לנתוני מסחר, המתמקדת ברכישת נתונים היסטוריים מ-Interactive Brokers, בניית מאגר מידע יציב ומהימן, וביצוע מחקר סטטיסטי מקיף. המערכת תשמש כבסיס לפיתוח אסטרטגיות מסחר מבוססות נתונים.

### **הבדלים מגישה קודמת (Trading Project 001):**
- **מערכת חדשה לחלוטין** - לא מיגרציה מ-C#/NinjaTrader
- **מיקוד על ניתוח סטטיסטי** כבסיס לאסטרטגיות
- **בניית תשתית נתונים** כעדיפות ראשונה
- **גישה מחקרית** - ממצאים יובילו לאסטרטגיות

---

## 📁 **קבצים קיימים במערכת הקודמת (Reference)**

### **מסמכי תיעוד וניהול:**
- **README.md** - תיאור כללי פרויקט המיגרציה מ-C#
- **current_status.md** - מעקב התקדמות ומשימות
- **conversation_log.md** - יומן שיחות מפורט
- **TASKS.md** - ניהול משימות וטיימליין
- **file_map.json** - מיפוי מלא של מבנה הקבצים

### **תכנון טכני:**
- **python_architecture_plan.md** - תכנון ארכיטקטורת Python
- **database_comparison.md** - השוואת מסדי נתונים (SQLite/PostgreSQL/DuckDB)
- **data_loader_plan.md** - תכנון טעינת נתונים מ-CSV

### **מערכת Dashboard:**
- **project_dashboard.html** - דשבורד מרכזי עם סקירה כללית
- **current_status.html, tasks.html, conversation_log.html** - דפי מעקב
- **architecture_plan.html, database_comparison.html** - דפי תכנון
- **rtl_editor.html** - עורך טקסט RTL
- **generate_html_dashboard.py** - מחולל HTML אוטומטי

### **כלי עזר:**
- **update_conversation_log.py** - עדכון יומן אוטומטי
- **update_project_status.py** - עדכון סטטוס פרויקט
- **start_session.bat, update_html_auto.bat** - סקריפטי אוטומציה

### **מבנה קוד בסיסי:**
- **src/** - מבנה תיקיות Python עם core, brokers, data, indicators
- **requirements.txt** - רשימת ספריות Python
- **config/, data/, tests/, notebooks/** - תיקיות תמיכה

**קשרים בין קבצים:** מערכת מתוחכמת של עדכון הדדי בין Markdown ל-HTML, עם כלי אוטומציה לסינכרון תוכן.

---

## 🎯 **שלבי הפרויקט**

### **Phase 1: Interactive Brokers Integration**
**מטרה:** יצירת חיבור יציב ל-IB עם יכולות מלאות
- חיבור ל-TWS API
- הורדת נתונים היסטוריים (MSTR, 2 שנים, 1-דקה)
- יכולת ביצוע פקודות מסחר (לשלבים עתידיים)
- טיפול ב-rate limiting ושגיאות

### **Phase 2: Data Infrastructure**
**מטרה:** בניית מאגר נתונים יציב ואמין
- תכנון schema למסד נתונים
- רזולוציות מרובות (1-דקה, 15-דקות, 2-שעות, 4-שעות, יומי)
- אחסון ~2M רשומות OHLCV + timestamp
- מנגנוני backup ו-recovery

### **Phase 3 & 4: Indicators & Statistical Research** (במקביל)
**מטרה:** פיתוח כלי ניתוח ומחקר
- **Phase 3:** פיתוח/ייבוא אינדיקטורים טכניים
- **Phase 4:** מחקר סטטיסטי מקיף על הנתונים
- השוואות בין רזולוציות זמן שונות
- ניתוח patterns ו-correlations

### **Phase 5: Analysis Results**
**מטרה:** הפקת מסקנות מהמחקר
- סיכום ממצאים סטטיסטיים
- זיהוי patterns משמעותיים
- הערכת פוטנציאל רווח

### **Phase 6: Trading Strategy Development**
**מטרה:** בניית אסטרטגיה מבוססת ממצאים
- תכנון אסטרטגיה על בסיס הממצאים
- backtesting מקיף
- אופטימיזציה ובדיקות

### **Phase 7: Quality Assurance** (לאורך כל הפרויקט)
**מטרה:** בקרת איכות מתמשכת
- בדיקות תקינות נתונים
- validation של חישובים
- monitoring וloggin
- error handling מקיף

---

## 🏗️ **רכיבים טכניים**

### **IB Connection Module**
- חיבור TWS/Gateway
- Historical data requests
- Real-time data (שלבים עתידיים)
- Order management capabilities

### **Data Storage System**
- רזולוציות זמן מרובות
- Data validation ו-cleansing
- Performance optimization
- Schema flexibility

### **Analysis Engine**
- Technical indicators library
- Statistical analysis tools
- Pattern recognition
- Performance metrics

### **Dashboard System**
- Web-based interface
- Real-time monitoring
- Data visualization
- Progress tracking

---

## ✅ **קריטריוני הצלחה**

### **Phase 1 Success:**
- חיבור יציב ל-IB ללא שגיאות
- הורדה מוצלחת של sample data
- טיפול נכון בשגיאות ו-reconnection

### **Phase 2 Success:**
- מסד נתונים עם 2M+ רשומות
- זמן query מהיר (<1 שניה לבקשות רגילות)
- שלמות נתונים 100%

### **Phase 3-4 Success:**
- אינדיקטורים מחושבים נכון
- ממצאים סטטיסטיים משמעותיים
- תיעוד מפורט של הממצאים

### **Phase 5-6 Success:**
- אסטרטגיה מוגדרת ברורה
- backtesting results חיוביים
- מוכנות לtrading בזמן אמת

---

## ⚠️ **גורמי סיכון ופתרונות**

### **סיכונים טכניים:**
- **IB API limitations** → fallback mechanisms, rate limiting
- **גודל נתונים** → database optimization, indexing
- **ביצועים** → profiling, caching strategies

### **סיכוני נתונים:**
- **איכות נתונים** → multiple validation layers
- **נתונים חסרים** → detection ו-handling protocols
- **שגיאות חישוב** → unit testing מקיף

### **סיכוני פרויקט:**
- **complexity creep** → phased approach, clear boundaries
- **timeline overruns** → realistic planning, buffer time
- **scope changes** → clear requirements, change control

---

## 📈 **תוצאות צפויות**

### **תשתית טכנית:**
- מערכת איסוף נתונים אמינה
- מסד נתונים מייעל וגמיש
- כלי ניתוח מתקדמים

### **ממצאי מחקר:**
- הבנת התנהגות מחירי MSTR
- זיהוי patterns סטטיסטיים
- base line לאסטרטגיות עתידיות

### **אסטרטגיית מסחר:**
- מבוססת נתונים וממצאים
- backtested ומאומתת
- מוכנה ליישום בזמן אמת

---

## 🔄 **Dependencies בין שלבים**

- **Phase 2** תלוי ב-Phase 1 (צריך נתונים לפני אחסון)
- **Phase 3-4** תלויים ב-Phase 2 (צריך מסד נתונים מוכן)
- **Phase 5** תלוי ב-Phase 3-4 (צריך ממצאים לפני מסקנות)
- **Phase 6** תלוי ב-Phase 5 (צריך מסקנות לפני אסטרטגיה)
- **Phase 7** רץ במקביל לכל השלבים

---

**📅 תאריך יצירה:** 31 באוגוסט 2025  
**🔄 גרסה:** 1.0  
**👤 נוצר על ידי:** Claude Code Assistant  
**📝 סטטוס:** Draft - מחכה לאישור