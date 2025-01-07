#!/usr/bin/env python
import sys

from sales_personalized_email.crew import SalesPersonalizedEmailCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """
    inputs = {
        "name": "<PROSPECT_NAME>",
        "title": "<PROSPECT_TITLE>", 
        "company": "<PROSPECT_COMPANY>",
        "industry": "<PROSPECT_INDUSTRY>",
        "company_category": "<PROSPECT_COMPANY_CATEGORY>",
        "company_subcategory": "<PROSPECT_COMPANY_SUBCATEGORY>",
        "company_website": "<PROSPECT_COMPANY_WEBSITE>",
        "company_phone": "<PROSPECT_COMPANY_PHONE>",
        "company_email": "<PROSPECT_COMPANY_EMAIL>",
        "facebook_url": "<PROSPECT_FACEBOOK_URL>",
        "instagram_url": "<PROSPECT_INSTAGRAM_URL>",
        "twitter_url": "<PROSPECT_TWITTER_URL>",
        "linkedin_url": "<PROSPECT_LINKEDIN_URL>",
        "our_product": "<OUR_PRODUCT>",
        "sender_company": "<SENDER_COMPANY>",
        "sender_company_website": "<SENDER_COMPANY_WEBSITE>",
        "sender_email": "<SENDER_EMAIL>",
    }
    SalesPersonalizedEmailCrew().crew().kickoff(inputs=inputs)


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
