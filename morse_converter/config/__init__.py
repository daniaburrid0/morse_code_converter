# Este archivo indica que el directorio config es un paquete de Python.

"""
Configuration Package for Morse Code Converter.

Este módulo maneja la carga y validación de la configuración del proyecto
desde el archivo config.json.

Example:
    >>> from morse_converter.config import load_config, get_config
    >>> config = load_config()
    >>> audio_freq = config['audio']['frequency']
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

# Configuración por defecto
DEFAULT_CONFIG = {
    "audio": {
        "frequency": 800,
        "wpm": 20,
        "volume": 0.5
    },
    "system": {
        "log_level": "INFO",
        "max_log_size": "10MB"
    }
}

class AudioConfig(BaseModel):
    """Modelo de configuración para audio."""
    frequency: int = Field(default=800, ge=20, le=20000)
    wpm: int = Field(default=20, ge=5, le=60)
    volume: float = Field(default=0.5, ge=0.0, le=1.0)

class SystemConfig(BaseModel):
    """Modelo de configuración del sistema."""
    log_level: str = Field(default="INFO")
    max_log_size: str = Field(default="10MB")

class Config(BaseModel):
    """Modelo principal de configuración."""
    audio: AudioConfig
    system: SystemConfig

# Variable global para almacenar la configuración
_config: Optional[Dict[str, Any]] = None

def get_config_path() -> Path:
    """
    Obtiene la ruta al archivo de configuración.

    Returns:
        Path: Ruta al archivo config.json
    """
    return Path(__file__).parent / "config.json"

def load_config() -> Dict[str, Any]:
    """
    Carga la configuración desde el archivo JSON.
    Si el archivo no existe, crea uno nuevo con la configuración por defecto.

    Returns:
        Dict[str, Any]: Configuración cargada y validada

    Raises:
        ValueError: Si la configuración no es válida
        FileNotFoundError: Si no se puede crear el archivo de configuración
    """
    global _config
    
    if _config is not None:
        return _config
        
    config_path = get_config_path()
    
    try:
        if not config_path.exists():
            # Crear archivo de configuración con valores por defecto
            config_path.write_text(json.dumps(DEFAULT_CONFIG, indent=2))
            _config = DEFAULT_CONFIG
        else:
            # Cargar configuración existente
            with open(config_path) as f:
                loaded_config = json.load(f)
                
            # Validar configuración usando Pydantic
            validated_config = Config(**loaded_config)
            _config = validated_config.model_dump()
            
        return _config
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")
    except Exception as e:
        raise ValueError(f"Error loading configuration: {e}")

def get_config() -> Dict[str, Any]:
    """
    Obtiene la configuración actual. La carga si aún no está cargada.

    Returns:
        Dict[str, Any]: Configuración actual
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config

def update_config(new_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Actualiza la configuración y guarda los cambios en el archivo.

    Args:
        new_config (Dict[str, Any]): Nueva configuración

    Returns:
        Dict[str, Any]: Configuración actualizada y validada

    Raises:
        ValueError: Si la nueva configuración no es válida
    """
    global _config
    
    try:
        # Validar nueva configuración
        validated_config = Config(**new_config)
        config_dict = validated_config.model_dump()
        
        # Guardar en archivo
        config_path = get_config_path()
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
            
        _config = config_dict
        return _config
        
    except Exception as e:
        raise ValueError(f"Invalid configuration: {e}")

__all__ = [
    'load_config',
    'get_config',
    'update_config',
    'AudioConfig',
    'SystemConfig',
    'Config'
]
