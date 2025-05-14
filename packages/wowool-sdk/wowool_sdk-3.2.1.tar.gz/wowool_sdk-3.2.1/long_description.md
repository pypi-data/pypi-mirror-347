# The Wowool NLP Toolkit

## install

Install the main sdk.

    pip install wowool-sdk

Installing languages.

    pip install wowool-lxware-[language]

## Quick Start

Just create a document and pipeline, pass your document trough the Pipeline, and your done.

```python
from wowool.sdk import PipeLine
from wowool.document import Document

document = Document("Mark Van Den Berg works at Omega Pharma.")
# Create an analyzer for a given language and options
process = PipeLine("english,entity")
# Process the data
document = process(document)
print(document)
```

## License

In both cases you will need to acquirer a license file at https://www.wowool.com

### Non-Commercial

    This library is licensed under the GNU AGPLv3 for non-commercial use.  
    For commercial use, a separate license must be purchased.  

### Commercial license Terms

    1. Grants the right to use this library in proprietary software.  
    2. Requires a valid `license.lic` file in the project.  
    3. Redistribution in SaaS requires a commercial license.  
