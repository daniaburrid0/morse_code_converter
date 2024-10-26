import pytest
from typer.testing import CliRunner
from unittest.mock import Mock, patch
from morse_converter.cli.interface import app
from morse_converter.cli.interface import ValidationError

# Configurar el runner de CLI para los tests
runner = CliRunner()

@pytest.fixture(autouse=True)
def mock_dependencies():
    """Fixture para mockear todas las dependencias."""
    # Primero, limpiar las instancias globales
    with patch('morse_converter.cli.interface.validator', None), \
         patch('morse_converter.cli.interface.converter', None), \
         patch('morse_converter.cli.interface.file_handler', None), \
         patch('morse_converter.cli.interface.config', {}):
        
        # Luego, mockear las clases
        with patch('morse_converter.cli.interface.InputValidator') as mock_validator, \
             patch('morse_converter.cli.interface.MorseConverter') as mock_converter, \
             patch('morse_converter.cli.interface.FileHandler') as mock_file_handler:
            
            # Configurar el comportamiento por defecto
            mock_validator_instance = Mock()
            mock_converter_instance = Mock()
            mock_file_handler_instance = Mock()
            
            # Configurar el comportamiento esperado para el test
            mock_converter_instance.text_to_morse.return_value = "... --- ..."
            
            mock_validator.return_value = mock_validator_instance
            mock_converter.return_value = mock_converter_instance
            mock_file_handler.return_value = mock_file_handler_instance
            
            yield {
                'validator': mock_validator,
                'converter': mock_converter,
                'file_handler': mock_file_handler
            }

def test_text_to_morse_basic(mock_dependencies):
    """Test básico del comando text-to-morse."""
    result = runner.invoke(app, ["text-to-morse", "SOS"])
    
    assert result.exit_code == 0
    assert "... --- ..." in result.stdout
    
    # Verificar que se llamaron los métodos correctos
    mock_dependencies['validator'].return_value.validate_text_input.assert_called_once_with("SOS")
    mock_dependencies['converter'].return_value.text_to_morse.assert_called_once_with("SOS")

def test_text_to_morse_validation_error(mock_dependencies):
    """Test del manejo de errores de validación en text-to-morse."""
    # Configurar el mock para lanzar un error de validación
    mock_dependencies['validator'].return_value.validate_text_input.side_effect = \
        ValidationError("Invalid character '#' in input")
    
    result = runner.invoke(app, ["text-to-morse", "SO#S"])
    
    # Verificar que el comando falló apropiadamente
    assert result.exit_code == 1
    
    # Verificar que se mostró el mensaje de error
    assert "Validation Error" in result.stdout
    assert "Invalid character '#' in input" in result.stdout
    
    # Verificar que se llamó al validator pero no al converter
    mock_dependencies['validator'].return_value.validate_text_input.assert_called_once_with("SO#S")
    mock_dependencies['converter'].return_value.text_to_morse.assert_not_called()

def test_text_to_morse_with_output_file(mock_dependencies, tmp_path):
    """Test de conversión a Morse con guardado en archivo."""
    # Preparar el path temporal para el archivo de salida
    output_file = tmp_path / "morse_output.txt"
    
    # Configurar el comportamiento esperado
    morse_result = "... --- ..."
    mock_dependencies['converter'].return_value.text_to_morse.return_value = morse_result
    
    # Ejecutar el comando con la opción de output
    result = runner.invoke(app, [
        "text-to-morse", 
        "SOS",
        "--output", str(output_file)
    ])
    
    # Verificar la ejecución exitosa
    assert result.exit_code == 0
    assert morse_result in result.stdout
    
    # Verificar que se llamaron los métodos correctos
    mock_dependencies['validator'].return_value.validate_text_input.assert_called_once_with("SOS")
    mock_dependencies['converter'].return_value.text_to_morse.assert_called_once_with("SOS")
    mock_dependencies['file_handler'].return_value.write_file.assert_called_once_with(
        str(output_file),
        morse_result
    )
    
    # Verificar que el mensaje de salida contiene el path
    assert "Output saved to:" in result.stdout
    # Verificar solo el nombre del archivo final
    assert "morse_output.txt" in result.stdout.lower()
    
    # Alternativa: normalizar la salida eliminando saltos de línea
    normalized_output = result.stdout.lower().replace('\n', '')
    assert str(output_file).lower() in normalized_output

def test_morse_to_text_basic(mock_dependencies):
    """Test básico del comando morse-to-text."""
    # Configurar el comportamiento esperado
    mock_dependencies['converter'].return_value.morse_to_text.return_value = "SOS"
    
    # Ejecutar el comando
    result = runner.invoke(app, ["morse-to-text", "... --- ..."])
    
    # Verificar la ejecución exitosa
    assert result.exit_code == 0
    assert "SOS" in result.stdout
    
    # Verificar que se llamaron los métodos correctos
    mock_dependencies['validator'].return_value.validate_morse_input.assert_called_once_with("... --- ...")
    mock_dependencies['converter'].return_value.morse_to_text.assert_called_once_with("... --- ...")

