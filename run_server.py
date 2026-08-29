"""
run_server.py - Root entry point to launch the FastAPI server.
"""

import uvicorn

if __name__ == "__main__":
    print("\n[i] Launching GitHub Insights FastAPI Server...")
    print("[*] Local Swagger UI Docs : http://127.0.0.1:8000/docs")
    print("[*] ReDoc Documentation   : http://127.0.0.1:8000/redoc")
    print("[*] Health Endpoint       : http://127.0.0.1:8000/\n")
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=True)
