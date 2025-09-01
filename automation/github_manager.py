#!/usr/bin/env python3
"""
GitHub Manager for Trading Project 002
מנהל סינכרון עם GitHub - יצירת רפו, commits ו-pushes
"""

import os
import json
import subprocess
import requests
from datetime import datetime
from pathlib import Path
import shutil

class GitHubManager:
    def __init__(self, project_root=None):
        """אתחול מנהל GitHub"""
        if project_root is None:
            self.project_root = Path(__file__).parent.parent
        else:
            self.project_root = Path(project_root)
        
        self.repo_name = "trading-project-002"
        self.config_file = self.project_root / "automation" / "github_config.json"
        self.github_token = self._load_github_token()
        
    def _load_github_token(self):
        """טעינת GitHub token מהגדרות"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return config.get('github_token')
        except:
            pass
        
        # נסה מ-environment variables
        return os.environ.get('GITHUB_TOKEN')
    
    def _save_config(self, config_data):
        """שמירת הגדרות GitHub"""
        try:
            os.makedirs(self.config_file.parent, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ לא ניתן לשמור הגדרות: {e}")
    
    def check_git_setup(self):
        """בדיקת תקינות Git"""
        try:
            # בדוק אם Git מותקן
            result = subprocess.run(['git', '--version'], 
                                 capture_output=True, text=True, cwd=self.project_root)
            if result.returncode != 0:
                return False, "Git לא מותקן במערכת"
            
            # בדוק אם התיקייה היא git repository
            git_dir = self.project_root / ".git"
            if not git_dir.exists():
                return False, "התיקייה אינה Git repository"
            
            return True, "Git מוגדר כראוי"
            
        except Exception as e:
            return False, f"שגיאה בבדיקת Git: {str(e)}"
    
    def init_local_git(self):
        """אתחול Git repository מקומי"""
        try:
            # בדוק אם כבר יש .git
            if (self.project_root / ".git").exists():
                print("ℹ️ Git repository כבר קיים")
                return True
            
            print("🔄 מאתחל Git repository מקומי...")
            
            # git init
            result = subprocess.run(['git', 'init'], 
                                 capture_output=True, text=True, cwd=self.project_root)
            if result.returncode != 0:
                print(f"❌ כשל ב-git init: {result.stderr}")
                return False
            
            # יצור .gitignore
            self._create_gitignore()
            
            # הגדרת משתמש ברירת מחדל (אם לא מוגדר)
            self._setup_git_user()
            
            print("✅ Git repository מקומי הוקם בהצלחה")
            return True
            
        except Exception as e:
            print(f"❌ שגיאה באתחול Git: {str(e)}")
            return False
    
    def _create_gitignore(self):
        """יצירת קובץ .gitignore מתאים"""
        gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
automation/github_config.json
automation/last_*.json
*.tmp
temp/

# Sensitive data
*.key
*.pem
config/secrets.json
'''
        
        gitignore_path = self.project_root / ".gitignore"
        try:
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            print("📄 נוצר קובץ .gitignore")
        except Exception as e:
            print(f"⚠️ לא ניתן ליצור .gitignore: {e}")
    
    def _setup_git_user(self):
        """הגדרת משתמש Git ברירת מחדל"""
        try:
            # בדוק אם משתמש כבר מוגדר
            result = subprocess.run(['git', 'config', 'user.email'], 
                                 capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode != 0 or not result.stdout.strip():
                # הגדר משתמש ברירת מחדל
                subprocess.run(['git', 'config', 'user.email', 'trading.project.002@example.com'], 
                             cwd=self.project_root)
                subprocess.run(['git', 'config', 'user.name', 'Trading Project 002'], 
                             cwd=self.project_root)
                print("👤 הוגדר משתמש Git ברירת מחדל")
        except:
            pass
    
    def create_github_repository(self):
        """יצירת repository חדש ב-GitHub"""
        if not self.github_token:
            return False, "לא נמצא GitHub token - נדרש לאוטנטיקציה"
        
        try:
            print(f"🔄 יוצר repository: {self.repo_name}")
            
            # נתונים ליצירת repository
            repo_data = {
                "name": self.repo_name,
                "description": "Statistical Trading Analysis System - מערכת ניתוח סטטיסטי לנתוני מסחר",
                "private": False,  # שנה ל-True אם רוצה repository פרטי
                "auto_init": False,
                "has_issues": True,
                "has_wiki": True,
                "has_downloads": True
            }
            
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            # שלח בקשה ליצירת repository
            response = requests.post("https://api.github.com/user/repos", 
                                   json=repo_data, headers=headers)
            
            if response.status_code == 201:
                repo_info = response.json()
                repo_url = repo_info["clone_url"]
                
                # שמור מידע על ה-repository
                config = {
                    "github_token": self.github_token,
                    "repo_name": self.repo_name,
                    "repo_url": repo_url,
                    "created_at": datetime.now().isoformat()
                }
                self._save_config(config)
                
                print(f"✅ Repository נוצר בהצלחה: {repo_info['html_url']}")
                return True, repo_url
                
            elif response.status_code == 422:
                return False, f"Repository בשם {self.repo_name} כבר קיים"
            else:
                return False, f"שגיאה ביצירת repository: {response.status_code} - {response.text}"
                
        except Exception as e:
            return False, f"שגיאה בחיבור ל-GitHub API: {str(e)}"
    
    def add_remote_origin(self, repo_url):
        """הוספת remote origin ל-repository המקומי"""
        try:
            # בדוק אם remote origin כבר קיים
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                 capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                current_origin = result.stdout.strip()
                if repo_url in current_origin:
                    print("ℹ️ Remote origin כבר מוגדר נכון")
                    return True
                else:
                    # עדכן origin קיים
                    subprocess.run(['git', 'remote', 'set-url', 'origin', repo_url], 
                                 cwd=self.project_root)
                    print("🔄 עודכן remote origin")
            else:
                # הוסף origin חדש
                result = subprocess.run(['git', 'remote', 'add', 'origin', repo_url], 
                                     capture_output=True, text=True, cwd=self.project_root)
                if result.returncode != 0:
                    print(f"❌ כשל בהוספת remote: {result.stderr}")
                    return False
                print("✅ נוסף remote origin")
            
            return True
            
        except Exception as e:
            print(f"❌ שגיאה בהגדרת remote: {str(e)}")
            return False
    
    def create_initial_commit(self):
        """יצירת commit ראשוני"""
        try:
            print("📋 יוצר commit ראשוני...")
            
            # git add .
            result = subprocess.run(['git', 'add', '.'], 
                                 capture_output=True, text=True, cwd=self.project_root)
            if result.returncode != 0:
                print(f"❌ כשל ב-git add: {result.stderr}")
                return False
            
            # בדוק אם יש משהו לcommit
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                 capture_output=True, text=True, cwd=self.project_root)
            if not result.stdout.strip():
                print("ℹ️ אין שינויים לcommit")
                return True
            
            # יצור commit message
            commit_msg = f"""🚀 Initial commit - Trading Project 002

