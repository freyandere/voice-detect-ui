
import sys
sys.path.insert(0, r'E:\2.Projects\voice-detect-ui')
sys.path.insert(0, r'E:\2.Projects\voice-detect-ui/src')

from main import create_interface

try:
    print("Starting Gradio server...")
    demo = create_interface()
    print("Interface created successfully")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
