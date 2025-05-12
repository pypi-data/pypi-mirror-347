KAAS - Kubernetes AI-powered Cluster Analysis and Solution
KAAS is a tool that leverages AI to analyze Kubernetes clusters, identify issues, and provide solutions using tools like k8sgpt and LLMs (e.g., Ollama, Bedrock).
Installation

Install dependencies:
pip install -r requirements.txt


Install KAAS:
python setup.py install



Configuration
Edit config.yaml or kaas/config.py to set your backend LLM and AWS settings:

backend_llm: The LLM backend for k8sgpt (e.g., ollama, bedrock).
aws_region: AWS region for SNS and CloudWatch.
sns_topic_arn: SNS Topic ARN for notifications.
log_group and log_stream: CloudWatch Log Group and Stream names.
pricing_url: URL for multi-cluster pricing information.

Usage
Run KAAS to analyze your Kubernetes cluster:
kaas

Prerequisites

k8sgpt and kubectl must be installed and available in your PATH.
AWS credentials must be configured for SNS and CloudWatch access.

License
This project is licensed under the MIT License - see the LICENSE file for details.

