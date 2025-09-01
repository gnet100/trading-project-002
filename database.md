# 🗃️ מאגר הנתונים - Trading Project 002

## 📊 **סקירה כללית**
מסמך מקיף המרכז את כל הקשור למערך הנתונים של הפרויקט - החל מתכנון והתלבטויות ראשוניות, דרך איסוף וולידציה, ועד עבודה שוטפת עם המאגר.

**מטרה:** בניית מאגר נתונים יציב ואמין עבור ~2 מיליון רשומות MSTR היסטוריות לצורך ניתוח סטטיסטי מתקדם.

---

## 🎯 **דרישות הליבה**

### **נפח נתונים**
| פרמטר | ערך | הערות |
|--------|-----|-------|
| מניה יעד | MSTR | MicroStrategy Inc. |
| טווח זמן | 2 שנים אחורה | ~730 ימי מסחר |
| רזולוציה ראשית | 1 דקה | OHLCV + timestamp |
| רשומות משוערות | ~2M רשומות | 390 דקות × 730 ימים |
| גודל משוער | 120-150 MB | כולל אינדקסים |

### **רזולוציות נדרשות**
- **1 דקה** - בסיס לכל הניתוחים
- **15 דקות** - ניתוחי momentum קצרי טווח  
- **2 שעות** - טרנדים יומיים
- **4 שעות** - swing trading patterns
- **יומי** - ניתוח טרנדים ארוכי טווח

---

## 🤔 **התלבטויות וקבלת החלטות**

### **בחירת טכנולוגיית Database**

#### **אפשרויות נבחנות:**

**1. SQLite** 
- ✅ **יתרונות:** פשוט, ללא הגדרות, מובנה ב-Python
- ✅ **ביצועים:** מצוין עד 100GB
- ❌ **חסרונות:** מוגבל בעתידנות, אין concurrent writes
- 🎯 **מתאים ל:** פרוטוטיפים ופיתוח ראשוני

**2. PostgreSQL**
- ✅ **יתרונות:** מקצועי, scalable, תמיכה מלאה ב-time series
- ✅ **extensions:** TimescaleDB לזמני series
- ❌ **חסרונות:** מורכב הגדרה, דורש תחזוקה
- 🎯 **מתאים ל:** production ופרויקטים גדולים

**3. DuckDB**
- ✅ **יתרונות:** מהיר במיוחד לanalytics, תמיכה מצוינת ב-pandas
- ✅ **ביצועים:** אופטימיזציה לקריאות analytical
- ❌ **חסרונות:** יחסית חדש, פחות mature
- 🎯 **מתאים ל:** data analysis וBI

#### **החלטה ראשונית:** 
**התחלה עם SQLite** לשלב פיתוח, מעבר ל-PostgreSQL בשלב production.

**נימוק:**
- מאפשר התחלה מהירה ללא complexity
- קל לנסות patterns שונים
- מעבר פשוט ל-PostgreSQL בהמשך
- תמיכה מצוינת ב-Python ecosystem

---

## 🏗️ **תכנון Schema**

### **מבנה טבלאות - גישה ראשונית**

#### **טבלה ראשית: `mstr_1min`**
```sql
CREATE TABLE mstr_1min (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    open DECIMAL(10,4) NOT NULL,
    high DECIMAL(10,4) NOT NULL, 
    low DECIMAL(10,4) NOT NULL,
    close DECIMAL(10,4) NOT NULL,
    volume INTEGER NOT NULL,
    
    -- Metadata fields
    data_source VARCHAR(50) DEFAULT 'IB_API',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    UNIQUE(timestamp)
);
```

#### **אינדקסים מתוכננים:**
```sql
-- Primary index for time-based queries
CREATE INDEX idx_mstr_1min_timestamp ON mstr_1min(timestamp);

-- Composite index for range queries
CREATE INDEX idx_mstr_1min_date_range ON mstr_1min(timestamp, close);

-- Index for volume analysis
CREATE INDEX idx_mstr_1min_volume ON mstr_1min(volume, timestamp);
```

#### **טבלאות רזולוציות נוספות:**
- `mstr_15min` - אגרגציה של 15 דקות
- `mstr_2hour` - אגרגציה של 2 שעות  
- `mstr_4hour` - אגרגציה של 4 שעות
- `mstr_daily` - נתונים יומיים

### **שאלות פתוחות לחקירה:**
1. האם לשמור רזולוציות גבוהות כטבלאות נפרדות או לחשב on-the-fly?
2. איך לטפל ב-gaps בנתונים (סוף שבועות, חגים)?
3. אילו מטדאטה נוספת לשמור (split adjustments, dividend dates)?
4. האם להוסיף טבלת log לפעולות על הנתונים?

---

## 📥 **אסטרטגיית איסוף נתונים**

### **שלב 1: חיבור IB API**
- בדיקת דרישות חשבון לנתונים היסטוריים
- הבנת rate limits וגבולות API
- הערכת עלויות (אם קיימות)

### **שלב 2: Data Pipeline ראשוני**
```python
# Pseudocode למבנה כללי
def download_mstr_data():
    # 1. Connect to IB API
    # 2. Request historical data (1min, 2 years)
    # 3. Validate data quality
    # 4. Insert to database with proper error handling
    # 5. Log progress and issues
    pass
```

