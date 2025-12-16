import requests
import random
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
ENDPOINT = "/api/v1/iothumedad/insert"

def generate_random_humidity():
    """Generate a random humidity value between 20% and 90%"""
    return round(random.uniform(20.0, 90.0), 2)

def generate_random_temperature():
    """Generate a random temperature value between 15°C and 35°C"""
    return round(random.uniform(15.0, 35.0), 2)

def test_successful_insertion():
    """Test successful insertion with valid data"""
    print("\n" + "="*60)
    print("TEST 1: Successful insertion with valid data")
    print("="*60)
    
    humedad = generate_random_humidity()
    temperatura = generate_random_temperature()
    
    params = {
        'sensor_value_humedad': humedad,
        'sensor_value_temperatura': temperatura
    }
    
    print(f"Sending request with:")
    print(f"  - Humidity: {humedad}%")
    print(f"  - Temperature: {temperatura}°C")
    
    try:
        response = requests.get(f"{BASE_URL}{ENDPOINT}", params=params)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✓ Test PASSED")
        else:
            print("✗ Test FAILED")
    except Exception as e:
        print(f"✗ Test FAILED with error: {e}")

def test_missing_humidity():
    """Test with missing humidity parameter"""
    print("\n" + "="*60)
    print("TEST 2: Missing humidity parameter")
    print("="*60)
    
    params = {
        'sensor_value_temperatura': generate_random_temperature()
    }
    
    print(f"Sending request with only temperature: {params['sensor_value_temperatura']}°C")
    
    try:
        response = requests.get(f"{BASE_URL}{ENDPOINT}", params=params)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400:
            print("✓ Test PASSED - Error handled correctly")
        else:
            print("✗ Test FAILED - Should return 400")
    except Exception as e:
        print(f"✗ Test FAILED with error: {e}")

def test_missing_temperature():
    """Test with missing temperature parameter"""
    print("\n" + "="*60)
    print("TEST 3: Missing temperature parameter")
    print("="*60)
    
    params = {
        'sensor_value_humedad': generate_random_humidity()
    }
    
    print(f"Sending request with only humidity: {params['sensor_value_humedad']}%")
    
    try:
        response = requests.get(f"{BASE_URL}{ENDPOINT}", params=params)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400:
            print("✓ Test PASSED - Error handled correctly")
        else:
            print("✗ Test FAILED - Should return 400")
    except Exception as e:
        print(f"✗ Test FAILED with error: {e}")

def test_invalid_humidity():
    """Test with invalid (non-numeric) humidity value"""
    print("\n" + "="*60)
    print("TEST 4: Invalid humidity value (non-numeric)")
    print("="*60)
    
    params = {
        'sensor_value_humedad': 'invalid_value',
        'sensor_value_temperatura': generate_random_temperature()
    }
    
    print(f"Sending request with:")
    print(f"  - Humidity: {params['sensor_value_humedad']} (invalid)")
    print(f"  - Temperature: {params['sensor_value_temperatura']}°C")
    
    try:
        response = requests.get(f"{BASE_URL}{ENDPOINT}", params=params)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400:
            print("✓ Test PASSED - Error handled correctly")
        else:
            print("✗ Test FAILED - Should return 400")
    except Exception as e:
        print(f"✗ Test FAILED with error: {e}")

def test_invalid_temperature():
    """Test with invalid (non-numeric) temperature value"""
    print("\n" + "="*60)
    print("TEST 5: Invalid temperature value (non-numeric)")
    print("="*60)
    
    params = {
        'sensor_value_humedad': generate_random_humidity(),
        'sensor_value_temperatura': 'not_a_number'
    }
    
    print(f"Sending request with:")
    print(f"  - Humidity: {params['sensor_value_humedad']}%")
    print(f"  - Temperature: {params['sensor_value_temperatura']} (invalid)")
    
    try:
        response = requests.get(f"{BASE_URL}{ENDPOINT}", params=params)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400:
            print("✓ Test PASSED - Error handled correctly")
        else:
            print("✗ Test FAILED - Should return 400")
    except Exception as e:
        print(f"✗ Test FAILED with error: {e}")

def test_extreme_values():
    """Test with extreme but valid values"""
    print("\n" + "="*60)
    print("TEST 6: Extreme values")
    print("="*60)
    
    params = {
        'sensor_value_humedad': 0.0,
        'sensor_value_temperatura': 100.0
    }
    
    print(f"Sending request with:")
    print(f"  - Humidity: {params['sensor_value_humedad']}%")
    print(f"  - Temperature: {params['sensor_value_temperatura']}°C")
    
    try:
        response = requests.get(f"{BASE_URL}{ENDPOINT}", params=params)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✓ Test PASSED")
        else:
            print("✗ Test FAILED")
    except Exception as e:
        print(f"✗ Test FAILED with error: {e}")

def test_multiple_insertions():
    """Test multiple rapid insertions to simulate real sensor behavior"""
    print("\n" + "="*60)
    print("TEST 7: Multiple rapid insertions (simulating sensor data)")
    print("="*60)
    
    num_insertions = 5
    print(f"Inserting {num_insertions} random sensor readings...")
    
    successful = 0
    failed = 0
    
    for i in range(num_insertions):
        humedad = generate_random_humidity()
        temperatura = generate_random_temperature()
        
        params = {
            'sensor_value_humedad': humedad,
            'sensor_value_temperatura': temperatura
        }
        
        print(f"\n  Reading #{i+1}: Humidity={humedad}%, Temperature={temperatura}°C")
        
        try:
            response = requests.get(f"{BASE_URL}{ENDPOINT}", params=params)
            if response.status_code == 200:
                data = response.json()
                print(f"    ✓ Inserted successfully (ID: {data['data']['data']['id_sensor']})")
                successful += 1
            else:
                print(f"    ✗ Failed: {response.json()}")
                failed += 1
        except Exception as e:
            print(f"    ✗ Error: {e}")
            failed += 1
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.2)
    
    print(f"\nResults: {successful} successful, {failed} failed")
    if successful == num_insertions:
        print("✓ Test PASSED - All insertions successful")
    else:
        print(f"✗ Test PARTIALLY FAILED - {failed} insertions failed")

def test_negative_values():
    """Test with negative values"""
    print("\n" + "="*60)
    print("TEST 8: Negative values")
    print("="*60)
    
    params = {
        'sensor_value_humedad': -10.5,
        'sensor_value_temperatura': -5.0
    }
    
    print(f"Sending request with:")
    print(f"  - Humidity: {params['sensor_value_humedad']}%")
    print(f"  - Temperature: {params['sensor_value_temperatura']}°C")
    
    try:
        response = requests.get(f"{BASE_URL}{ENDPOINT}", params=params)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✓ Test PASSED - Negative values accepted")
        else:
            print("✗ Test FAILED")
    except Exception as e:
        print(f"✗ Test FAILED with error: {e}")

def run_all_tests():
    """Run all test cases"""
    print("\n" + "="*60)
    print("STARTING HUMIDITY SENSOR ENDPOINT TESTS")
    print(f"Testing endpoint: {BASE_URL}{ENDPOINT}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/v1/iothumedad/")
        print(f"✓ Server is running (Status: {response.status_code})")
    except Exception as e:
        print(f"✗ Cannot connect to server: {e}")
        print("Please make sure the Flask server is running on http://localhost:5000")
        return
    
    # Run all tests
    test_successful_insertion()
    test_missing_humidity()
    test_missing_temperature()
    test_invalid_humidity()
    test_invalid_temperature()
    test_extreme_values()
    test_negative_values()
    test_multiple_insertions()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)

if __name__ == "__main__":
    run_all_tests()
