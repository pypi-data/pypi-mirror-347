# Test Case Generation System

A system that automatically generates formal requirements and test cases from PDF documents using AI agents.

## Features

- PDF document processing
- Automatic formal requirement generation
- Test case generation with multiple test design methods
- User-friendly Gradio interface


## Usage

1. Run the application using uvx and visit website http://127.0.0.1:7860/ to use
```bash
uvx testcase-gen-tool
```

2. Open the provided Gradio interface URL in your browser
3. Upload a PDF document containing requirements
4. Click "Process Document" to generate formal requirements and test cases

## Project Structure

```
.
├── app/
│   └── interface.py            # Application Entry
|   └── testcase_gen_app.py     # Testcase generation Logic
├── pyproject.toml              # Project configuration
├── agents/
│   ├── requirement_agent.py    # Formal requirement generation agent
│   └── testcase_agent.py       # Test case generation agent
└── utils/
    └── pdf_processor.py        # PDF processing utility
```

## Development

The project uses:
- Gradio for the web interface
- SmolAgents for AI agent implementation
- PyPDF2 for PDF processing

## License

MIT License