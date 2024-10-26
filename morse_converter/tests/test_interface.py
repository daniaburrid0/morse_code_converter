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
