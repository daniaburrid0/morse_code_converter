# English Prompt

Create a Morse Code Converter application with the following structure. Include detailed docstrings explaining the purpose and functionality of each component, but leave the implementation empty or with pass statements. The program should follow a mixed paradigm (OOP and functional) and be organized in a modular way.

## Project Structure:
```
morse_converter/
├── __init__.py
├── config/
│   ├── __init__.py
│   └── config.json
├── core/
│   ├── __init__.py
│   ├── converter.py       # Main conversion logic
│   ├── audio.py          # Audio generation
│   └── validator.py      # Input validation
├── cli/
│   ├── __init__.py
│   └── interface.py      # CLI implementation
├── utils/
│   ├── __init__.py
│   ├── file_handler.py   # File operations
│   └── logger.py         # Logging system
├── practice/
│   ├── __init__.py
│   ├── exercises.py      # Practice system
│   └── progress.py       # Progress tracking
├── tests/
│   ├── __init__.py
│   ├── test_converter.py
│   ├── test_audio.py
│   └── test_exercises.py
├── main.py
└── requirements.txt
```

For each file, generate the class and function structures with detailed docstrings that explain:
- Purpose of the class/function
- Parameters and their types
- Return values and their types
- Exceptions that might be raised
- Usage examples in docstrings

Key requirements:
1. Use Typer for CLI interface (modern, type-hint based CLI framework)
2. Implement pytest for testing
3. Use JSON for configuration
4. Include type hints for all functions
5. Follow PEP 8 style guidelines
6. Include proper error handling
7. Implement logging

The docstrings should be detailed enough that another developer could understand what needs to be implemented without seeing the actual code.

Let me know when you want to start with a specific file, and I'll provide the structure with complete docstrings for that component.

---

# Prompt en Español

Crea una aplicación Convertidor de Código Morse con la siguiente estructura. Incluye docstrings detallados que expliquen el propósito y funcionalidad de cada componente, pero deja la implementación vacía o con declaraciones pass. El programa debe seguir un paradigma mixto (POO y funcional) y estar organizado de forma modular.

## Estructura del Proyecto:
```
morse_converter/
├── __init__.py
├── config/
│   ├── __init__.py
│   └── config.json
├── core/
│   ├── __init__.py
│   ├── converter.py       # Lógica principal de conversión
│   ├── audio.py          # Generación de audio
│   └── validator.py      # Validación de entrada
├── cli/
│   ├── __init__.py
│   └── interface.py      # Implementación de CLI
├── utils/
│   ├── __init__.py
│   ├── file_handler.py   # Operaciones con archivos
│   └── logger.py         # Sistema de logging
├── practice/
│   ├── __init__.py
│   ├── exercises.py      # Sistema de práctica
│   └── progress.py       # Seguimiento de progreso
├── tests/
│   ├── __init__.py
│   ├── test_converter.py
│   ├── test_audio.py
│   └── test_exercises.py
├── main.py
└── requirements.txt
```

Para cada archivo, genera las estructuras de clases y funciones con docstrings detallados que expliquen:
- Propósito de la clase/función
- Parámetros y sus tipos
- Valores de retorno y sus tipos
- Excepciones que podrían generarse
- Ejemplos de uso en los docstrings

Requisitos clave:
1. Usar Typer para la interfaz CLI (framework CLI moderno basado en type-hints)
2. Implementar pytest para testing
3. Usar JSON para configuración
4. Incluir type hints para todas las funciones
5. Seguir las guías de estilo PEP 8
6. Incluir manejo de errores apropiado
7. Implementar logging

Los docstrings deben ser lo suficientemente detallados para que otro desarrollador pueda entender qué necesita ser implementado sin ver el código actual.

Avísame cuando quieras empezar con un archivo específico y te proporcionaré la estructura con docstrings completos para ese componente.

