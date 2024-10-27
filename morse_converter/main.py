import typer
import signal
import sys
import json
import logging
from pathlib import Path
from typing import Optional
from rich.console import Console
from morse_converter.cli.interface import app
from morse_converter.utils import setup_logger, get_logger
from morse_converter.core import create_converter, create_audio_system

# Configurar console para output formateado
console = Console()

# Configurar logger para este módulo
logger = None

def setup_signal_handlers():
    """
    Configura los manejadores de señales para una terminación limpia.
    
    Esta función registra manejadores para SIGINT y SIGTERM que:
    1. Registran el evento en el log
    2. Muestran un mensaje de salida al usuario
    3. Aseguran que cleanup() se ejecute
    4. Terminan el programa de manera ordenada
    """
    def signal_handler(signum: int, frame):
        signal_name = signal.Signals(signum).name
        logger.info(f"Received signal {signal_name}")
        console.print(f"\n[yellow]Received {signal_name}, performing cleanup...[/yellow]")
        
        try:
            cleanup()
            console.print("[green]Cleanup completed successfully[/green]")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            console.print("[red]Error during cleanup[/red]")
        finally:
            console.print("[yellow]Exiting...[/yellow]")
            sys.exit(0)
    
    # Registrar manejadores para SIGINT y SIGTERM
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.debug("Signal handlers configured successfully")

def initialize_components() -> None:
    """
    Inicializa todos los componentes necesarios de la aplicación.
    
    Esta función:
    1. Configura el sistema de logging
    2. Carga la configuración global
    3. Inicializa los componentes principales
    4. Configura el sistema de audio
    
    Raises:
        FileNotFoundError: Si no se encuentra el archivo de configuración
        Exception: Para otros errores de inicialización
    """
    global logger, config, converter, audio_generator, audio_player
    
    try:
        # Inicializar logger
        log_file = Path("logs/morse_converter.log")
        logger = setup_logger(
            name="morse_converter",
            log_file=str(log_file)
        )
        logger.info("Starting Morse Code Converter application")
        
        # Cargar configuración
        config_path = Path(__file__).parent / "config" / "config.json"
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
            
        with open(config_path) as f:
            config = json.load(f)
        logger.debug("Configuration loaded successfully")
        
        # Crear instancia del converter
        converter = create_converter()
        logger.debug("Morse converter initialized")
        
        # Configurar sistema de audio
        audio_frequency = config.get("audio", {}).get("frequency", 800)
        audio_generator, audio_player = create_audio_system(
            frequency=audio_frequency
        )
        logger.debug(f"Audio system initialized with frequency {audio_frequency}Hz")
        
        # Configurar manejadores de señales
        setup_signal_handlers()
        
        console.print("[green]All components initialized successfully[/green]")
        
    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        console.print(f"[red]Configuration error: {e}[/red]")
        raise
        
    except Exception as e:
        logger.error(f"Initialization error: {e}")
        console.print(f"[red]Error during initialization: {e}[/red]")
        raise

def cleanup() -> None:
    """
    Realiza limpieza antes de la terminación del programa.
    
    Esta función:
    1. Detiene la reproducción de audio si está activa
    2. Cierra los manejadores de archivos abiertos
    3. Libera recursos del sistema de audio
    4. Asegura que los logs se escriban correctamente
    
    Raises:
        Exception: Si ocurre algún error durante la limpieza
    """
    try:
        logger.info("Starting cleanup process")
        
        # Detener reproducción de audio
        if 'audio_player' in globals() and audio_player is not None:
            try:
                audio_player.stop()
                logger.debug("Audio playback stopped")
            except Exception as e:
                logger.warning(f"Error stopping audio playback: {e}")
        
        # Liberar recursos de audio
        if 'audio_generator' in globals() and audio_generator is not None:
            try:
                audio_generator.cleanup()
                logger.debug("Audio resources released")
            except Exception as e:
                logger.warning(f"Error releasing audio resources: {e}")
        
        # Cerrar manejadores de archivos
        try:
            # Forzar escritura de logs pendientes
            for handler in logger.handlers[:]:
                handler.flush()
                handler.close()
                logger.removeHandler(handler)
            logging.shutdown()
        except Exception as e:
            # No podemos usar logger aquí porque ya está cerrado
            console.print(f"[yellow]Warning: Error closing log handlers: {e}[/yellow]")
        
        console.print("[green]Cleanup completed successfully[/green]")
        
    except Exception as e:
        console.print(f"[red]Error during cleanup: {e}[/red]")
        # No relanzamos la excepción para permitir que el programa termine
        # pero aseguramos que el error quede registrado
        if logging.getLogger().handlers:  # Si aún hay handlers disponibles
            logger.error(f"Cleanup error: {e}")

def main():
    """
    Punto de entrada principal para la aplicación Morse Code Converter.
    
    Esta función:
    1. Inicializa los componentes necesarios
    2. Configura el manejo de señales
    3. Ejecuta la interfaz CLI
    4. Maneja la limpieza al salir
    
    Returns:
        int: Código de salida (0 para éxito, 1 para error)
    """
    exit_code = 0
    
    try:
        # Inicializar componentes
        initialize_components()
        logger.info("Application initialized successfully")
        
        # Ejecutar la interfaz CLI
        logger.debug("Starting CLI interface")
        app()
        
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
        console.print("\n[yellow]Application terminated by user[/yellow]")
        exit_code = 0
        
    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        console.print(f"\n[red]Configuration error: {e}[/red]")
        exit_code = 1
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        console.print(f"\n[red]Unexpected error: {e}[/red]")
        exit_code = 1
        
    finally:
        try:
            cleanup()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            console.print(f"[red]Error during cleanup: {e}[/red]")
            exit_code = 1
        
        if exit_code == 0:
            logger.info("Application terminated successfully")
            console.print("[green]Application terminated successfully[/green]")
        else:
            logger.info("Application terminated with errors")
            console.print("[red]Application terminated with errors[/red]")
        
        return exit_code

if __name__ == "__main__":
    sys.exit(main())
