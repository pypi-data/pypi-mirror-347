# CS Assistant

🎥 WATCH THE USAGE EXAMPLE VIDEO BY CLICKING ON THE IMAGE BELOW 🎥
[![CS Assistant Demo](https://img.youtube.com/vi/ZOk53RLavdc/0.jpg)](https://www.youtube.com/watch?v=ZOk53RLavdc)

CS Assistant is a command-line tool that helps solve computer science problems by leveraging large language models. It can generate algorithmic explanations, pseudocode, code implementations in multiple programming languages, and visual diagrams.

## Features

- Generate verbal explanations of algorithms in multiple languages
- Create pseudocode representations of solutions
- Implement complete code solutions in various programming languages (Python, Java, etc.)
- Generate Mermaid diagrams visualizing the solution
- Support for multiple LLM providers (OpenAI, Google, Anthropic)
- Configurable output directory and formatting options

## Installation

### Prerequisites

- Python 3.8 or higher
- API keys for at least one of the supported LLM providers (OpenAI, Google, Anthropic)

### Option 1: Install from PyPI (Recommended)

Install the package directly from PyPI:

```bash
pip install cs-assistant
```

The first run will automatically create a `.config/cs_assistant/.csarc` template file in your home directory.

### Option 2: Install from Source

1. Clone the repository
2. Run the setup script:

```bash
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Create a template .env file for your API keys

3. Activate the virtual environment:

```bash
source venv/bin/activate
```

4. Edit the `.env` file with your API keys (The first run of the application will also automatically create a `.config/cs_assistant/.csarc` template file)

### Option 3: Manual installation

1. Clone the repository
2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. The first run of the application will automatically create a `.config/cs_assistant/.csarc` file in your home directory. Edit this file with your API keys:

```
OPENAI_API_KEY="your_openai_api_key_here"
GOOGLE_API_KEY="your_google_api_key_here"
ANTHROPIC_API_KEY="your_anthropic_api_key_here"
```

## Usage

### Basic Commands

If installed from PyPI:

```bash
# Create a default configuration file
cs-assistant create-config -o config.json

# Solve a coding problem
cs-assistant solve "Write an algorithm to find the longest common subsequence of two strings"

# Solve a problem with specific configuration file
cs-assistant -c config.json solve "Implement a binary search tree"
```

If installed from source:

```bash
# Create a default configuration file
python -m src.main create-config -o config.json

# Solve a coding problem
python -m src.main solve "Write an algorithm to find the longest common subsequence of two strings"

# Solve a problem with specific configuration file
python -m src.main -c config.json solve "Implement a binary search tree"
```

### Command Line Options

```
usage: CS Assistant [-h] [-c CONFIG] [-o OUTPUT_DIRECTORY] {create-config,solve} ...

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the configuration file (config.json). If provided, command-line arguments will be ignored.
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        Directory where solution files will be saved.

Available commands:
  {create-config,solve}
    create-config       Create a new configuration file with default settings.
    solve               Solve a given coding issue.
```

### Solve Command Options

```
usage: CS Assistant solve [-h] [-m LLM_MODEL] [-t TEMPERATURE] [-v | --verbal-algorithm | --no-verbal-algorithm]
                             [-l VERBAL_ALGORITHM_LANGUAGES [VERBAL_ALGORITHM_LANGUAGES ...]]
                             [-p | --verbal-algorithm-include-pseudocode | --no-verbal-algorithm-include-pseudocode]
                             [-d | --include-mermaid-diagram | --no-include-mermaid-diagram]
                             [-i | --code-implementations | --no-code-implementations]
                             [-L CODE_IMPLEMENTATIONS_LANGUAGES [CODE_IMPLEMENTATIONS_LANGUAGES ...]]
                             issue_description

positional arguments:
  issue_description     The description of the coding issue.

options:
  -h, --help            show this help message and exit
  -m LLM_MODEL, --llm-model LLM_MODEL
                        The identifier for the large language model to be used. Format: 'vendor/model_name' where vendor (e.g., 'google', 'openai') represents
                        the company providing the LLM.
  -t TEMPERATURE, --temperature TEMPERATURE
                        Controls the randomness of the model's output (0.0 to 1.0).

Verbal Algorithm Options:
  -v, --verbal-algorithm, --no-verbal-algorithm
                        Enable/disable verbal algorithm explanations.
  -l VERBAL_ALGORITHM_LANGUAGES [VERBAL_ALGORITHM_LANGUAGES ...], --verbal-algorithm-languages VERBAL_ALGORITHM_LANGUAGES [VERBAL_ALGORITHM_LANGUAGES ...]
                        List of languages for verbal explanations.
  -p, --verbal-algorithm-include-pseudocode, --no-verbal-algorithm-include-pseudocode
                        Include/exclude pseudocode in the output.

  -d, --include-mermaid-diagram, --no-include-mermaid-diagram
                        Include/exclude a Mermaid diagram in the output.

Code Implementation Options:
  -i, --code-implementations, --no-code-implementations
                        Enable/disable code implementation generation.
  -L CODE_IMPLEMENTATIONS_LANGUAGES [CODE_IMPLEMENTATIONS_LANGUAGES ...], --code-implementations-languages CODE_IMPLEMENTATIONS_LANGUAGES [CODE_IMPLEMENTATIONS_LANGUAGES ...]
                        List of programming languages for code implementations.
```

### Example

```bash
# Generate a solution for finding prime numbers in Python and JavaScript
cs-assistant solve -L Python JavaScript "Write an algorithm to find all prime numbers up to n using the Sieve of Eratosthenes"
```

## Configuration

You can customize the behavior of CS Assistant using a configuration file. Create a default configuration with:

```bash
cs-assistant create-config -o config.json
```

This will generate a JSON file with default settings that you can modify:

```json
{
  "solve_issue": {
    "llm_config": {
      "model_config_name": "openai/gpt-4o",
      "temperature": 0.7
    },
    "verbal_algorithm": {
      "languages": [
        "en"
      ],
      "include_pseudocode": true
    },
    "include_mermaid_diagram": true,
    "code_implementations": {
      "implementation_languages": [
        "Python"
      ]
    }
  },
  "output_directory": "cs-assistant-output"
}
```

## Output

The tool creates a directory structure for each problem in the specified output directory:

```
cs-assistant-output/
└── solve/
    └── find_prime_numbers/
        ├── verbal_algorithm.md      # Contains algorithm explanation and pseudocode
        ├── sieve_of_eratosthenes.py # Python implementation
        ├── SieveOfEratosthenes.js   # JavaScript implementation
        └── find_prime_numbers-diagram.md # Contains Mermaid diagram
```

## API Keys

You need to set up API keys for the LLM providers you want to use. These can be provided in one of two ways:

1. In a `.csarc` file located at `~/.config/cs_assistant/.csarc`
2. As environment variables

Example `.csarc` file:
```
OPENAI_API_KEY="sk-..."
GOOGLE_API_KEY="..."
ANTHROPIC_API_KEY="sk-ant-..."
```

The first run of the application will automatically create this file with template values that you can replace with your actual API keys.

## License

See the LICENSE file for details.

## Recent Changes

Here's a summary of the latest updates:

- **`1a22ccd`**: Updated solution output path to include a `solve` directory (e.g., `cs-assistant-output/solve/problem_name/`). Also fixed a missing newline at the end of `src/solve.py`.
- **`3c71c2b`**: Refactored internal code by renaming `src/issue_solver.py` to `src/solve.py`. Unused imports were also removed from `src/solve.py`.
- **`857729f`**: Renamed the primary command from `solve-issue` to `solve`. For example, you now run `cs-assistant solve "your problem"` instead of `cs-assistant solve-issue "your problem"`.
