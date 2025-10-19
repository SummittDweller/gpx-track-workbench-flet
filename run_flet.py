#!/usr/bin/env python3
"""
GPX Track Workbench - Flet Version Launcher
Simple launcher script for the Flet version of GPX Track Workbench
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    import flet as ft
    print("✅ Flet is available")
except ImportError:
    print("❌ Flet is not installed. Please run:")
    print("   pip install -r flet_requirements.txt")
    sys.exit(1)

# Import and run the Flet app
try:
    from flet_app import main
    print("🚀 Starting GPX Track Workbench (Flet version)...")
    ft.app(target=main)
except Exception as e:
    print(f"❌ Error starting application: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)