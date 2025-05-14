from dataclasses import dataclass, asdict, field
from typing import List, Any, Dict, Optional, Union
import json
from llm_config import LLMConfig

@dataclass(frozen=True)
class VerbalAlgorithmConfig:
    """Configuration for the verbal algorithm feature."""
    language_code: str = "en"
    include_pseudocode: bool = True

@dataclass(frozen=True)
class SolveConfig:
    """Configuration specific to the 'solve' functionality."""
    llm_config: LLMConfig = field(default_factory=LLMConfig)
    verbal_algorithm: Optional[VerbalAlgorithmConfig] = field(default_factory=VerbalAlgorithmConfig)
    include_mermaid_diagram: bool = True
    code_implementations: Optional[List[str]] = field(default_factory=lambda: ["Python"])

@dataclass(frozen=True)
class Config:
    """
    Represents the overall application configuration.
    It is strongly-typed and immutable after initialization.
    """
    solve: SolveConfig = field(default_factory=SolveConfig)
    output_directory: str = "cs-assistant-output"

    @classmethod
    def from_json(cls, json_data: Union[str, Dict[str, Any]]) -> 'Config':
        """
        Creates a Config object from JSON data.

        Args:
            json_data: Either a JSON string or a dictionary representing the configuration.
                      Expected structure:
                      {
                          "solve": {
                              "llm_config": {
                                  "model_config_name": str,
                                  "temperature": float
                              },
                              "verbal_algorithm": {
                                  "languages": List[str]
                              } | null,
                              "include_mermaid_diagram": bool,
                              "code_implementations": List[str] | null
                          },
                          "output_directory": str
                      }

        Returns:
            An immutable Config object.

        Raises:
            json.JSONDecodeError: If json_data is a string and is not valid JSON.
            ValueError: If the JSON structure doesn't match the expected configuration format.
        """
        # Convert string to dict if necessary
        if isinstance(json_data, str):
            try:
                config_dict = json.loads(json_data)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(
                    f"Invalid JSON string provided: {str(e)}", e.doc, e.pos
                )
        else:
            config_dict = json_data

        # Validate required top-level keys
        if not isinstance(config_dict, dict):
            raise ValueError("JSON data must be an object")
        
        if "solve" not in config_dict:
            raise ValueError("Missing required 'solve' configuration")
        
        if "output_directory" not in config_dict:
            raise ValueError("Missing required 'output_directory' configuration")

        solve_data = config_dict["solve"]

        # Parse nested model configuration
        model_data = solve_data.get("llm_config")
        if model_data is None or not isinstance(model_data, dict):
            raise ValueError("Missing or invalid 'llm_config' configuration in solve")
        if "model_config_name" not in model_data:
            raise ValueError("Missing 'model_config_name' in solve.llm_config")
        if "temperature" not in model_data:
            raise ValueError("Missing 'temperature' in solve.llm_config")
        llm_config = LLMConfig(
            model_config_name=str(model_data["model_config_name"]),
            temperature=float(model_data["temperature"])
        )

        # Create verbal algorithm config if present
        verbal_algo_config = None
        if (verbal_algo_data := solve_data.get("verbal_algorithm")) is not None:
            if not isinstance(verbal_algo_data, dict):
                raise ValueError("verbal_algorithm must be an object or null")
            if "language_code" not in verbal_algo_data:
                raise ValueError("verbal_algorithm must contain 'language_code' string")
            if not isinstance(verbal_algo_data["language_code"], str):
                raise ValueError("verbal_algorithm.language_code must be a string")
            verbal_algo_config = VerbalAlgorithmConfig(
                language_code=verbal_algo_data["language_code"],
                include_pseudocode=bool(verbal_algo_data.get("include_pseudocode"))
            )

        # Create code implementations list if present
        code_implementations: Optional[List[str]] = None
        if (code_impl_data := solve_data.get("code_implementations")) is not None:
            if not isinstance(code_impl_data, list):
                raise ValueError("code_implementations must be a list or null")
            if not all(isinstance(lang, str) for lang in code_impl_data):
                raise ValueError("All items in code_implementations list must be strings")
            code_implementations = list(code_impl_data)
        elif "code_implementations" in solve_data and solve_data["code_implementations"] is None:  # Explicitly null
            code_implementations = None
        else:  # Not present, use None
            code_implementations = None


        # Create solve config
        solve_config = SolveConfig(
            llm_config=llm_config,
            verbal_algorithm=verbal_algo_config,
            include_mermaid_diagram=bool(solve_data["include_mermaid_diagram"]),
            code_implementations=code_implementations
        )

        # Create and return the complete config
        return cls(
            solve=solve_config,
            output_directory=str(config_dict["output_directory"])
        )

    @classmethod
    def from_args(cls, args: Any) -> 'Config':
        """
        Creates a Config object from an args-like object (e.g., argparse.Namespace).

        Args:
            args: An object with attributes corresponding to the configuration values.
                  Expected attributes:
                  - llm_model: str
                  - temperature: float
                  - verbal_algorithm: bool (toggles the verbal algorithm feature)
                  - verbal_algorithm_languages: List[str]
                  - verbal_algorithm_include_pseudocode: bool
                  - include_mermaid_diagram: bool
                  - code_implementations: bool (toggles the code implementations feature)
                  - code_implementations_languages: List[str]
                  - output_directory: str
        Returns:
            An immutable Config object.
        """
        verbal_algo_config: Optional[VerbalAlgorithmConfig] = None
        if hasattr(args, 'verbal_algorithm') and args.verbal_algorithm:
            verbal_algo_config = VerbalAlgorithmConfig(
                language_code=str(args.verbal_algorithm_language_code) if hasattr(args, 'verbal_algorithm_language_code') else "en",
                include_pseudocode=args.verbal_algorithm_include_pseudocode if hasattr(args, 'verbal_algorithm_include_pseudocode') else True
            )

        code_implementations: Optional[List[str]] = None
        if hasattr(args, 'code_implementations') and not args.code_implementations:  # Explicitly disabled
            code_implementations = None
        elif hasattr(args, 'code_implementations_languages') and args.code_implementations_languages:
            code_implementations = list(args.code_implementations_languages)
        else:  # Default if not specified or enabled
            code_implementations = ["Python"]


        model_config = LLMConfig(
            model_config_name=args.llm_model,
            temperature=float(args.temperature)
        )
        solve_config = SolveConfig(
            llm_config=model_config,
            verbal_algorithm=verbal_algo_config,
            include_mermaid_diagram=args.include_mermaid_diagram,
            code_implementations=code_implementations
        )
        return cls(
            solve=solve_config,
            output_directory=str(args.output_directory)
        )

    def as_dict(self) -> Dict[str, Any]:
        """
        Converts the Config object to a dictionary.

        Returns:
            A dictionary representation of the configuration.
        """
        def dict_factory(data):
            d = {}
            for k, v in data:
                if isinstance(v, list):
                    d[k] = list(v)
                elif v is not None:
                    d[k] = v
            return d
        return asdict(self, dict_factory=dict_factory)

    def to_json(self, indent: Optional[int] = None) -> str:
        """
        Converts the Config object to a JSON string.

        Args:
            indent: Number of spaces to indent JSON output for pretty printing.
                   If None, the output will be compact. Default is None.

        Returns:
            A JSON string representation of the configuration.
        """
        return json.dumps(self.as_dict(), indent=indent)
