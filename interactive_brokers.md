# 🔗 חיבור Interactive Brokers - Trading Project 002

## 🌐 **סקירה כללית**
מסמך מקיף המרכז את כל הקשור לחיבור, הגדרה ועבודה עם Interactive Brokers API לצורך הורדת נתוני MSTR היסטוריים ועתידיים. המסמך יתעדכן בהדרגה עם התקדמות החיבור והמימוש.

**מטרה:** יצירת חיבור יציב ואמין ל-Interactive Brokers לאיסוף נתונים היסטוריים של MSTR ויכולות מסחר עתידיות.

---

## 🎯 **יעדי החיבור**

### **Phase 1: IB Integration - יעדים עיקריים**
- **חיבור יציב** - קישור אמין לחשבון IB
- **הורדת נתונים** - איסוף 2 שנות נתונים של MSTR
- **API Management** - טיפול ב-rate limits ושגיאות
- **Data Quality** - אימות ובדיקת שלמות נתונים
- **אוטומציה** - תהליכי הורדה אוטומטיים

### **יעדים ארוכי טווח**
- מסחר אוטומטי באמצעות IB
- real-time data feeds
- portfolio management
- risk monitoring בזמן אמת

---

## 📋 **דרישות מוקדמות**

### **דרישות חשבון IB**
*בהמתנה לבדיקה*
- [ ] חשבון Interactive Brokers פעיל
- [ ] הרשאות לנתונים היסטוריים
- [ ] גבולות API מותרים
- [ ] עלויות נתונים (אם רלוונטי)

### **דרישות טכניות**
- [ ] TWS (Trader Workstation) או IB Gateway
- [ ] Python 3.8+ environment
- [ ] ספריית ib_insync
- [ ] חיבור אינטרנט יציב
- [ ] הגדרת firewall מתאימה

---

## 🔧 **הגדרת הסביבה הטכנית**

### **התקנת ספריות Python**
```bash
# Environment setup - יבוצע בPhase 1
pip install ib_insync
pip install pandas
pip install numpy
pip install asyncio
pip install nest_asyncio
```

### **מבנה פרויקט מתוכנן**
```
Trading Project 002/
├── ib_connection/
│   ├── __init__.py
│   ├── connection_manager.py
│   ├── data_downloader.py
│   ├── error_handler.py
│   └── config.py
├── data/
│   ├── raw/
│   └── processed/
└── logs/
    └── ib_connection.log
```

---

## 🔌 **ארכיטקטורת החיבור**

### **רכיבי החיבור המתוכננים**

#### **1. Connection Manager**
```python
# Pseudocode - יפותח בPhase 1
class IBConnectionManager:
    def __init__(self, host='127.0.0.1', port=7497, clientId=1):
        self.ib = IB()
        self.host = host
        self.port = port  
        self.clientId = clientId
        
    def connect(self):
        """Establish connection to IB"""
        pass
        
    def disconnect(self):
        """Safely disconnect from IB"""
        pass
        
    def is_connected(self):
        """Check connection status"""
        pass
```

#### **2. Data Downloader**
```python
# Pseudocode - יפותח בPhase 1
class MSTRDataDownloader:
    def __init__(self, connection_manager):
        self.ib_conn = connection_manager
        
    def download_historical(self, symbol='MSTR', period='2 Y'):
        """Download historical MSTR data"""
        pass
        
    def get_contract_details(self, symbol='MSTR'):
        """Get contract specifications"""
        pass
        
    def validate_data(self, data):
        """Validate downloaded data quality"""
        pass
```

#### **3. Error Handler**
```python
# Pseudocode - יפותח בPhase 1
class IBErrorHandler:
    def __init__(self):
        self.error_log = []
        
    def handle_rate_limit(self):
        """Handle API rate limiting"""
        pass
        
    def handle_connection_loss(self):
        """Handle connection interruptions"""
        pass
        
    def retry_with_backoff(self, func, max_retries=3):
        """Retry failed operations"""
        pass
```

---

## 📊 **פרמטרי הורדת הנתונים**

### **מפרטי MSTR**
| פרמטר | ערך | הערות |
|--------|-----|-------|
| **Symbol** | MSTR | MicroStrategy Inc. |
| **Exchange** | SMART | IB Smart routing |
| **Currency** | USD | דולר אמריקאי |
| **Security Type** | STK | מניה רגילה |

