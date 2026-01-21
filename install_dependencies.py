"""
家庭财务管理系统 - 依赖安装脚本
"""

import subprocess
import sys

def install_package(package_name, import_name=None):
    """安装 Python 包"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✓ {package_name} 已安装")
        return True
    except ImportError:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
            print(f"✓ {package_name} 安装成功")
            return True
        except subprocess.CalledProcessError:
            print(f"✗ {package_name} 安装失败")
            return False

print("="*60)
print("家庭财务管理系统 - 依赖检查与安装")
print("="*60)

packages = [
    ('flask', 'flask'),
    ('flask-cors', 'flask_cors'),
    ('openpyxl', 'openpyxl'),
    ('pandas', 'pandas')
]

success_count = 0
for package_name, import_name in packages:
    if install_package(package_name, import_name):
        success_count += 1

print("="*60)
print(f"依赖安装完成: {success_count}/{len(packages)}")
print("="*60)

if success_count == len(packages):
    print("\n✓ 所有依赖已就绪，可以启动服务器了！")
    print("运行命令: python start_server.py")
else:
    print("\n⚠️  部分依赖安装失败，请手动检查")
