"""
Script de inicio rápido para UpDaily Backend
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        print(f"Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def setup_environment():
    """Configurar entorno de desarrollo"""
    print("🚀 Configurando UpDaily Backend...")
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Crear entorno virtual si no existe
    venv_path = Path("venv")
    if not venv_path.exists():
        print("\n📦 Creando entorno virtual...")
        if not run_command("python -m venv venv", "Creación de entorno virtual"):
            return False
    
    # Determinar comando de activación
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Instalar dependencias
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Instalación de dependencias"):
        return False
    
    # Crear archivo .env si no existe
    env_file = Path(".env")
    if not env_file.exists():
        env_example = Path(".env.example")
        if env_example.exists():
            run_command(f"copy .env.example .env" if os.name == 'nt' else "cp .env.example .env", "Creación de archivo .env")
    
    print("\n✅ Configuración completada!")
    print("\n📋 Próximos pasos:")
    print("1. Activar entorno virtual:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Inicializar datos de ejemplo:")
    print(f"   {python_cmd} init_data.py")
    print("3. Ejecutar la aplicación:")
    print(f"   {python_cmd} main.py")
    print("\n🌐 La API estará disponible en: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/docs")
    
    return True

def main():
    """Función principal"""
    print("=" * 50)
    print("🎯 UpDaily Backend - Configuración Inicial")
    print("=" * 50)
    
    if setup_environment():
        print("\n🎉 ¡Configuración exitosa!")
        print("\n¿Deseas ejecutar la aplicación ahora? (y/n): ", end="")
        response = input().lower().strip()
        
        if response in ['y', 'yes', 'sí', 'si']:
            print("\n🚀 Iniciando aplicación...")
            python_cmd = "venv\\Scripts\\python" if os.name == 'nt' else "venv/bin/python"
            subprocess.run(f"{python_cmd} main.py", shell=True)
    else:
        print("\n❌ Configuración fallida. Revisa los errores anteriores.")
        sys.exit(1)

if __name__ == "__main__":
    main()
