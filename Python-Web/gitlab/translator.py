#!/usr/bin/env python3

"""Prompt usado:

Haz un programa que traduzca un texto dado como argumento en la línea de 
comandos. Para hacer la traducción, usa una función que llame a la API 
de Langbly.
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import argparse
import sys
import os
from typing import Optional, Dict, Any

class LangblyTranslator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.langbly.com/language/translate/v2"
    
    def translate(self, text: str, target_lang: str = "en",
                  source_lang: str = "auto") -> Optional[Dict[str, Any]]:
        """
        Translate text using Langbly API
        
        Args:
            text: Text to translate
            target_lang: Target language code (e.g., 'en', 'es', 'fr')
            source_lang: Source language code (e.g., 'en', 'es', 'auto')
            
        Returns:
            Translation result dictionary or None if failed
        """
        if not self.api_key:
            print("Error: Se requiere una API key de Langbly")
            print("Obtén una en: https://langbly.com/dashboard/keys")
            return None
        
        # Prepare the request data
        data = {
            'q': text,
            'target': target_lang.lower()
        }
        
        if source_lang != "auto":
            data['source_language'] = source_lang.lower()
        
        try:
            # Create the request
            url = f"{self.base_url}"
            encoded_data = json.dumps(data).encode('utf-8')
            
            req = urllib.request.Request(url)
            req.add_header('Content-Type', 'application/json')
            req.add_header('X-API-Key', self.api_key)
            req.data = encoded_data
            req.get_method = lambda: 'POST'
            
            # Make the request
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result
                
        except urllib.error.URLError as e:
            print(f"Error de red: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error al procesar respuesta JSON: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None


def load_api_key_from_env() -> Optional[str]:
    """Load Langbly API key from .env file"""
    env_file = '.env'
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('LANGBLY_TOKEN='):
                        return line.split('=', 1)[1].strip().strip('"\'')
        except Exception as e:
            print(f"Error leyendo .env: {e}")
    return None

def main():
    parser = argparse.ArgumentParser(description='Traductor usando API de Langbly')
    parser.add_argument('text', nargs='*', help='Texto a traducir')
    parser.add_argument('--api-key', help='API key de Langbly')
    parser.add_argument('--from', dest='source_lang', default='auto', 
                       help='Idioma origen (default: auto)')
    parser.add_argument('--to', dest='target_lang', default='en', 
                       help='Idioma destino (default: en)')
    args = parser.parse_args()
        # Load API key from command line or .env
    api_key = args.api_key or load_api_key_from_env()
    
    if not api_key:
        print("Error: Se requiere una API key de Langbly")
        print("Obtén una API key en: https://langbly.com/dashboard/keys")
        print("Opciones:")
        print("  1. Usa --api-key TU_API_KEY")
        print("  2. Crea un archivo .env con: LANGBLY_TOKEN=TU_API_KEY")
        sys.exit(1)
    
    # Create translator instance
    translator = LangblyTranslator(api_key=api_key)

    # Get text to translate
    if not args.text:
        print("Error: Debes proporcionar un texto para traducir")
        print("Ejemplo: python3 translator.py \"Hola, mundo!\"")
        sys.exit(1)
    
    text = ' '.join(args.text)
    
    # Perform translation
    print(f"🔄 Traduciendo: \"{text}\"")
    print(f"📝 De: {args.source_lang} → A: {args.target_lang}")
    print("-" * 50)
    
    result = translator.translate(text, args.target_lang, args.source_lang)
    
    if result:
        if 'data' in result and 'translations' in result['data'] \
                and 'translatedText' in result['data']['translations'][0]:
            translations = result['data']['translations'][0]
            translated_text = translations['translatedText']
            detected_source = translations.get('detectedSourceLanguage', '')
            
            print(f"✅ Traducción:")
            print(f"   {translated_text}")
            
            if args.source_lang == 'auto' and detected_source:
                print(f"🔍 Idioma detectado: {detected_source}")
        else:
            print("❌ No se encontró texto traducido en la respuesta")
            print(f"Respuesta: {result}")
    else:
        print("❌ Error en la traducción")
        sys.exit(1)

if __name__ == "__main__":
    main()