📊 Statistical Trading Analysis System
📅 נוצר: {datetime.now().strftime("%d בספטמבר %Y")}
🎯 מטרה: מערכת ניתוח סטטיסטי לנתוני MSTR

🤖 Generated with Claude Code Automation
Co-Authored-By: Claude <noreply@anthropic.com>"""
            
            # git commit
            result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                                 capture_output=True, text=True, cwd=self.project_root)
            if result.returncode != 0:
                print(f"❌ כשל ב-git commit: {result.stderr}")
                return False
            
            print("✅ נוצר commit ראשוני")
            return True
            
        except Exception as e:
            print(f"❌ שגיאה ביצירת commit: {str(e)}")
            return False
    
    def push_to_github(self):
        """push לrepository ב-GitHub"""
        try:
            print("⬆️ מבצע push ל-GitHub...")
            
            # git push -u origin main
            result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                                 capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode != 0:
                # נסה עם master אם main לא עבד
                result = subprocess.run(['git', 'push', '-u', 'origin', 'master'], 
                                     capture_output=True, text=True, cwd=self.project_root)
                
                if result.returncode != 0:
                    print(f"❌ כשל ב-git push: {result.stderr}")
                    return False
            
            print("✅ הפרויקט הועלה ל-GitHub בהצלחה!")
            return True
            
        except Exception as e:
            print(f"❌ שגיאה ב-push: {str(e)}")
            return False
    
    def sync_with_github(self):
        """סינכרון מלא עם GitHub"""
        try:
            print("📋 יוצר commit חדש...")
            
            # git add .
            subprocess.run(['git', 'add', '.'], cwd=self.project_root)
            
            # בדוק אם יש שינויים
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                 capture_output=True, text=True, cwd=self.project_root)
            
            if not result.stdout.strip():
                print("ℹ️ אין שינויים חדשים לsync")
                return True
            
            # יצור commit message מותאם
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            commit_msg = f"""📝 Automatic sync - {timestamp}