### **פרמטרי הורדה מתוכננים**
| רזולוציה | תקופה | נקודות נתונים משוערות |
|-----------|-------|------------------------|
| **1 min** | 2 years | ~2,000,000 רשומות |
| **15 min** | 2 years | ~130,000 רשומות |
| **2 hour** | 2 years | ~16,000 רשומות |
| **4 hour** | 2 years | ~8,000 רשומות |
| **1 day** | 2 years | ~730 רשומות |

---

## ⚙️ **ניהול Rate Limits**

### **מגבלות IB API הידועות**
*יבדקו בPhase 1*
- בקשות היסטוריות: עד X לדקה
- בקשות real-time: עד Y בשנייה  
- בקשות יומיות: עד Z ליום
- timeout periods: T שניות

### **אסטרטגיית ניהול**
```python
# Pseudocode - יפותח בPhase 1
class RateLimitManager:
    def __init__(self, requests_per_minute=60):
        self.rpm_limit = requests_per_minute
        self.request_times = []
        
    def can_make_request(self):
        """Check if request can be made"""
        pass
        
    def wait_if_needed(self):
        """Wait if rate limit reached"""
        pass
        
    def track_request(self):
        """Track request timing"""
        pass
```

---

## 🔍 **בדיקת איכות נתונים**

### **Validation Checks מתוכננות**
- [ ] **Completeness** - אין gaps בנתונים
- [ ] **OHLCV Logic** - Open ≤ High, Low ≤ Close
- [ ] **Volume Validation** - volume > 0
- [ ] **Timestamp Sequence** - רצף זמנים תקין
- [ ] **Price Reasonableness** - מחירים בטווח הגיוני

### **Quality Metrics**
```python
# Pseudocode - יפותח בPhase 1
def validate_mstr_data(df):
    """Comprehensive data validation"""
    checks = {
        'completeness': check_missing_data(df),
        'ohlc_logic': check_ohlc_validity(df), 
        'volume_positive': check_volume_positivity(df),
        'timestamp_sequence': check_time_sequence(df),
        'price_bounds': check_price_reasonableness(df)
    }
    return checks
```

---

## 🚨 **טיפול בשגיאות**

### **סוגי שגיאות צפויות**
1. **Connection Errors** - ניתוק מהשרת
2. **Rate Limit Exceeded** - חריגה ממגבלות API
3. **Invalid Requests** - בקשות לא תקינות
4. **Data Quality Issues** - נתונים פגומים
5. **Authentication Failures** - בעיות אימות

### **מנגנוני Recovery**
```python
# Pseudocode - יפותח בPhase 1
class IBRecoveryManager:
    def __init__(self):
        self.max_retries = 3
        self.backoff_factor = 2
        
    def exponential_backoff(self, attempt):
        """Calculate wait time for retry"""
        return self.backoff_factor ** attempt
        
    def recover_connection(self):
        """Attempt to recover lost connection"""
        pass
        
    def resume_download(self, last_timestamp):
        """Resume interrupted download"""
        pass
```

---

## 📈 **מוניטורינג וLoggging**

### **מדדי ביצועים לניטור**
- **Connection Uptime** - זמינות החיבור
- **Download Speed** - מהירות הורדה (records/sec)
- **Error Rate** - תדירות שגיאות
- **Data Completeness** - אחוז שלמות נתונים
- **API Usage** - ניצול מכסת API

### **Logging Strategy**
```python
# Pseudocode - יפותח בPhase 1
import logging

def setup_ib_logging():
    """Configure IB connection logging"""
    logger = logging.getLogger('ib_connection')
    logger.setLevel(logging.INFO)
    
    handler = logging.FileHandler('logs/ib_connection.log')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
```

---

## 🔄 **תהליך הורדה מתוכנן**

### **שלבי ההורדה**

#### **שלב 1: חיבור וולידציה**
1. התחברות ל-TWS/Gateway
2. בדיקת הרשאות חשבון
3. קבלת פרטי חוזה MSTR
4. בדיקת זמינות נתונים

#### **שלב 2: הורדה הדרגתית**
1. התחלה מהרזולוציה הגרועה (יומית)
2. הורדה ברצפים קטנים (חודש בכל פעם)
3. validation מיידית של כל batch
4. שמירה למאגר נתונים

