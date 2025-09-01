#!/usr/bin/env python3
"""
Documentation Updater for Trading Project 002
מעדכן אוטומטית את כל קבצי MD→HTML
"""

import os
import json
import markdown
from datetime import datetime
from pathlib import Path
import shutil
import hashlib

class DocumentationUpdater:
    def __init__(self, project_root=None):
        """אתחול מעדכן התיעוד"""
        if project_root is None:
            # התיקייה הראשית של הפרויקט (אחד למעלה מ-automation)
            self.project_root = Path(__file__).parent.parent
        else:
            self.project_root = Path(project_root)
        
        self.timestamp = datetime.now().strftime("%d בספטמבר %Y, %H:%M")
        self.updated_files = []
        
    def scan_md_files(self):
        """סריקת כל קבצי .md בפרויקט"""
        md_files = []
        for md_file in self.project_root.glob("*.md"):
            if md_file.name not in ['README.md']:  # השאר README כמו שהוא
                md_files.append(md_file)
        return md_files
    
    def check_if_update_needed(self, md_file):
        """בדיקה אם הקובץ זקוק לעדכון"""
        html_file = md_file.with_suffix('.html')
        
        if not html_file.exists():
            return True
            
        # השווה timestamps
        md_time = md_file.stat().st_mtime
        html_time = html_file.stat().st_mtime
        
        return md_time > html_time
    
    def md_to_html(self, md_file):
        """המרת קובץ MD ל-HTML מעוצב"""
        try:
            # קרא תוכן MD
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # המר ל-HTML
            html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
            
            # קבע כותרת מהקובץ או מהתוכן
            title = self._extract_title(md_content, md_file.stem)
            
            # יצירת HTML מלא עם סגנון
            full_html = self._create_full_html(html_content, title, md_file)
            
            # שמור HTML
            html_file = md_file.with_suffix('.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            print(f"✓ עודכן: {html_file.name} מתוך {md_file.name}")
            self.updated_files.append(html_file.name)
            return True
            
        except Exception as e:
            print(f"✗ שגיאה בעדכון {md_file.name}: {str(e)}")
            return False
    
    def _extract_title(self, md_content, default_title):
        """חילוץ כותרת מתוכן MD"""
        lines = md_content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return default_title.replace('_', ' ').title()
    
    def _create_full_html(self, html_content, title, source_file):
        """יצירת HTML מלא עם סגנון מתואם"""
        file_stats = self._get_file_stats(source_file)
        
        return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Trading Project 002</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #333;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            position: relative;
        }}
        
        .back-btn {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: linear-gradient(45deg, #4caf50, #66bb6a);
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            font-size: 14px;
            transition: all 0.3s ease;
        }}
        
        .back-btn:hover {{
            background: linear-gradient(45deg, #66bb6a, #4caf50);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
        }}
        
        .header {{
            text-align: center;
            border-bottom: 3px solid #6f42c1;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            color: #1e3c72;
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .file-info {{
            background: linear-gradient(120deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-right: 4px solid #6f42c1;
        }}
        
        h1, h2, h3 {{
            color: #1e3c72;
        }}
        
        h2 {{
            border-right: 4px solid #6f42c1;
            padding-right: 15px;
            margin-top: 30px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        th, td {{
            padding: 12px;
            text-align: right;
            border-bottom: 1px solid #ddd;
        }}
        
        th {{
            background: #f5f5f5;
            font-weight: bold;
            color: #333;
        }}
        
        tr:hover {{
            background: #f9f9f9;
        }}
        
        code {{
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }}
        
        pre {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            border-right: 4px solid #6f42c1;
        }}
        
        blockquote {{
            border-right: 4px solid #6f42c1;
            padding: 10px 20px;
            margin: 20px 0;
            background: #f9f9f9;
            border-radius: 0 8px 8px 0;
        }}
        
        ul, ol {{
            padding-right: 30px;
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        .highlight {{
            background: linear-gradient(120deg, #fff3cd 0%, #ffeaa7 100%);
            padding: 15px;
            border-radius: 8px;
            border-right: 4px solid #ffc107;
            margin: 15px 0;
        }}
        
        .timestamp {{
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #eee;
        }}
        
        .quick-access-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-top: 30px;
        }}
        
        .quick-access-section h2 {{
            color: #1e3c72;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .quick-access {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
        }}
        
        .quick-btn {{
            background: linear-gradient(45deg, #6f42c1, #8e44ad);
            color: white;
            padding: 6px 10px;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
            text-decoration: none;
            text-align: center;
            display: block;
            font-size: 0.75em;
        }}
        
        .quick-btn:hover {{
            background: linear-gradient(45deg, #8e44ad, #6f42c1);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(111, 66, 193, 0.4);
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
                margin: 10px;
            }}
            
            .file-info {{
                flex-direction: column;
                gap: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="project_dashboard.html" class="back-btn">🏠 חזרה לדשבורד</a>
        
        <div class="header">
            <h1>{title}</h1>
        </div>
        
        <div class="file-info">
            <div><strong>📄 גודל קובץ:</strong> {file_stats['size_kb']} KB</div>
            <div><strong>🕒 עודכן:</strong> {file_stats['modified']}</div>
            <div><strong>🔄 נוצר אוטומטית מ:</strong> {source_file.name}</div>
        </div>
        
        <div class="content">
            {html_content}
        </div>
        
        <!-- Quick Access Section -->
        <div class="quick-access-section">
            <h2>⚡ גישה מהירה</h2>
            <div class="quick-access">
                <a href="project_dashboard.html" class="quick-btn">🏠 דשבורד</a>
                <a href="readme.html" class="quick-btn">📖 README</a>
                <a href="prd.html" class="quick-btn">📋 PRD</a>
                <a href="current_status.html" class="quick-btn">📊 מצב נוכחי</a>
                <a href="conversation_log.html" class="quick-btn">💬 יומן שיחות</a>
                <a href="tasks.html" class="quick-btn">🎯 משימות</a>
                <a href="database.html" class="quick-btn">🗃️ מאגר נתונים</a>
                <a href="strategy.html" class="quick-btn">🚀 אסטרטגיה</a>
                <a href="statistics.html" class="quick-btn">📊 סטטיסטיקות</a>
                <a href="interactive_brokers.html" class="quick-btn">🔗 IB חיבור</a>
                <a href="file_map.html" class="quick-btn">🗂️ מפת קבצים</a>
                <a href="rtl_editor.html" class="quick-btn">📝 RTL Editor</a>
            </div>
        </div>
        
        <div class="timestamp">
            📅 HTML נוצר: {self.timestamp}<br>
            🔄 עדכון אוטומטי מקובץ המקור<br>
            🤖 נוצר על ידי מערכת העדכון האוטומטית
        </div>
    </div>
</body>
</html>"""
    
    def _get_file_stats(self, file_path):
        """קבלת סטטיסטיקות קובץ"""
        try:
            stat = file_path.stat()
            return {
                'size_kb': round(stat.st_size / 1024, 1),
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime("%d-%m-%Y %H:%M")
            }
        except:
            return {'size_kb': 0, 'modified': 'לא ידוע'}
    
    def update_file_map(self):
        """עדכון file_map.json עם הקבצים החדשים"""
        try:
            file_map_path = self.project_root / "file_map.json"
            
            if file_map_path.exists():
                with open(file_map_path, 'r', encoding='utf-8') as f:
                    file_map = json.load(f)
            else:
                return
            
            # עדכן תאריך עדכון אחרון
            file_map["project_info"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            
            # עדכן סטטיסטיקות
            html_files = len(list(self.project_root.glob("*.html")))
            md_files = len(list(self.project_root.glob("*.md")))
            
            file_map["statistics"]["by_type"]["html"] = html_files
            file_map["statistics"]["by_type"]["markdown"] = md_files
            file_map["statistics"]["total_files"] = html_files + md_files + 1  # +1 for JSON
            
            # שמור עדכון
            with open(file_map_path, 'w', encoding='utf-8') as f:
                json.dump(file_map, f, ensure_ascii=False, indent=4)
            
            print(f"✓ עודכן file_map.json")
            
        except Exception as e:
            print(f"✗ שגיאה בעדכון file_map: {str(e)}")
    
    def run_full_update(self):
        """הרצת עדכון מלא של כל התיעוד"""
        print(f"🚀 מתחיל עדכון תיעוד - Trading Project 002")
        print(f"📅 {self.timestamp}")
        print("=" * 50)
        
        # סרוק קבצי MD
        md_files = self.scan_md_files()
        print(f"📄 נמצאו {len(md_files)} קבצי Markdown")
        
        if not md_files:
            print("ℹ️ לא נמצאו קבצי MD לעדכון")
            return {'success': True, 'files_updated': 0}
        
        # עדכן כל קובץ שזקוק לכך
        updated_count = 0
        for md_file in md_files:
            if self.check_if_update_needed(md_file):
                if self.md_to_html(md_file):
                    updated_count += 1
            else:
                print(f"⏭️ מדולג: {md_file.name} (עדכני)")
        
        # עדכן file_map
        self.update_file_map()
        
        print("=" * 50)
        print(f"✅ הושלם! עודכנו {updated_count} קבצים")
        print(f"📋 רשימת קבצים שעודכנו: {', '.join(self.updated_files) if self.updated_files else 'אף אחד'}")
        
        return {
            'success': True,
            'files_updated': updated_count,
            'updated_files': self.updated_files
        }

def main():
    """הרצה עצמאית"""
    updater = DocumentationUpdater()
    result = updater.run_full_update()
    
    if result['success']:
        print(f"\n🎉 עדכון התיעוד הושלם בהצלחה!")
    else:
        print(f"\n❌ נכשל בעדכון התיעוד")
    
    return result

if __name__ == "__main__":
    main()