import subprocess
import sys
import os
from pathlib import Path

def start_servers():
    project_root = Path(__file__).parent
    
    backend_cmd = [
        sys.executable, "-m", "uvicorn", 
        "backend.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ]
    
    frontend_cmd = ["npm", "run", "dev"]
    
    print("正在启动后端服务器...")
    backend_process = subprocess.Popen(
        backend_cmd,
        cwd=project_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='utf-8',
        errors='ignore'
    )
    
    print("正在启动前端服务器...")
    frontend_process = subprocess.Popen(
        frontend_cmd,
        cwd=project_root / "frontend",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='utf-8',
        errors='ignore',
        shell=True
    )
    
    print("\n" + "="*60)
    print("服务器启动成功！")
    print("="*60)
    print("后端服务器: http://localhost:8000")
    print("前端服务器: http://localhost:5173 (或查看前端输出)")
    print("="*60)
    print("\n按 Ctrl+C 停止所有服务器\n")
    
    try:
        while True:
            backend_output = backend_process.stdout.readline()
            if backend_output:
                print(f"[后端] {backend_output.strip()}")
            
            frontend_output = frontend_process.stdout.readline()
            if frontend_output:
                print(f"[前端] {frontend_output.strip()}")
            
            if backend_process.poll() is not None and frontend_process.poll() is not None:
                break
                
    except KeyboardInterrupt:
        print("\n\n正在停止服务器...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()
        print("服务器已停止")

if __name__ == "__main__":
    start_servers()