#### **שלב 3: עיבוד ואגרגציה**
1. יצירת רזולוציות נוספות
2. חישוב מדדים טכניים בסיסיים
3. בדיקת consistency בין רזולוציות
4. דו"ח איכות נתונים סופי

---

## 💾 **אינטגרציה עם מאגר הנתונים**

### **Data Pipeline מתוכנן**
```
IB API → Validation → SQLite → Aggregation → Final Storage
```

### **Schema Integration**
```sql
-- יתווסף למאגר הנתונים
CREATE TABLE ib_download_log (
    id INTEGER PRIMARY KEY,
    symbol VARCHAR(10),
    timeframe VARCHAR(10), 
    start_date DATE,
    end_date DATE,
    records_count INTEGER,
    download_time DATETIME,
    status VARCHAR(20),
    error_message TEXT
);
```

---

## 🎯 **מדדי הצלחה לPhase 1**

### **KPIs עיקריים**
- [ ] **Connection Success Rate** > 99%
- [ ] **Data Completeness** > 99.9%
- [ ] **Download Speed** > 1000 records/minute
- [ ] **Error Rate** < 0.1%
- [ ] **Recovery Time** < 30 seconds

### **Deliverables מתוכננים**
- [ ] חיבור יציב ל-IB API
- [ ] הורדה מוצלחת של שבוע לדוגמה
- [ ] מנגנון error handling פועל
- [ ] תיעוד מקיף של התהליך
- [ ] קוד מודולרי וניתן לתחזוקה

---

## 🔮 **תכונות עתידיות**

### **Real-time Data Feed**
- streaming price data
- real-time alerts
- market depth information
- news feed integration

### **Trading Capabilities**
- order placement automation
- position management  
- risk monitoring
- P&L tracking

### **Advanced Features**
- portfolio rebalancing
- multi-asset support
- options data integration
- alternative data sources

---

## 📚 **משאבים ותיעוד**

### **Documentation Links**
- [IB API Documentation](https://interactivebrokers.github.io/tws-api/)
- [ib_insync Documentation](https://ib-insync.readthedocs.io/)
- [TWS Configuration Guide](https://www.interactivebrokers.com/en/index.php?f=5041)
- [API Rate Limits](https://www.interactivebrokers.com/en/software/api/apiguide/tables/historical_data_limitations.htm)

### **Code Examples**
- Basic connection setup
- Historical data requests  
- Error handling patterns
- Async programming with IB

---

## ⚠️ **סיכונים ומגבלות**

### **סיכונים טכניים**
1. **API Changes** - שינויים ב-IB API
2. **Rate Limiting** - מגבלות קשיחות
3. **Data Costs** - עלויות נוספות
4. **Connection Stability** - אמינות החיבור
5. **Market Hours** - מגבלות זמני מסחר

### **Risk Mitigation**
- backup data sources
- comprehensive error handling
- regular API updates monitoring
- cost tracking and management
- alternative connection methods

---

## 🔄 **מעקב התקדמות**

### **Phase 1 Timeline**
| שבוע | משימה | סטטוס |
|------|-------|-------|
| 1 | מחקר דרישות IB | 🟡 בתכנון |
| 1 | הגדרת Python env | 🟡 בתכנון |
| 1 | חיבור בסיסי | 🟡 בתכנון |
| 2 | הורדת דוגמה | 🟡 בתכנון |
| 2 | validation מקיף | 🟡 בתכנון |

---

## 🔄 **מעקב שינויים**

| תאריך | שינוי | סיבה |
|--------|-------|-------|
| 01/09/2025 | יצירת מסמך ראשוני | תחילת Phase 1 planning |
| - | מבנה טכני מתוכנן | טרם מימוש |

---

**📅 עודכן:** 01 בספטמבר 2025  
**👤 עודכן על ידי:** Claude Code Assistant  
**🔄 עדכון הבא:** תחילת Phase 1  
**📍 קישורים:** [Dashboard](project_dashboard.html) | [Tasks](tasks.html) | [Database](database.html)

---

> **📝 הערה חשובה:** מסמך זה מכיל תכנון מפורט לחיבור IB. המימוש הפרקטי יתחיל בPhase 1 עם מחקר דרישות החשבון והתקנת הסביבה הטכנית. כל הקוד והמימוש יתועדו במסמך זה בהדרגה.