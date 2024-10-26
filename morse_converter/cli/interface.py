import typer
import signal
import json
from pathlib import Path
from typing import Optional, Dict, Any
from rich.console import Console
from rich.progress import Progress
from morse_converter.core.converter import MorseConverter
from morse_converter.core.audio import AudioGenerator, AudioPlayer
from morse_converter.utils import FileHandler, setup_logger
from morse_converter.core.validator import InputValidator, ValidationError

# Configuración inicial
app = typer.Typer(
    help="Morse Code Converter CLI - Convert text to Morse code and vice versa, with audio playback capabilities"
)
console = Console()
logger = setup_logger(__name__)

# Configuración global
config: Dict[str, Any] = {}

def load_config() -> Dict[str, Any]:
    """Cargar configuración desde archivo JSON."""
    try:
        config_path = Path(__file__).parent.parent / "config" / "config.json"
        with open(config_path) as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Could not load config file: {e}. Using defaults.")
        return {
            "audio": {
                "frequency": 800,
                "volume": 0.5
            }
        }

def signal_handler(signum: int, frame: Any) -> None:
    """Manejador de señales para limpieza al salir."""
    logger.info("Received signal to terminate")
    console.print("\n[yellow]Cleaning up and exiting...[/yellow]")
    raise typer.Exit()

# Registrar manejadores de señales
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Instancias globales - inicialización lazy
validator = None
converter = None
file_handler = None

def get_validator():
    """Obtener instancia de validator."""
    global validator
    if validator is None:
        validator = InputValidator()
    return validator

def get_converter():
    """Obtener instancia de converter."""
    global converter
    if converter is None:
        converter = MorseConverter()
    return converter

def get_file_handler():
    """Obtener instancia de file_handler."""
    global file_handler
    if file_handler is None:
        file_handler = FileHandler()
    return file_handler

def validate_frequency(frequency: int) -> int:
    """Validar que la frecuencia esté en un rango aceptable."""
    if not (20 <= frequency <= 20000):
        raise typer.BadParameter("Frequency must be between 20 and 20000 Hz")
    return frequency

# Inicializar las instancias
validator = get_validator()
converter = get_converter()
file_handler = get_file_handler()

@app.callback()
def app_callback():
    """Inicializar las dependencias cuando se ejecuta cualquier comando."""
    global config, validator, converter, file_handler
    if config is None:
        config = load_config()
    if validator is None:
        validator = get_validator()
    if converter is None:
        converter = get_converter()
    if file_handler is None:
        file_handler = get_file_handler()

@app.command()
def text_to_morse(
    text: str = typer.Argument(
        ...,
        help="Text to convert to Morse code. Supports A-Z, 0-9, and basic punctuation."
    ),
    output_file: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output file path to save the Morse code"
    ),
    play: bool = typer.Option(
        False,
        "--play", "-p",
        help="Play the Morse code as audio"
    ),
    frequency: int = typer.Option(
        800,
        "--frequency", "-f",
        help="Tone frequency in Hz (20-20000)",
        callback=validate_frequency
    )
) -> None:
    """
    Convert text to Morse code with optional audio playback.

    The input text is converted to Morse code using standard International Morse Code.
    The result can be displayed, saved to a file, and/or played as audio.
    """
    try:
        logger.info(f"Converting text to Morse: {text}")
        
        # Validar entrada
        validator.validate_text_input(text)
        
        # Convertir texto
        morse_code = converter.text_to_morse(text)
        
        # Mostrar resultado
        console.print(f"\n[green]Input Text:[/green] {text}")
        console.print(f"[green]Morse Code:[/green] {morse_code}\n")
        
        # Guardar en archivo si se especifica
        if output_file:
            file_handler.write_file(str(output_file), morse_code)
            console.print(f"[blue]Output saved to:[/blue] {output_file}")
        
        # Reproducir audio si se solicita
        if play:
            with Progress() as progress:
                task = progress.add_task(
                    "[cyan]Playing audio...[/cyan]",
                    total=100
                )
                
                generator = AudioGenerator(
                    frequency=frequency,
                    volume=config.get('audio', {}).get('volume', 0.5)
                )
                player = AudioPlayer(generator)
                
                audio_data = generator.generate_audio(morse_code)
                player.play_audio()
                
                progress.update(task, completed=100)
            
    except ValidationError as e:
        console.print(f"[red]Validation Error:[/red] {str(e)}")
        logger.error(f"Validation error: {str(e)}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        logger.error(f"Unexpected error: {str(e)}")
        raise typer.Exit(1)

@app.command()
def morse_to_text(
    morse: str = typer.Argument(
        ...,
        help="Morse code to convert to text. Use dots (.) and dashes (-) separated by spaces."
    ),
    output_file: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output file path to save the converted text"
    )
) -> None:
    """
    Convert Morse code to text.

    The input should be valid Morse code using dots (.) and dashes (-),
    with spaces between letters and double spaces between words.
    """
    try:
        logger.info(f"Converting Morse to text: {morse}")
        
        # Validar entrada
        validator.validate_morse_input(morse)
        
        # Convertir código Morse
        text = converter.morse_to_text(morse)
        
        # Mostrar resultado
        console.print(f"\n[green]Input Morse:[/green] {morse}")
        console.print(f"[green]Text:[/green] {text}\n")
        
        # Guardar en archivo si se especifica
        if output_file:
            file_handler.write_file(str(output_file), text)
            console.print(f"[blue]Output saved to:[/blue] {output_file}")
            
    except ValidationError as e:
        console.print(f"[red]Validation Error:[/red] {str(e)}")
        logger.error(f"Validation error: {str(e)}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        logger.error(f"Unexpected error: {str(e)}")
        raise typer.Exit(1)

@app.command()
def play_morse(
    morse: str = typer.Argument(
        ...,
        help="Morse code to play. Use dots (.) and dashes (-) separated by spaces."
    ),
    frequency: int = typer.Option(
        800,
        "--frequency", "-f",
        help="Tone frequency in Hz (20-20000)",
        callback=validate_frequency
    )
) -> None:
    """
    Play Morse code as audio.

    Converts the input Morse code to audio signals using the specified frequency.
    The timing follows standard Morse code conventions.
    """
    try:
        logger.info(f"Playing Morse code: {morse}")
        
        # Validar entrada
        validator.validate_morse_input(morse)
        
        # Configurar y reproducir audio
        with Progress() as progress:
            task = progress.add_task(
                "[cyan]Playing audio...[/cyan]",
                total=100
            )
            
            generator = AudioGenerator(
                frequency=frequency,
                volume=config.get('audio', {}).get('volume', 0.5)
            )
            player = AudioPlayer(generator)
            
            audio_data = generator.generate_audio(morse)
            player.play_audio()
            
            progress.update(task, completed=100)
            
    except ValidationError as e:
        console.print(f"[red]Validation Error:[/red] {str(e)}")
        logger.error(f"Validation error: {str(e)}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        logger.error(f"Unexpected error: {str(e)}")
        raise typer.Exit(1)

def main():
    """Entry point for the command-line interface."""
    global config, validator, converter, file_handler
    config = load_config()
    validator = get_validator()
    converter = get_converter()
    file_handler = get_file_handler()
    app()

if __name__ == "__main__":
    main()
