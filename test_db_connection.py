#!/usr/bin/env python3
"""
Simple test script to verify database connection and table structure
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.db.conection import DatabaseConnection

def test_database_connection():
    """Test the database connection"""
    try:
        print("Testing database connection...")
        db = DatabaseConnection()
        
        # Test basic connection
        print("✓ Database connection established successfully")
        
        # Test table existence
        query = """
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'sensor_data_raw'
        ORDER BY ordinal_position;
        """
        
        result = db.execute_query(query)
        columns = result.fetchall()
        
        if columns:
            print("✓ Table 'sensor_data_raw' found with columns:")
            for column in columns:
                print(f"  - {column[0]} ({column[1]})")
        else:
            print("⚠ Table 'sensor_data_raw' not found. Please create it using:")
            print("""
            CREATE TABLE sensor_data_raw (
              id_sensor SERIAL PRIMARY KEY,
              type_sensor VARCHAR(50) NULL,
              sensor_value VARCHAR(50) NULL,
              date_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL
            );
            """)
        
        # Test insert functionality (optional)
        print("\nTesting data insertion...")
        test_data = db.insert_sensor_data("temperature", "25.5")
        print(f"✓ Test data inserted successfully: {test_data}")
        
        db.close_connection()
        print("✓ Database connection closed successfully")
        
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_database_connection()