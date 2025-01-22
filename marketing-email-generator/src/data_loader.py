import csv
from typing import Dict, Any, List

# Field definitions for different data types
FIELD_DEFINITIONS = {
    'target': {
        'company', 'industry', 'category', 'subcategory',
        'phone', 'email', 'website', 'facebook', 'instagram',
        'twitter', 'linkedin', 'address', 'rating'
    },
    'sender': {
        'sender_summary', 'sender_company', 'sender_website',
        'sender_email', 'sender_full_name', 'sender_title',
        'sender_phone'
    }
}

def ensure_fields(data: dict, field_type: str) -> dict:
    """
    Generic function to ensure all fields of a specific type exist.
    """
    if field_type not in FIELD_DEFINITIONS:
        raise ValueError(f"Unknown field type: {field_type}")
        
    required_fields = FIELD_DEFINITIONS[field_type]
    
    # Create base dictionary with empty strings
    base_dict = {field: '' for field in required_fields}
    
    # Update with cleaned data
    cleaned_data = {
        key: str(value).strip() if value is not None else ''
        for key, value in data.items()
    }
    
    base_dict.update(cleaned_data)
    return base_dict

def load_sender_info(sender_csv_path: str) -> Dict[str, str]:
    """
    Load and validate sender information from CSV.
    """
    try:
        with open(sender_csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            sender_data = next(reader)
            return ensure_fields(sender_data, 'sender')
            
    except FileNotFoundError:
        raise FileNotFoundError(f"Sender CSV file not found: {sender_csv_path}")
    except Exception as e:
        raise Exception(f"Error loading sender information: {e}")

def load_target_info(targets_csv_path: str) -> List[Dict[str, str]]:
    """
    Load and validate target companies information from CSV.
    """
    try:
        targets = []
        with open(targets_csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                complete_data = ensure_fields(row, 'target')
                targets.append(complete_data)
        return targets
            
    except FileNotFoundError:
        raise FileNotFoundError(f"Targets CSV file not found: {targets_csv_path}")
    except Exception as e:
        raise Exception(f"Error loading target information: {e}") 