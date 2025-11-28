#!/usr/bin/env python3
"""
Run Streamlit Dashboard
Book Store API - Admin Dashboard
"""
import os
import subprocess
import sys


def main():
    """Run the Streamlit dashboard"""
    dashboard_dir = os.path.join(os.path.dirname(__file__), 'dashboard')
    app_file = os.path.join(dashboard_dir, 'app.py')
    
    if not os.path.exists(app_file):
        print("❌ Error: Dashboard app not found at:", app_file)
        sys.exit(1)
    
    print("🚀 Starting Book Store Admin Dashboard...")
    print(f"📁 Dashboard directory: {dashboard_dir}")
    print(f"📄 App file: {app_file}")
    print("\n" + "="*60)
    print("📊 Dashboard will be available at: http://localhost:8501")
    print("🔐 Login with admin credentials")
    print("="*60 + "\n")
    
    try:
        # Change to dashboard directory and run streamlit
        os.chdir(dashboard_dir)
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard stopped")
    except Exception as e:
        print(f"\n❌ Error running dashboard: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

