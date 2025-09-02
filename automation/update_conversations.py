#!/usr/bin/env python3
"""
Conversation Log Updater for Trading Project 002
מעדכן את יומן השיחות מהטרמינל/Claude Code
"""

import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

class ConversationUpdater:
    def __init__(self, project_root=None):
        """אתחול מעדכן השיחות"""
        if project_root is None:
            self.project_root = Path(__file__).parent.parent
        else:
            self.project_root = Path(project_root)
        
        self.conversation_log = self.project_root / "conversation_log.md"
        self.last_update_file = self.project_root / "automation" / "last_conversation_update.json"
        
        # טען זמן העדכון האחרון
        self.last_update_time = self._load_last_update_time()
        
    def _load_last_update_time(self):
        """טעינת זמן העדכון האחרון"""
        try:
            if self.last_update_file.exists():
                with open(self.last_update_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return datetime.fromisoformat(data['last_update'])
            else:
                # אם אין קובץ, קח מזמן השיחה האחרונה בלוג
                return self._get_last_session_time()
        except:
            # פתרון ברירת מחדל - 24 שעות אחורה
            return datetime.now() - timedelta(days=1)
    
    def _save_last_update_time(self):
        """שמירת זמן העדכון הנוכחי"""
        try:
            os.makedirs(self.last_update_file.parent, exist_ok=True)
            with open(self.last_update_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'last_update': datetime.now().isoformat(),
                    'session_updated': self._get_current_session_number()
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[WARNING] לא ניתן לשמור זמן עדכון: {e}")
    
    def _get_last_session_time(self):
        """חילוץ זמן מהסשן האחרון בלוג"""
        try:
            if not self.conversation_log.exists():
                return datetime.now() - timedelta(days=1)
            
            with open(self.conversation_log, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # חפש תאריכים בפורמט Session
            sessions = re.findall(r'Session #(\d+).*?(\d{4}-\d{2}-\d{2})', content)
            if sessions:
                last_date = sessions[-1][1]
                return datetime.strptime(last_date, "%Y-%m-%d")
                
        except:
            pass
            
        return datetime.now() - timedelta(days=1)
    
    def _get_current_session_number(self):
        """מציאת מספר הסשן הנוכחי"""
        try:
            if not self.conversation_log.exists():
                return 1
            
            with open(self.conversation_log, 'r', encoding='utf-8') as f:
                content = f.read()
            
            sessions = re.findall(r'Session #(\d+)', content)
            if sessions:
                return max([int(s) for s in sessions]) + 1
            else:
                return 1
                
        except:
            return 1
    
    def scan_terminal_history(self):
        """סריקת היסטוריית הטרמינל עבור פעילות Claude Code"""
        activities = []
        
        try:
            # נסה לקרוא מ-PowerShell history
            powershell_history = self._get_powershell_history()
            if powershell_history:
                activities.extend(self._parse_powershell_activities(powershell_history))
            
            # נסה לקרוא מ-CMD history אם קיים
            cmd_activities = self._get_cmd_activities()
            if cmd_activities:
                activities.extend(cmd_activities)
            
            # חפש קבצי לוג נוספים
            log_activities = self._scan_log_files()
            if log_activities:
                activities.extend(log_activities)
                
        except Exception as e:
            print(f"[WARNING] שגיאה בסריקת היסטוריה: {e}")
        
        return self._filter_relevant_activities(activities)
    
    def _get_powershell_history(self):
        """קריאת היסטוריית PowerShell"""
        try:
            # נתיב היסטוריית PowerShell
            history_path = Path.home() / "AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine/ConsoleHost_history.txt"
            
            if not history_path.exists():
                return []
            
            # קרא רק שורות מהזמן האחרון
            with open(history_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # סנן פעילות רלוונטית מהזמן האחרון
            recent_lines = []
            file_mod_time = datetime.fromtimestamp(history_path.stat().st_mtime)
            
            if file_mod_time > self.last_update_time:
                # קח את השורות האחרונות (משערים לפי מיקום)
                recent_lines = lines[-200:]  # קח 200 השורות האחרונות
            
            return recent_lines
            
        except Exception as e:
            print(f"[WARNING] לא ניתן לקרוא היסטוריית PowerShell: {e}")
            return []
    
    def _parse_powershell_activities(self, history_lines):
        """פרסר פעילויות מהיסטוריית PowerShell"""
        activities = []
        
        claude_keywords = [
            'claude', 'anthropic', 'claude-code', 'npx @anthropic-ai/claude-code',
            'trading project', 'project 002'
        ]
        
        for line in history_lines:
            line = line.strip().lower()
            
            # בדוק אם יש קשר ל-Claude או לפרויקט
            if any(keyword in line for keyword in claude_keywords):
                activity = {
                    'type': 'claude_activity',
                    'command': line,
                    'timestamp': datetime.now(),  # נעדכן מאוחר יותר אם נמצא
                    'description': self._analyze_command(line)
                }
                activities.append(activity)
        
        return activities
    
    def _get_cmd_activities(self):
        """סריקת פעילויות CMD (אם קיימות)"""
        # CMD לא שומר היסטוריה כמו PowerShell
        # אבל נוכל לחפש בקבצי לוג או ב-Recent Documents
        activities = []
        
        try:
            # חפש קבצים שנוצרו/שונו לאחרונה בפרויקט
            for file_path in self.project_root.rglob("*"):
                if file_path.is_file():
                    mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mod_time > self.last_update_time:
                        activity = {
                            'type': 'file_change',
                            'file': file_path.name,
                            'timestamp': mod_time,
                            'description': f"עודכן קובץ: {file_path.name}"
                        }
                        activities.append(activity)
        except:
            pass
        
        return activities
    
    def _scan_log_files(self):
        """סריקת קבצי לוג בפרויקט"""
        activities = []
        
        # חפש קבצי לוג אפשריים
        log_patterns = ['*.log', '*.txt', 'debug*', 'error*']
        
        for pattern in log_patterns:
            for log_file in self.project_root.rglob(pattern):
                if log_file.is_file():
                    try:
                        mod_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                        if mod_time > self.last_update_time:
                            # נסה לקרוא תוכן רלוונטי
                            with open(log_file, 'r', encoding='utf-8') as f:
                                content = f.read()[-1000:]  # קח 1000 תווים אחרונים
                            
                            if 'claude' in content.lower() or 'error' in content.lower():
                                activity = {
                                    'type': 'log_entry',
                                    'file': log_file.name,
                                    'timestamp': mod_time,
                                    'description': f"פעילות בלוג: {log_file.name}"
                                }
                                activities.append(activity)
                    except:
                        continue
        
        return activities
    
    def _analyze_command(self, command):
        """ניתוח פקודה והחזרת תיאור ברור"""
        command = command.lower()
        
        if 'claude-code' in command or 'npx @anthropic-ai' in command:
            return "הפעלת Claude Code"
        elif 'git' in command:
            if 'commit' in command:
                return "ביצוע Git commit"
            elif 'push' in command:
                return "ביצוע Git push"
            elif 'pull' in command:
                return "ביצוע Git pull"
            else:
                return "פעילות Git"
        elif 'python' in command or '.py' in command:
            return "הרצת סקריפט Python"
        elif 'mkdir' in command or 'md ' in command:
            return "יצירת תיקייה"
        elif 'touch' in command or 'new-item' in command:
            return "יצירת קובץ חדש"
        elif 'edit' in command or 'code' in command:
            return "עריכת קבצים"
        else:
            return f"פקודת טרמינל: {command[:50]}"
    
    def _filter_relevant_activities(self, activities):
        """סינון פעילויות רלוונטיות לפרויקט"""
        relevant = []
        
        project_keywords = [
            'trading', 'project', '002', 'claude', 'mstr', 
            'html', 'dashboard', 'automation'
        ]
        
        for activity in activities:
            # בדוק רלוונטיות לפי מילות מפתח
            text_to_check = f"{activity.get('command', '')} {activity.get('description', '')}".lower()
            
            if any(keyword in text_to_check for keyword in project_keywords):
                relevant.append(activity)
        
        return relevant
    
    def create_new_session(self, activities):
        """יצירת סשן חדש ביומן השיחות"""
        session_num = self._get_current_session_number()
        current_time = datetime.now()
        
        # בנה סיכום מהפעילויות
        achievements = self._extract_achievements(activities)
        issues_found = self._extract_issues(activities)
        files_modified = self._extract_file_changes(activities)
        
        session_content = f'''

## 🎯 **Session #{session_num:03d}** - {current_time.strftime("%d/%m/%Y")} - {current_time.strftime("%H:%M")} - עדכון אוטומטי

### 📋 **נושאים עיקריים:**
1. **עדכון אוטומטי** - מערכת העדכון סרקה פעילות חדשה
2. **ניהול קבצים** - זוהו שינויים בקבצי הפרויקט
3. **תיעוד וארגון** - עדכון יומן השיחות האוטומטי

### [SUCCESS] **הישגים שזוהו:**
{self._format_achievements(achievements)}

### 🔍 **שינויים בקבצים:**
{self._format_file_changes(files_modified)}

### 🔧 **פעילויות טכניות:**
{self._format_technical_activities(activities)}

### ⏳ **משימות לבדיקה:**
- [ ] סקירת השינויים שזוהו אוטומטית
- [ ] אישור פעילויות שבוצעו  
- [ ] תכנון הצעדים הבאים

### 🎯 **יעדים לסשן הבא:**
- מעקב אחר התקדמות הפרויקט
- המשך פיתוח מערכת האוטומציה
- תיעוד שיפורים נוספים

### 📊 **נתונים חשובים:**
- **זמן עדכון:** {current_time.strftime("%H:%M:%S")}
- **פעילויות זוהו:** {len(activities)}
- **קבצים שונו:** {len(files_modified)}
- **עדכון אחרון:** {self.last_update_time.strftime("%d/%m/%Y %H:%M")}

---

'''
        
        return session_content
    
    def _extract_achievements(self, activities):
        """חילוץ הישגים מהפעילויות"""
        achievements = []
        
        for activity in activities:
            desc = activity.get('description', '').lower()
            
            if 'commit' in desc:
                achievements.append("ביצוע שמירה בגיט")
            elif 'קובץ' in desc and 'עודכן' in desc:
                achievements.append(f"עדכון קובץ: {activity.get('file', 'קובץ')}")
            elif 'claude' in desc:
                achievements.append("שימוש במערכת Claude Code")
            elif 'python' in desc:
                achievements.append("הרצת סקריפט Python")
        
        return achievements
    
    def _extract_issues(self, activities):
        """חילוץ בעיות מהפעילויות"""
        issues = []
        
        for activity in activities:
            desc = activity.get('description', '').lower()
            
            if 'error' in desc or 'שגיאה' in desc:
                issues.append(f"שגיאה זוהתה: {activity.get('description', '')}")
        
        return issues
    
    def _extract_file_changes(self, activities):
        """חילוץ שינויי קבצים"""
        changes = []
        
        for activity in activities:
            if activity.get('type') == 'file_change':
                changes.append({
                    'file': activity.get('file'),
                    'time': activity.get('timestamp'),
                    'description': activity.get('description')
                })
        
        return changes
    
    def _format_achievements(self, achievements):
        """עיצוב רשימת הישגים"""
        if not achievements:
            return "- לא זוהו הישגים ספציפיים בסשן זה"
        
        formatted = []
        for achievement in achievements:
            formatted.append(f"- **✓ {achievement}**")
        
        return '\n'.join(formatted)
    
    def _format_file_changes(self, changes):
        """עיצוב רשימת שינויי קבצים"""
        if not changes:
            return "- לא זוהו שינויי קבצים"
        
        formatted = []
        for change in changes:
            time_str = change['time'].strftime("%H:%M")
            formatted.append(f"- **{change['file']}** - {time_str}")
        
        return '\n'.join(formatted)
    
    def _format_technical_activities(self, activities):
        """עיצוב פעילויות טכניות"""
        if not activities:
            return "- לא זוהו פעילויות טכניות"
        
        formatted = []
        for activity in activities:
            if activity.get('type') == 'claude_activity':
                formatted.append(f"- **Claude:** {activity.get('description')}")
            elif activity.get('type') == 'log_entry':
                formatted.append(f"- **לוג:** {activity.get('description')}")
        
        return '\n'.join(formatted[:5])  # הגבל ל-5 פעילויות
    
    def update_conversation_log(self, session_content):
        """עדכון קובץ יומן השיחות"""
        try:
            # קרא תוכן נוכחי
            if self.conversation_log.exists():
                with open(self.conversation_log, 'r', encoding='utf-8') as f:
                    current_content = f.read()
            else:
                current_content = self._create_initial_log()
            
            # הוסף סשן חדש לפני הסטטיסטיקות
            if "## 📈 **סטטיסטיקות" in current_content:
                parts = current_content.split("## 📈 **סטטיסטיקות")
                new_content = parts[0] + session_content + "\n## 📈 **סטטיסטיקות" + parts[1]
            else:
                new_content = current_content + session_content
            
            # שמור קובץ מעודכן
            with open(self.conversation_log, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✓ עודכן יומן השיחות עם סשן חדש")
            return True
            
        except Exception as e:
            print(f"✗ שגיאה בעדכון יומן: {str(e)}")
            return False
    
    def _create_initial_log(self):
        """יצירת יומן שיחות ראשוני אם לא קיים"""
        return f"""# 💬 יומן שיחות - Trading Project 002

## 📊 **מידע כללי על הפרויקט**
**שם הפרויקט:** Statistical Trading Analysis System  
**תאריך התחלה:** 01 בספטמבר 2025  
**מטרה עיקרית:** פיתוח מערכת ניתוח סטטיסטי לנתוני MSTR ובניית אסטרטגיות מסחר מבוססות נתונים

---

## 📈 **סטטיסטיקות פרויקט**
- **סשנים:** 1
- **שעות עבודה:** ~1
- **קבצים נוצרו:** {len(list(self.project_root.glob('*')))}
- **שלב נוכחי:** פיתוח מתקדם
- **אחוז השלמה:** 25%

---

**[UPDATE] עודכן:** {datetime.now().strftime("%d בספטמבר %Y, %H:%M")}  
**🔄 סטטוס:** פעיל - מערכת עדכון אוטומטית
"""
    
    def run_conversation_update(self):
        """הרצת עדכון מלא של יומן השיחות"""
        print(f"[CONV] מתחיל עדכון יומן שיחות - Trading Project 002")
        print(f"[DATE] {datetime.now().strftime('%d בספטמבר %Y, %H:%M')}")
        print(f"עדכון אחרון: {self.last_update_time.strftime('%d/%m/%Y %H:%M')}")
        print("=" * 50)
        
        # סרוק פעילויות חדשות
        print("סורק פעילות בטרמינל...")
        activities = self.scan_terminal_history()
        
        if not activities:
            print("[INFO] לא נמצאו פעילויות חדשות מאז העדכון האחרון")
            return {'success': True, 'new_activities': 0}
        
        print(f"📄 נמצאו {len(activities)} פעילויות חדשות")
        
        # יצור סשן חדש
        print("[UPDATE] יוצר סשן חדש ביומן...")
        session_content = self.create_new_session(activities)
        
        # עדכן יומן השיחות
        if self.update_conversation_log(session_content):
            # שמור זמן עדכון
            self._save_last_update_time()
            
            print("=" * 50)
            print(f"[SUCCESS] יומן השיחות עודכן בהצלחה!")
            print(f"📋 פעילויות שנמצאו: {len(activities)}")
            
            return {
                'success': True,
                'new_activities': len(activities),
                'session_created': True
            }
        else:
            return {'success': False, 'error': 'כשל בעדכון היומן'}

def main():
    """הרצה עצמאית"""
    updater = ConversationUpdater()
    result = updater.run_conversation_update()
    
    if result['success']:
        print(f"\n🎉 עדכון יומן השיחות הושלם בהצלחה!")
    else:
        print(f"\n[ERROR] נכשל בעדכון יומן השיחות")
    
    return result

if __name__ == "__main__":
    main()