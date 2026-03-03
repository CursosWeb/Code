#!/usr/bin/env python3
import unittest
import urllib.request
import urllib.parse
import urllib.error
import json
import re
import subprocess
import time
import signal
import os
from threading import Thread

class TestCalculadorasServer(unittest.TestCase):
    """Tests HTTP endpoints of the calculator application"""
    
    @classmethod
    def setUpClass(cls):
        """Connect to existing server"""
        cls.server_port = 8004  # Use port where server is running
        cls.server_url = f"http://localhost:{cls.server_port}"
        
        # Verify server is running
        try:
            response = urllib.request.urlopen(f"{cls.server_url}/")
            cls.server_running = True
        except urllib.error.URLError:
            cls.server_running = False
            raise Exception("Server is not running on port 8004")
    
    @classmethod
    def tearDownClass(cls):
        """No cleanup needed - using existing server"""
        pass
    
    def make_request(self, method, path, data=None):
        """Helper method to make HTTP requests"""
        url = f"{self.server_url}{path}"
        
        if method == 'GET':
            req = urllib.request.Request(url)
        elif method == 'POST':
            req = urllib.request.Request(url, data=data.encode('utf-8') if data else None)
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        try:
            with urllib.request.urlopen(req) as response:
                return response.read().decode('utf-8'), response.getcode()
        except urllib.error.HTTPError as e:
            return e.read().decode('utf-8'), e.getcode()
    
    def extract_calculator_id(self, response_body, calc_type):
        """Helper method to extract calculator ID from main page"""
        # Look for specific pattern with exact type match
        pattern = rf'<a href="/calcs/([a-f0-9]+)">Calculadora \1</a> - Tipo: {calc_type}</a>'
        match = re.search(pattern, response_body)
        if match:
            return match.group(1)
        
        # If not found, try to find the last calculator of the specified type
        lines = response_body.split('\n')
        for line in lines:
            if f'Tipo: {calc_type}' in line and '<a href="/calcs/' in line:
                id_match = re.search(r'/calcs/([a-f0-9]+)"', line)
                if id_match:
                    return id_match.group(1)
        
        return None
    
    def test_get_main_page(self):
        """Test GET / returns HTML with form and calculator list"""
        response_body, status_code = self.make_request('GET', '/')
        
        # Check status code
        self.assertEqual(status_code, 200)
        
        # Check HTML structure
        self.assertIn('<!DOCTYPE html>', response_body)
        self.assertIn('<title>Calculadoras</title>', response_body)
        self.assertIn('<h1>Calculadoras</h1>', response_body)
        
        # Check form for creating calculators
        self.assertIn('<form method="POST" action="/">', response_body)
        self.assertIn('<select id="tipo" name="crear">', response_body)
        self.assertIn('<option value="iva">Calculadora de IVA</option>', response_body)
        self.assertIn('<option value="suma">Calculadora de Sumas</option>', response_body)
        self.assertIn('<button type="submit">Crear Nueva Calculadora</button>', response_body)
        
        # Check calculator list section
        self.assertTrue('No hay calculadoras creadas aún' in response_body or 'Calculadoras existentes:' in response_body)
    
    def test_post_create_iva_calculator(self):
        """Test POST / creates IVA calculator"""
        response_body, status_code = self.make_request('POST', '/', 'crear=iva')
        
        # Check status code
        self.assertEqual(status_code, 200)
        
        # Check response content
        self.assertIn('<h1>Calculadora Creada</h1>', response_body)
        self.assertIn('tipo <strong>iva</strong>', response_body)
        self.assertIn('ID: <strong>', response_body)
        self.assertIn('<a href="/calcs/', response_body)
        
        # Extract calculator ID for later tests
        id_match = re.search(r'ID: <strong>([a-f0-9]+)</strong>', response_body)
        self.assertIsNotNone(id_match, "Calculator ID not found in response")
        self.iva_calculator_id = id_match.group(1)
    
    def test_post_create_suma_calculator(self):
        """Test POST / creates suma calculator"""
        response_body, status_code = self.make_request('POST', '/', 'crear=suma')
        
        # Check status code
        self.assertEqual(status_code, 200)
        
        # Check response content
        self.assertIn('<h1>Calculadora Creada</h1>', response_body)
        self.assertIn('tipo <strong>suma</strong>', response_body)
        self.assertIn('ID: <strong>', response_body)
        self.assertIn('<a href="/calcs/', response_body)
        
        # Extract calculator ID for later tests
        id_match = re.search(r'ID: <strong>([a-f0-9]+)</strong>', response_body)
        self.assertIsNotNone(id_match, "Calculator ID not found in response")
        self.suma_calculator_id = id_match.group(1)
    
    def test_post_create_invalid_calculator(self):
        """Test POST / with invalid calculator type returns error"""
        response_body, status_code = self.make_request('POST', '/', 'crear=invalid')
        
        # Should return 400 Bad Request
        self.assertEqual(status_code, 400)
    
    def test_get_calculator_form_iva(self):
        """Test GET /calcs/<id> returns IVA calculator form"""
        # First create an IVA calculator and get the ID from response
        response_body, _ = self.make_request('POST', '/', 'crear=iva')
        id_match = re.search(r'ID: <strong>([a-f0-9]+)</strong>', response_body)
        self.assertIsNotNone(id_match, "Calculator ID not found in response")
        calc_id = id_match.group(1)
        
        # Get calculator form
        response_body, status_code = self.make_request('GET', f'/calcs/{calc_id}')
        
        # Check status code
        self.assertEqual(status_code, 200)
        
        # Check IVA calculator form
        self.assertIn('<h1>Calculadora de IVA - ID:', response_body)
        self.assertIn(f'ID: {calc_id}</h1>', response_body)
        self.assertIn('<form method="POST" action="/calcs/' + calc_id + '">', response_body)
        self.assertIn('<label for="valor">Cantidad para calcular IVA:</label>', response_body)
        self.assertIn('<input type="number" id="valor" name="valor"', response_body)
        self.assertIn('<button type="submit">Calcular IVA</button>', response_body)
    
    def test_get_calculator_form_suma(self):
        """Test GET /calcs/<id> returns suma calculator form"""
        # First create a suma calculator and get the ID from response
        response_body, _ = self.make_request('POST', '/', 'crear=suma')
        id_match = re.search(r'ID: <strong>([a-f0-9]+)</strong>', response_body)
        self.assertIsNotNone(id_match, "Calculator ID not found in response")
        calc_id = id_match.group(1)
        
        # Get calculator form
        response_body, status_code = self.make_request('GET', f'/calcs/{calc_id}')
        
        # Check status code
        self.assertEqual(status_code, 200)
        
        # Check suma calculator form
        self.assertIn('<h1>Calculadora de Sumas - ID:', response_body)
        self.assertIn(f'ID: {calc_id}</h1>', response_body)
        self.assertIn('<form method="POST" action="/calcs/' + calc_id + '">', response_body)
        self.assertIn('<label for="sum1">Primer número:</label>', response_body)
        self.assertIn('<label for="sum2">Segundo número:</label>', response_body)
        self.assertIn('<input type="number" id="sum1" name="sum1"', response_body)
        self.assertIn('<input type="number" id="sum2" name="sum2"', response_body)
        self.assertIn('<button type="submit">Calcular Suma</button>', response_body)
    
    def test_post_calculate_iva(self):
        """Test POST /calcs/<id> calculates IVA correctly"""
        # First create an IVA calculator and get the ID from response
        response_body, _ = self.make_request('POST', '/', 'crear=iva')
        id_match = re.search(r'ID: <strong>([a-f0-9]+)</strong>', response_body)
        self.assertIsNotNone(id_match, "Calculator ID not found in response")
        calc_id = id_match.group(1)
        
        # Calculate IVA for 100
        response_body, status_code = self.make_request('POST', f'/calcs/{calc_id}', 'valor=100')
        
        # Check status code
        self.assertEqual(status_code, 200)
        
        # Check calculation result
        self.assertIn('<h2>Resultado</h2>', response_body)
        self.assertIn('Cantidad original: <strong>100.00€</strong>', response_body)
        self.assertIn('IVA (21%): <strong>21.00€</strong>', response_body)
        self.assertIn('Total con IVA: <strong>121.00€</strong>', response_body)
        
        # Check form is still present for new calculations
        self.assertIn('<h3>Calcular otra cantidad</h3>', response_body)
        self.assertIn('<form method="POST" action="/calcs/' + calc_id + '">', response_body)
    
    def test_post_calculate_suma(self):
        """Test POST /calcs/<id> calculates sum correctly"""
        # First create a suma calculator and get the ID from response
        response_body, _ = self.make_request('POST', '/', 'crear=suma')
        id_match = re.search(r'ID: <strong>([a-f0-9]+)</strong>', response_body)
        self.assertIsNotNone(id_match, "Calculator ID not found in response")
        calc_id = id_match.group(1)
        
        # Calculate sum for 50 + 75
        response_body, status_code = self.make_request('POST', f'/calcs/{calc_id}', 'sum1=50&sum2=75')
        
        # Check status code
        self.assertEqual(status_code, 200)
        
        # Check calculation result
        self.assertIn('<h2>Resultado</h2>', response_body)
        self.assertIn('Primer número: <strong>50.00</strong>', response_body)
        self.assertIn('Segundo número: <strong>75.00</strong>', response_body)
        self.assertIn('Suma: <strong>125.00</strong>', response_body)
        
        # Check form is still present for new calculations
        self.assertIn('<h3>Calcular otra suma</h3>', response_body)
        self.assertIn('<form method="POST" action="/calcs/' + calc_id + '">', response_body)
    
    def test_get_invalid_calculator_id(self):
        """Test GET /calcs/<invalid_id> returns 404"""
        response_body, status_code = self.make_request('GET', '/calcs/invalidid')
        
        # Should return 404 Not Found
        self.assertEqual(status_code, 404)
    
    def test_post_invalid_calculator_id(self):
        """Test POST /calcs/<invalid_id> returns 404"""
        response_body, status_code = self.make_request('POST', '/calcs/invalidid', 'valor=100')
        
        # Should return 404 Not Found
        self.assertEqual(status_code, 404)
    
    def test_post_invalid_path(self):
        """Test POST to invalid path returns 404"""
        response_body, status_code = self.make_request('POST', '/invalidpath', 'data=test')
        
        # Should return 404 Not Found
        self.assertEqual(status_code, 404)
    
    def test_get_invalid_path(self):
        """Test GET to invalid path returns 404"""
        response_body, status_code = self.make_request('GET', '/invalidpath')
        
        # Should return 404 Not Found
        self.assertEqual(status_code, 404)
    
    def test_calculator_list_updates(self):
        """Test that main page shows updated calculator list"""
        # Get initial state (should be empty or have previous calculators)
        initial_response, _ = self.make_request('GET', '/')
        
        # Create a new calculator
        _, _ = self.make_request('POST', '/', 'crear=iva')
        
        # Get updated main page
        updated_response, _ = self.make_request('GET', '/')
        
        # Should contain calculator list
        self.assertIn('Calculadoras existentes:', updated_response)
        self.assertIn('<a href="/calcs/', updated_response)
        self.assertIn('Tipo: iva', updated_response)
    
    def test_invalid_numeric_input_iva(self):
        """Test POST /calcs/<id> with invalid numeric input for IVA"""
        # First create an IVA calculator and get the ID from response
        response_body, _ = self.make_request('POST', '/', 'crear=iva')
        id_match = re.search(r'ID: <strong>([a-f0-9]+)</strong>', response_body)
        self.assertIsNotNone(id_match, "Calculator ID not found in response")
        calc_id = id_match.group(1)
        
        # Try to calculate with invalid input
        response_body, status_code = self.make_request('POST', f'/calcs/{calc_id}', 'valor=invalid')
        
        # Should return 400 Bad Request
        self.assertEqual(status_code, 400)
    
    def test_invalid_numeric_input_suma(self):
        """Test POST /calcs/<id> with invalid numeric input for suma"""
        # First create a suma calculator and get the ID from response
        response_body, _ = self.make_request('POST', '/', 'crear=suma')
        id_match = re.search(r'ID: <strong>([a-f0-9]+)</strong>', response_body)
        self.assertIsNotNone(id_match, "Calculator ID not found in response")
        calc_id = id_match.group(1)
        
        # Try to calculate with invalid input
        response_body, status_code = self.make_request('POST', f'/calcs/{calc_id}', 'sum1=invalid&sum2=50')
        
        # Should return 400 Bad Request
        self.assertEqual(status_code, 400)

if __name__ == '__main__':
    unittest.main()
