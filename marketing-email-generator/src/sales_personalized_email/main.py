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
        "company": "Home Improvement People Inc.",
        "industry": "Construction",
        "company_category": "Construction & Renovations",
        "company_subcategory": "Bathroom renovation",
        "company_website": "https://www.homeimprovementpeople.com/",
        "company_phone": "(416) 782-7605",
        "company_email": "hello@homeimprovementpeople.com",
        "facebook_url": "",
        "instagram_url": "https://www.instagram.com/homeimprovementpeople/",
        "twitter_url": "",
        "linkedin_url": "",
        "our_company_summary": "Techfi is a cutting-edge IT solutions company that offers a range of services to empower small and medium-sized businesses in North America. Their main services include:\n\n1. Artificial Intelligence Solutions: Techfi provides custom AI solutions tailored to various industries. They offer AI solution development, custom AI applications, and AI integration services to enhance business efficiency and innovation.\n\n2. Business Automation: Techfi offers customized automation solutions integrated with AI tools to boost efficiency and growth. Their automation tools include digital assistants, chatbots, and AI personalization features.\n\n3. Web/Mobile Development: Techfi specializes in developing tailor-made web and mobile applications to drive business success. They focus on creating high-performance websites and mobile apps optimized for performance and reach.\n\n4. Audit & IT Consulting: Techfi aligns technology with business goals through expert IT consulting and audits. They help businesses identify opportunities, optimize IT infrastructure, and develop forward-thinking IT strategies for growth.\n\n5. AR & VR: Techfi offers immersive AR and VR experiences that uniquely connect businesses with their customers. They provide captivating AR and VR designs, interactive development, and seamless deployment and integration of AR/VR technologies.\n\n6. Digital Branding: Techfi elevates digital identity and audience connection through strategic branding services. Their services include crafting unique brand identities, enhancing online visibility, and fostering deep connections with strategic digital content and interactions.\n\nTechfi's services are designed to empower businesses by leveraging cutting-edge technologies and innovative solutions tailored to their specific needs. Their commitment to excellence, customer success, and forward-thinking innovation sets them apart in the IT solutions industry.",
        "sender_company": "Techfi",
        "sender_company_website": "https://techfi.ca",
        "sender_email": "hello@techfi.ca",
        "sender_fullname": "Ozan Muldur",
        "sender_title": "Business Development Engineer",
        "sender_phone": "(705) 791-7718",
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
