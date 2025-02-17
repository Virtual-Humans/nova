# Predictive Coding Implementation

[![CI](https://github.com/leonvanbokhorst/virtual-human/actions/workflows/ci.yml/badge.svg)](https://github.com/leonvanbokhorst/virtual-human/actions/workflows/ci.yml)

## Overview

This project implements predictive coding models in Python, focusing on virtual human experiences. It includes both standalone implementations and a Kafka-integrated version for real-time processing.

## Project Structure

```
.
├── predictive_coding/
│   ├── 01_predcod.py         # Basic predictive coding implementation
│   ├── 02_predcod_nova.py    # Enhanced Nova implementation
│   ├── 03_kafka_nova_poc.py  # Kafka-integrated version
│   └── utils/
├── docs/                 
├── requirements.txt
├── pyproject.toml      
└── setup.py
```

## Technical Stack

- Python-based implementation
- Core dependencies:
  - NumPy: Numerical computing
  - Matplotlib: Data visualization
  - confluent-kafka: Kafka client for real-time processing
  - python-dotenv: Environment variable management

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Environment Configuration:
   - For Kafka integration, set up appropriate environment variables
   - Use `.env` file for local development

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

---
*Part of the Virtual Humans research at Fontys ICT, Research Group IxD.*