🔄 עדכון אוטומטי של הפרויקט
📊 כולל עדכוני תיעוד וקבצי HTML
🤖 בוצע על ידי מערכת האוטומציה

🤖 Generated with Claude Code Automation
Co-Authored-By: Claude <noreply@anthropic.com>"""
            
            # commit
            result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                                 capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                # push
                result = subprocess.run(['git', 'push'], 
                                     capture_output=True, text=True, cwd=self.project_root)
                
                if result.returncode == 0:
                    print("✅ סינכרון עם GitHub הושלם בהצלחה!")
                    return True
                else:
                    print(f"⚠️ commit נוצר אך push נכשל: {result.stderr}")
                    return False
            else:
                print(f"❌ כשל ביצירת commit: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ שגיאה בסינכרון: {str(e)}")
            return False
    
    def run_full_github_setup(self):
        """הרצת תהליך מלא של הגדרת GitHub"""
        print(f"🔗 מתחיל הגדרת GitHub - Trading Project 002")
        print(f"📅 {datetime.now().strftime('%d בספטמבר %Y, %H:%M')}")
        print("=" * 50)
        
        # 1. בדוק Git מקומי
        print("🔍 בודק הגדרת Git מקומית...")
        git_ok, git_msg = self.check_git_setup()
        
        if not git_ok:
            if "אינה Git repository" in git_msg:
                print("🔄 מאתחל Git repository...")
                if not self.init_local_git():
                    return {'success': False, 'error': 'כשל באתחול Git'}
            else:
                return {'success': False, 'error': git_msg}
        
        # 2. נסה ליצור repository ב-GitHub (אם לא קיים)
        print("🔍 בודק/יוצר GitHub repository...")
        repo_created, repo_url = self.create_github_repository()
        
        if not repo_created and "כבר קיים" not in str(repo_url):
            print(f"⚠️ יצירת repository נכשלה: {repo_url}")
            # המשך עם repository קיים אם יש
            config_data = self._load_existing_config()
            if config_data and config_data.get('repo_url'):
                repo_url = config_data['repo_url']
                print(f"📂 משתמש ב-repository קיים: {repo_url}")
            else:
                return {'success': False, 'error': str(repo_url)}
        
        # 3. הגדר remote origin
        if not self.add_remote_origin(repo_url):
            return {'success': False, 'error': 'כשל בהגדרת remote origin'}
        
        # 4. יצור commit ראשוני אם נדרש
        if not self.create_initial_commit():
            return {'success': False, 'error': 'כשל ביצירת commit ראשוני'}
        
        # 5. push ל-GitHub
        if not self.push_to_github():
            return {'success': False, 'error': 'כשל ב-push לGitHub'}
        
        print("=" * 50)
        print("🎉 הגדרת GitHub הושלמה בהצלחה!")
        print(f"🔗 Repository URL: {repo_url.replace('.git', '')}")
        
        return {
            'success': True,
            'repo_url': repo_url,
            'message': 'GitHub repository הוגדר ומסונכרן'
        }
    
    def _load_existing_config(self):
        """טעינת הגדרות קיימות"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return None

def main():
    """הרצה עצמאית"""
    manager = GitHubManager()
    
    # בדוק אם יש token
    if not manager.github_token:
        print("❌ לא נמצא GitHub token!")
        print("💡 הגדר GitHub token באחת מהדרכים הבאות:")
        print("1. משתנה סביבה: set GITHUB_TOKEN=your_token")
        print("2. קובץ הגדרות: automation/github_config.json")
        return {'success': False, 'error': 'חסר GitHub token'}
    
    # הרץ הגדרה מלאה
    result = manager.run_full_github_setup()
    
    if result['success']:
        print(f"\n🎉 GitHub sync הושלם בהצלחה!")
    else:
        print(f"\n❌ נכשל ב-GitHub sync: {result.get('error')}")
    
    return result

if __name__ == "__main__":
    main()