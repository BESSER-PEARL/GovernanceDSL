#!/usr/bin/env python3
"""
Launch script for the Governance DSL Form Builder
"""

import os
import sys

# Add the parent directory to Python path so we can import from the DSL modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def main():
    try:
        from governance_form_builder import main as run_interface
        print("🚀 Starting Governance DSL Form Builder...")
        print("📖 Open your browser to: http://localhost:7860")
        print("⏹️  Press Ctrl+C to stop the server")
        
        interface = run_interface()
        interface.launch(
            server_name="localhost",
            server_port=7860,
            share=False,
            debug=True
        )
    except ImportError as e:
        print(f"❌ Error importing required modules: {e}")
        print("💡 Make sure to install requirements: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting the interface: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()