def test_morse_to_text_with_output_file(mock_dependencies, tmp_path):
    """Test de conversión de Morse a texto con guardado en archivo."""
    # Preparar el path temporal para el archivo de salida
    output_file = tmp_path / "text_output.txt"
    
    # Configurar el comportamiento esperado
    text_result = "SOS"
    mock_dependencies['converter'].return_value.morse_to_text.return_value = text_result
    
    # Ejecutar el comando con la opción de output
    result = runner.invoke(app, [
        "morse-to-text",
        "... --- ...",
        "--output", str(output_file)
    ])
    
    # Verificar la ejecución exitosa
    assert result.exit_code == 0
    assert text_result in result.stdout
    
    # Verificar que se llamaron los métodos correctos
    mock_dependencies['validator'].return_value.validate_morse_input.assert_called_once_with("... --- ...")
    mock_dependencies['converter'].return_value.morse_to_text.assert_called_once_with("... --- ...")
    mock_dependencies['file_handler'].return_value.write_file.assert_called_once_with(
        str(output_file),
        text_result
    )
    
    # Verificar que el mensaje de salida contiene el path
    assert "Output saved to:" in result.stdout
    # Verificar solo el nombre del archivo final
    assert "text_output.txt" in result.stdout.lower()
    
    # Normalizar la salida para verificar el path completo
    normalized_output = result.stdout.lower().replace('\n', '')
    assert str(output_file).lower() in normalized_output

def test_play_morse_basic(mock_dependencies):
    """Test básico del comando play-morse."""
    # Configurar el comportamiento esperado
    morse_code = "... --- ..."
    
    # Mockear AudioGenerator y AudioPlayer
    with patch('morse_converter.cli.interface.AudioGenerator') as mock_audio_generator, \
         patch('morse_converter.cli.interface.AudioPlayer') as mock_audio_player:
        
        # Configurar los mocks de audio
        mock_generator_instance = Mock()
        mock_player_instance = Mock()
        
        mock_audio_generator.return_value = mock_generator_instance
        mock_audio_player.return_value = mock_player_instance
        
        # Ejecutar el comando
        result = runner.invoke(app, ["play-morse", morse_code])
        
        # Verificar la ejecución exitosa
        assert result.exit_code == 0
        
        # Verificar que se llamaron los métodos correctos
        mock_dependencies['validator'].return_value.validate_morse_input.assert_called_once_with(morse_code)
        
        # Verificar la configuración del audio
        mock_audio_generator.assert_called_once_with(
            frequency=800,  # Frecuencia por defecto
            volume=0.5      # Volumen por defecto
        )
        
        # Verificar que se generó y reprodujo el audio
        mock_generator_instance.generate_audio.assert_called_once_with(morse_code)
        mock_player_instance.play_audio.assert_called_once()
        
        # Verificar que se muestra el progreso
        assert "Playing audio..." in result.stdout

def test_play_morse_validation_error(mock_dependencies):
    """Test del manejo de errores de validación en play-morse."""
    # Configurar el mock para lanzar un error de validación
    mock_dependencies['validator'].return_value.validate_morse_input.side_effect = \
        ValidationError("Invalid Morse pattern '***'")
    
    # Mockear AudioGenerator y AudioPlayer
    with patch('morse_converter.cli.interface.AudioGenerator') as mock_audio_generator, \
         patch('morse_converter.cli.interface.AudioPlayer') as mock_audio_player:
        
        # Configurar los mocks de audio
        mock_generator_instance = Mock()
        mock_player_instance = Mock()
        
        mock_audio_generator.return_value = mock_generator_instance
        mock_audio_player.return_value = mock_player_instance
        
        # Ejecutar el comando con entrada inválida
        result = runner.invoke(app, ["play-morse", "... *** ..."])
        
        # Verificar que el comando falló apropiadamente
        assert result.exit_code == 1
        
        # Verificar que se mostró el mensaje de error
        assert "Validation Error" in result.stdout
        assert "Invalid Morse pattern '***'" in result.stdout
        
        # Verificar que se llamó al validator pero no al audio
        mock_dependencies['validator'].return_value.validate_morse_input.assert_called_once_with("... *** ...")
        mock_audio_generator.assert_not_called()
        mock_player_instance.play_audio.assert_not_called()
        
        # Verificar que se registró el error
        mock_dependencies['validator'].return_value.validate_morse_input.assert_called_once()