### **שלב 3: Data Validation**
- בדיקת שלמות זמנית (אין gaps לא מוסברים)
- validation של OHLCV logic (Open ≤ High, Low ≤ Close, וכו')
- השוואה עם מקורות נתונים אחרים (spot checks)
- זיהוי outliers ונתונים חריגים

---

## ⚡ **אופטימיזציה וביצועים**

### **אסטרטגיות Indexing**
- **Time-based queries** - הכרחי לכל ניתוח
- **Range queries** - לסינון תקופות זמן
- **Volume analysis** - לניתוחי volume patterns

### **שיקולי Storage**
- **Compression** - שקלול דחיסת נתונים ישנים
- **Partitioning** - חלוקה לפי חודשים/רבעונים
- **Archival strategy** - העברת נתונים ישנים לאחסון קר

### **Query Optimization**
- בדיקת execution plans לשאילתות נפוצות
- מדידת זמני תגובה לפעולות שונות
- אופטימיזציה של join operations בין רזולוציות

---

## 🔄 **תחזוקה ואמינות**

### **Backup Strategy**
- **יומי:** גיבוי incremental של נתונים חדשים
- **שבועי:** גיבוי מלא של כל המאגר
- **חודשי:** גיבוי לאחסון חיצוני/cloud

### **Data Quality Monitoring**
- בדיקות אוטומטיות לשלמות נתונים
- התרעות על gaps או אנומליות
- דוחות איכות נתונים שבועיים

### **Recovery Procedures**
- תהליכי שחזור במקרה של corruption
- rollback לגרסאות קודמות
- re-download של תקופות ספציפיות

---

## 🚧 **שלבי מימוש**

### **Phase 2A: Database Foundation (שבוע 2)**
- [x] החלטה על SQLite כפתרון ראשוני
- [ ] הגדרת schema בסיסי
- [ ] יצירת scripts ליצירת טבלאות
- [ ] בדיקות יכולת והצגת נתונים

### **Phase 2B: Data Loading (שבוע 3)**
- [ ] מימוש data loader בסיסי
- [ ] connection ל-IB API
- [ ] הורדת batch ראשון (שבוע לדוגמה)
- [ ] בדיקת איכות ושלמות

### **Phase 2C: Full Dataset (שבוע 4)**
- [ ] הורדת 2 שנים מלאות
- [ ] יצירת כל רזולוציות הזמן
- [ ] validation מקיף של כל הנתונים
- [ ] אופטימיזציית ביצועים

---

## 📊 **מדדי הצלחה**

### **Phase 2 Success Criteria:**
- [ ] מאגר נתונים עם לפחות 100K רשומות מדויקות
- [ ] זמן תגובה < 1 שניה לשאילתות בסיסיות
- [ ] שלמות נתונים 100% (אפס missing data לא מוסבר)
- [ ] גיבוי אוטומטי פעיל ונבדק
- [ ] תיעוד מלא של schema ותהליכים

### **KPIs לביצועים:**
- **Insert Speed:** > 1000 records/second
- **Query Performance:** < 100ms לסינון יום
- **Storage Efficiency:** < 100 bytes/record בממוצע
- **Uptime:** 99.9% זמינות המאגר

---

## 💡 **רעיונות עתידיים**

### **תכונות מתקדמות**
- [ ] **Real-time updates** - עדכונים live במהלך שעות המסחר
- [ ] **Multi-symbol support** - הרחבה למניות נוספות
- [ ] **Advanced analytics** - מדדים טכניים במאגר
- [ ] **API layer** - REST API לגישה למאגר
- [ ] **Web dashboard** - ממשק גרפי לצפייה בנתונים

### **אינטגרציות**
- [ ] **Jupyter notebooks** - חיבור ישיר למחקר
- [ ] **Trading platforms** - export לפלטפורמות מסחר
- [ ] **Cloud deployment** - העברה ל-AWS/GCP

---

## 🔍 **בעיות ידועות ופתרונות**

### **חסמים צפויים:**
1. **IB API Rate Limits** - עלול להאט הורדת נתונים
   - *פתרון:* batch processing עם delays מתוכננים
   
2. **Data Quality Issues** - gaps או נתונים שגויים
   - *פתרון:* validation מרובד וbackfill procedures
   
3. **Storage Growth** - מאגר גדל במהירות
   - *פתרון:* compression ו-archival strategies

### **טכנולוגיות חלופיות לעתיד:**
- **ClickHouse** - לנתוני time series בהיקף גדול
- **InfluxDB** - מתמחה ב-time series data
- **Arctic (MongoDB)** - מגמגשות גדולות של time series

---

## 📚 **משאבים ותיעוד**

### **מדריכים טכניים:**
- [SQLite Time Series Best Practices](https://sqlite.org/draft/lang_datefunc.html)
- [Interactive Brokers API Documentation](https://interactivebrokers.github.io/tws-api/)
- [Pandas Time Series Analysis](https://pandas.pydata.org/docs/user_guide/timeseries.html)

### **ספריות Python מומלצות:**
- `sqlite3` - חיבור מובנה ל-SQLite
- `pandas` - עבודה עם time series
- `ib_insync` - ממשק נוח ל-IB API
- `sqlalchemy` - ORM לניהול schema

---

## 🔄 **מעקב שינויים**

| תאריך | שינוי | סיבה |
|--------|-------|-------|
| 01/09/2025 | יצירת מסמך ראשוני | תחילת Phase 2 planning |
| - | החלטה על SQLite ראשונית | פשטות ומהירות פיתוח |

---

**📅 עודכן:** 01 בספטמבר 2025  
**👤 עודכן על ידי:** Claude Code Assistant  
**🔄 עדכון הבא:** לאחר סיום Phase 2A  
**📍 קישורים:** [Dashboard](project_dashboard.html) | [Tasks](tasks.html) | [PRD](prd.html)