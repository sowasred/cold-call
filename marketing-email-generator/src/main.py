#!/usr/bin/env python
# Disable OTEL SDK
import os
os.environ["OTEL_SDK_DISABLED"] = "true"
import sys
from src.crew import MarketingEmailGeneratorCrew
from src.data_loader import load_sender_info, load_target_info

def run():
    """
    Run the crew for multiple companies from CSV files.
    
    Usage:
    python main.py targets.csv sender.csv
    """
    try:
        # Get file paths from command line arguments or use defaults
        targets_csv = sys.argv[1] if len(sys.argv) > 1 else "targets.csv"
        sender_csv = sys.argv[2] if len(sys.argv) > 2 else "sender.csv"
        
        # Load data using the data_loader functions
        sender_info = load_sender_info(sender_csv)
        
        # Load and process target companies
        targets = load_target_info(targets_csv)

        
        # Process each target company
        for idx, target_data in enumerate(targets, start=1):
            try:
                print(f"\nProcessing company {idx}: {target_data.get('company', 'Unknown')}")
                
                # Combine target and sender information
                inputs = {**target_data, **sender_info}
                
                # Initialize crew with specific provider and generate email
                MarketingEmailGeneratorCrew().crew().kickoff(inputs=inputs)
                
            except Exception as company_error:
                print(f"Error processing company {idx}: {str(company_error)}")
                continue
                    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        MarketingEmailGeneratorCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MarketingEmailGeneratorCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"company_name": "AI LLMs"}
    try:
        MarketingEmailGeneratorCrew().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
