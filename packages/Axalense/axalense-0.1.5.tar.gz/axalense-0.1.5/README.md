# Axalense

AI-powered image moderation using Groq.

## Installation

```bash
pip install Axalense

## Usage 
``` bash 
from Axalense import axavision

if __name__ == "__main__":
    result = axavision.analyze_image("sample_image.jpg","prompt","API")
    print(result)