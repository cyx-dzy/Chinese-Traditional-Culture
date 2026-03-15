import subprocess
import sys
import os
from pathlib import Path


def get_database_password():
    """获取数据库密码"""
    print("="*60)
    print("溯光而行 - 服务器启动程序")
    print("="*60)
    print("\n请输入MySQL数据库密码:")
    password = input().strip()
    
    if not password:
        print("错误: 密码不能为空")
        return None
    
    return password


def run_database_import():
    """运行数据库导入脚本，如果失败则退出"""
    print("="*60)
    print("开始数据库导入流程")
    print("="*60)
    
    writh_sql_path = Path(__file__).parent / "backend" / "sql" / "writh_sql.py"
    
    if not writh_sql_path.exists():
        print(f"错误: 数据库导入脚本不存在: {writh_sql_path}")
        return False
    
    print(f"正在运行数据库导入脚本: {writh_sql_path}")
    
    try:
        result = subprocess.run(
            [sys.executable, str(writh_sql_path)],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            encoding='utf-8',
            env={**os.environ, "DB_PASSWORD": os.environ.get("DB_PASSWORD", "")}
        )
        
        if result.returncode != 0:
            print(f"\n错误: 数据库导入失败！")
            print(f"返回码: {result.returncode}")
            print(f"错误输出:\n{result.stderr}")
            return False
        
        print(f"\n数据库导入成功！")
        print(f"输出:\n{result.stdout}")
        return True
        
    except Exception as e:
        print(f"\n错误: 运行数据库导入脚本时发生异常: {e}")
        return False

def start_servers():
    project_root = Path(__file__).parent
    
    # 获取数据库密码
    db_password = get_database_password()
    if not db_password:
        print("\n密码输入失败，程序退出")
        sys.exit(1)
    
    # 设置环境变量
    os.environ["DB_PASSWORD"] = db_password
    
    # 先运行数据库导入
    if not run_database_import():
        print("\n数据库导入失败，程序退出")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("开始启动服务器")
    print("="*60)
    
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
    
    except Exception as e:
        print(f"\n\n发生错误: {e}")
        print("正在停止服务器...")
        try:
            backend_process.terminate()
            frontend_process.terminate()
            backend_process.wait()
            frontend_process.wait()
        except:
            pass
        print("服务器已停止")
        sys.exit(1)

if __name__ == "__main__":
    start_servers()
