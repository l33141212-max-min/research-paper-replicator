
# Pure Python file-writer to prevent Notebook SyntaxErrors
with open("app_1.py", "w") as f:
    f.write("""import streamlit as st
import os
import time
from engine_1 import AdvancedResearchEngine

st.set_page_config(page_title="AI Research Engine", layout="wide", page_icon="🔬")

# Force Streamlit to cache the engine and not re-run it on every button click
@st.cache_resource(show_spinner="Initializing 7B Model weights on Kaggle GPU...")
def load_engine():
    return AdvancedResearchEngine()

st.title(" Deep AI Research & Replication Engine")

# Safely fetch the engine
try:
    engine = load_engine()
except Exception as e:
    st.error(f"Engine failed to mount to hardware layer: {e}")
    engine = None

uploaded_file = st.file_uploader("Upload target Research Paper (PDF Format Only)", type=["pdf"])

if uploaded_file is not None:
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.success(f"Successfully staged: {uploaded_file.name}")
    
    if st.button("Execute Comprehensive Analysis"):
        if engine is None:
            st.error("GPU Engine is not initialized yet. Please wait a moment and try again.")
        else:
            with st.spinner("Decoding document layouts and executing GPU extraction parameters..."):
                # Run the engine directly from your Kaggle backend
                st.session_state["results"] = engine.analyze_and_run(temp_path)
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if "results" in st.session_state:
        results = st.session_state["results"]
        
        if "error" in results:
            st.error(results["error"])
            st.stop()
            
        tab1, tab2, tab3 = st.tabs([" Architectural Blueprint", " Performance Metrics", "Implementation Guide"])
        
        with tab1:
            st.markdown("###  Complete Neural Architecture Layers")
            st.text_area(label="Live GPU Output", value=results.get("blueprint", ""), height=450, key="b_area")
            
        with tab2:
            st.markdown("###  Benchmark Validation Scores")
            st.text_area(label="Live GPU Output", value=results.get("metrics", ""), height=450, key="m_area")
            
        with tab3:
            st.markdown("### Reproduction Strategy Roadmap")
            st.text_area(label="Live GPU Output", value=results.get("steps", ""), height=450, key="s_area")
""")

print(" app_1.py has been successfully written via Python without syntax conflicts!")
from engine import AdvancedResearchEngine
import os
# ==================================================================
# EXECUTION SNIPPET 
# ==================================================================
if __name__ == "__main__":
    engine = AdvancedResearchEngine()
    pdf_path = "sample_paper.pdf"
    
    # Automatically downloads a sample AI paper to analyze if you don't have one uploaded
    if not os.path.exists(pdf_path):
        print("Downloading a sample PDF for analysis...")
        os.system("wget -q https://arxiv.org/pdf/1706.03762.pdf -O sample_paper.pdf")
        
    print(f"\nStarting analysis on: {pdf_path}")
    results = engine.analyze_and_run(pdf_path)
    print("\n--- RESULTS GENERATED SUCCESSFULLY ---")
    print(results.get("blueprint")[:500] + "...\n[Truncated for view]")
import threading
import time
import socket

# 1. Kill any broken connections
!pkill -9 -f ssh
!pkill -9 -f localtunnel
!pkill -9 -f streamlit
!fuser -k 8560/tcp 2>/dev/null

print(" Port 8560 cleared. Initializing Streamlit background worker...")

# 2. Spin up the server targeting your app_1.py file
def launch_my_app():
    os.system("streamlit run app_1.py --server.port 8560 --browser.gatherUsageStats=false")

threading.Thread(target=launch_my_app, daemon=True).start()

print(" Waiting for the 7B model to allocate GPU memory and bind to port 8560...")

# 3. Dynamic loop: Continually check port 8560 until it answers
port_ready = False
while not port_ready:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Check if port 8560 is listening
        if s.connect_ex(('localhost', 8560)) == 0:
            port_ready = True
            print("\n Streamlit engine successfully stabilized on Port 8560!")
         else:
            time.sleep(2)  # Check again every 2 seconds
os.system("ssh -p 443 -o StrictHostKeyChecking=no -R0:localhost:8560 qr@a.pinggy.io")
import os

# Read the current engine script
with open("engine_1.py", "r") as f:
    code = f.read()

# Swap out the 400 token ceiling for a roomier 1000 token limit
fixed_code = code.replace("max_new_tokens=400", "max_new_tokens=1000")

# Save it back down to the hard drive
with open("engine_1.py", "w") as f:
    f.write(fixed_code)

print(" Token limits raised to 1000! Your next analysis will not cut off mid-word.")
import os

# Read the current engine script
with open("engine_1.py", "r") as f:
    code = f.read()

# Make the architecture search query much more aggressive for numbers and shapes
old_query = '"model architecture layers channels dimensions convolutions parameters layers activation"'
new_query = '"layers hidden dimension heads parameters embedding blocks configuration architecture shape"'

fixed_code = code.replace(old_query, new_query)

# Save it back down
with open("engine_1.py", "w") as f:
    f.write(fixed_code)

print(" Search queries optimized for hidden layers, heads, and dimensions!")
            
