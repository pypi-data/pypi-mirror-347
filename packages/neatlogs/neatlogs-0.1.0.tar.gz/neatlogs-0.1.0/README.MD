# NeatLogs

This repository contains Python scripts that work as the 'NeatLogs' module to extract logs to build a collaborative workspace for agents. 


## Installation

```bash
cd neatlogs
pip install -r requirements.txt
```

## Quick Start

```python
import NeatLogs as nl

# Initialize logging
nl.init()

# That's it! Your LLM conversations will now be logged to demo.txt
```

## Example Output
(If used directly with litellm)
```
📝 Conversation Log
==================================================

🕒 2025-02-11 15:30:45
🤖 Model: gpt-4
--------------------------------------------------
👤 User:
What's the weather like today?

🤖 Assistant:
I don't have access to real-time weather data, but I can help you find weather information for your location.
==================================================
```

## Project Structure
(Not updated completely)
```
neatlogs/
├── __init__.py
├── llm_logger.py     #Core logging functionality
├── log_parser.py     #Log parsing and formatting
├── requirements.txt
└── README.md
```



