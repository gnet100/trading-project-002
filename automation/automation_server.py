#!/usr/bin/env python3
"""
Automation Server for Trading Project 002
שרת HTTP פשוט להפעלת כפתורי העדכון מהדשבורד
"""

import os
import json
import threading
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# Import הסקריפטים שלנו
try:
    from . import update_documentation, update_conversations, github_manager
except ImportError:
    import update_documentation
    import update_conversations
    import github_manager

class AutomationHandler(BaseHTTPRequestHandler):
    def __init__(self, project_root, *args, **kwargs):
        self.project_root = project_root
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        """טיפול בבקשות POST מהכפתורים"""
        try:
            # קרא נתונים מהבקשה
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            action = data.get('action')
            
            # הגדר headers לתגובה
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # בצע פעולה בהתאם לכפתור
            if action == 'update_conversations':
                result = self._handle_update_conversations()
            elif action == 'update_docs':
                result = self._handle_update_documentation()
            elif action == 'github_sync':
                result = self._handle_github_sync()
            else:
                result = {'success': False, 'error': 'פעולה לא מזוהה'}
            
            # החזר תגובה
            response = json.dumps(result, ensure_ascii=False)
            self.wfile.write(response.encode('utf-8'))
            
        except Exception as e:
            # טיפול בשגיאות
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            error_response = json.dumps({
                'success': False,
                'error': f'שגיאת שרת: {str(e)}'
            }, ensure_ascii=False)
            self.wfile.write(error_response.encode('utf-8'))
    
    def do_OPTIONS(self):
        """טיפול בבקשות preflight של CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _handle_update_conversations(self):
        """טיפול בעדכון יומן שיחות"""
        try:
            print("🗣️ מתחיל עדכון יומן שיחות...")
            
            updater = update_conversations.ConversationUpdater(self.project_root)
            result = updater.run_conversation_update()
            
            if result['success']:
                return {
                    'success': True,
                    'message': 'יומן השיחות עודכן בהצלחה',
                    'activities': result.get('new_activities', 0)
                }
            else:
                return result
                
        except Exception as e:
            return {'success': False, 'error': f'שגיאה בעדכון שיחות: {str(e)}'}
    
    def _handle_update_documentation(self):
        """טיפול בעדכון תיעוד"""
        try:
            print("📝 מתחיל עדכון תיעוד...")
            
            updater = update_documentation.DocumentationUpdater(self.project_root)
            result = updater.run_full_update()
            
            if result['success']:
                return {
                    'success': True,
                    'message': f'עודכנו {result["files_updated"]} קבצים',
                    'files_updated': result['files_updated'],
                    'updated_files': result.get('updated_files', [])
                }
            else:
                return result
                
        except Exception as e:
            return {'success': False, 'error': f'שגיאה בעדכון תיעוד: {str(e)}'}
    
    def _handle_github_sync(self):
        """טיפול בסינכרון GitHub"""
        try:
            print("🔗 מתחיל סינכרון GitHub...")
            
            manager = github_manager.GitHubManager(self.project_root)
            
            # בדוק אם Repository כבר קיים
            git_ok, _ = manager.check_git_setup()
            
            if git_ok:
                # Repository קיים - בצע sync רגיל
                if manager.sync_with_github():
                    return {
                        'success': True,
                        'message': 'סינכרון עם GitHub הושלם',
                        'action': 'sync'
                    }
                else:
                    return {'success': False, 'error': 'כשל בסינכרון'}
            else:
                # Repository לא קיים - בצע הגדרה מלאה
                result = manager.run_full_github_setup()
                
                if result['success']:
                    return {
                        'success': True,
                        'message': 'GitHub repository נוצר ומסונכרן',
                        'repo_url': result.get('repo_url'),
                        'action': 'created'
                    }
                else:
                    return result
                    
        except Exception as e:
            return {'success': False, 'error': f'שגיאה בסינכרון GitHub: {str(e)}'}
    
    def log_message(self, format, *args):
        """השתק לוגים מיותרים"""
        pass

class AutomationServer:
    def __init__(self, project_root=None, port=8080):
        if project_root is None:
            self.project_root = Path(__file__).parent.parent
        else:
            self.project_root = Path(project_root)
        
        self.port = port
        self.server = None
        
    def create_handler(self):
        """יצירת handler עם project_root"""
        def handler(*args, **kwargs):
            return AutomationHandler(self.project_root, *args, **kwargs)
        return handler
    
    def start_server(self):
        """הפעלת השרת"""
        try:
            handler = self.create_handler()
            self.server = HTTPServer(('localhost', self.port), handler)
            
            print(f"🚀 Automation Server מופעל על http://localhost:{self.port}")
            print(f"📁 Project Root: {self.project_root}")
            print("=" * 50)
            print("📋 נתיבים זמינים:")
            print("  POST /update_conversations - עדכון יומן שיחות")
            print("  POST /update_documentation - עדכון תיעוד") 
            print("  POST /github_sync - סינכרון GitHub")
            print("=" * 50)
            print("🔗 השרת מחובר לדשבורד - הכפתורים פעילים!")
            print("💡 עצור עם Ctrl+C")
            
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            print("\n🛑 השרת נעצר על ידי המשתמש")
            self.stop_server()
        except Exception as e:
            print(f"❌ שגיאה בהפעלת השרת: {str(e)}")
    
    def stop_server(self):
        """עצירת השרת"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("✅ השרת נעצר")

def check_dependencies():
    """בדיקת התלויות הנדרשות"""
    missing = []
    
    try:
        import requests
    except ImportError:
        missing.append('requests')
    
    try:
        import markdown
    except ImportError:
        missing.append('markdown')
    
    if missing:
        print("❌ חסרות ספריות Python:")
        for lib in missing:
            print(f"  - {lib}")
        print(f"\n💡 התקן עם: pip install {' '.join(missing)}")
        return False
    
    return True

def main():
    """הרצה עצמאית"""
    print("🤖 Trading Project 002 - Automation Server")
    print("=" * 50)
    
    # בדוק תלויות
    if not check_dependencies():
        return
    
    # הפעל שרת
    server = AutomationServer()
    
    try:
        server.start_server()
    except Exception as e:
        print(f"❌ שגיאה: {str(e)}")

if __name__ == "__main__":
    main()