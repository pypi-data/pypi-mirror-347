import os
import yaml

# Configuration file for KAAS (Kubernetes AI-powered Cluster Analysis and Solution)
# Users can edit this file to specify their backend LLM and other settings.
# Alternatively, users can define settings in a config.yaml file in the parent directory.

# Default configuration values
DEFAULT_CONFIG = {
    'backend_llm': 'ollama',  # Options: 'ollama', 'bedrock', 'openai', etc.
    'aws_region': 'us-east-1',  # AWS region for SNS and CloudWatch
    'sns_topic_arn': 'arn:aws:sns:us-east-1:Your_Account_ID:K8sGPTAlerts',  # SNS Topic ARN for notifications
    'log_group': '/k8sgpt/notifications',  # CloudWatch Log Group name
    'log_stream': 'kaas',  # CloudWatch Log Stream name
    'pricing_url': 'https://yourwebsite.com/pricing'
}

# Load configuration from config.yaml if it exists
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
config = DEFAULT_CONFIG.copy()

if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, 'r') as f:
            yaml_config = yaml.safe_load(f)
            if yaml_config:
                config.update(yaml_config)
    except Exception as e:
        print(f"Error loading config.yaml: {str(e)}. Falling back to default configuration.")

# Export configuration variables
BACKEND_LLM = config['backend_llm']
AWS_REGION = config['aws_region']
SNS_TOPIC_ARN = config['sns_topic_arn']
LOG_GROUP = config['log_group']
LOG_STREAM = config['log_stream']
PRICING_URL = config['pricing_url']
