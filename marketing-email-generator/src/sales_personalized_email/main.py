#!/usr/bin/env python
import sys
import csv
from sales_personalized_email.crew import SalesPersonalizedEmailCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def load_sender_info(sender_csv_path: str) -> dict:
    """
    Load sender company information from a CSV file.
    
    Args:
        sender_csv_path: Path to the sender information CSV file
        
    Returns:
        Dictionary containing sender company information
    """
    try:
        with open(sender_csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # Assuming first row contains the sender information
            sender_info = next(reader)
            return {k: v.strip() for k, v in sender_info.items() if v and v.strip()}
            
    except FileNotFoundError:
        raise FileNotFoundError(f"Sender CSV file not found: {sender_csv_path}")
    except Exception as e:
        raise Exception(f"Error loading sender information: {e}")

def run():
    """
    Run the crew for multiple companies from CSV files.
    Processes target companies using sender company information.
    
    Required files:
    - targets.csv: Contains information about target companies
    - sender.csv: Contains information about the sender company
    
    Usage:
    python main.py targets.csv sender.csv
    """
    try:
        # Get file paths from command line arguments or use defaults
        targets_csv = sys.argv[1] if len(sys.argv) > 1 else "targets.csv"
        sender_csv = sys.argv[2] if len(sys.argv) > 2 else "sender.csv"
        
        # Load sender information first
        sender_info = load_sender_info(sender_csv)
        
        # Process target companies
        with open(targets_csv, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row_num, target_data in enumerate(reader, start=1):
                try:
                    print(f"\nProcessing company {row_num}: {target_data.get('company', 'Unknown')}")
                    
                    # Clean target company data
                    cleaned_target = {
                        key: value.strip() 
                        for key, value in target_data.items() 
                        if value and value.strip()
                    }
                    
                    # Combine target and sender information
                    inputs = {**cleaned_target, **sender_info}
                    
                    # Generate email
                    SalesPersonalizedEmailCrew().crew().kickoff(inputs=inputs)
                    
                except Exception as company_error:
                    print(f"Error processing company {row_num}: {company_error}")
                    continue  # Continue with next company if one fails
                    
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing files: {e}")
        sys.exit(1)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        SalesPersonalizedEmailCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SalesPersonalizedEmailCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"company_name": "AI LLMs"}
    try:
        SalesPersonalizedEmailCrew().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
