import openai
import pandas as pd
from pydantic import create_model
from typing import Dict, Optional, List, Union, Callable
import instructor
from anthropic import Anthropic

try:
    from sqlalchemy.orm import DeclarativeMeta
except ImportError:
    DeclarativeMeta = None

def sqlalchemy_model_to_schema(model_class) -> dict:
    """
    Convert a SQLAlchemy declarative model class to a schema dict, marking foreign keys as 'foreign_key'.
    """
    schema = {}
    for col in model_class.__table__.columns:
        if col.foreign_keys:
            schema[col.name] = 'foreign_key'
        elif hasattr(col.type, 'python_type'):
            py_type = col.type.python_type
            if py_type is int:
                dtype = 'number'
            elif py_type is float:
                dtype = 'number'
            elif py_type is str:
                dtype = 'text'
            else:
                dtype = 'text'
            schema[col.name] = dtype
        else:
            schema[col.name] = 'text'
    return schema


class SyntheticDataGenerator:
    def __init__(self, model: str = "gpt-4", temperature: float = 0.7):
        """
        Initialize the synthetic data generator.

        Args:
            model: Model to use ("gpt-4", "gpt-3.5-turbo", "claude-2", etc.).
            temperature: Sampling temperature.
        """
        self.model = model.lower()
        self.temperature = temperature

        # Pick and wrap the correct client once
        if self.model.startswith("claude"):
            raw_client = Anthropic()
        else:
            raw_client = openai.OpenAI()
        self.client = instructor.patch(raw_client)

        # Registry for custom generators by type: type_name -> fn(row: pd.Series, col_name: str) -> value
        self.type_generators: Dict[str, Callable[[pd.Series, str], any]] = {}
        
        # Registry for custom generators by column name: col_name -> fn(row: pd.Series, col_name: str) -> value
        self.column_generators: Dict[str, Callable[[pd.Series, str], any]] = {}

    def register_generator(self, type_name: str, func: Callable[[pd.Series, str], any], column_name: Optional[str] = None):
        """
        Register a custom generator for a specific data type or column name.

        Args:
            type_name: The name of the data type (e.g., 'icd10_code', 'foreign_key').
            func: A function that takes (row: pd.Series, col_name: str) and returns a generated value.
            column_name: Optional specific column name to register this generator for. If provided,
                       this generator will only be used for this specific column. This takes precedence
                       over type-based generators.
        """
        if column_name:
            # Register a column-specific generator
            self.column_generators[column_name] = func
        else:
            # Register a type-based generator
            self.type_generators[type_name.lower()] = func

    def generate_data(
        self,
        schema: Union[Dict[str, str], type],
        prompt: str,
        sample_size: int = 10,
        output_path: Optional[str] = None
    ) -> Union[pd.DataFrame, str]:
        """
        Generate synthetic data via Instructor‑patched LLM, then apply custom generators.

        Args:
            schema: Either a mapping of column names to data types (all treated as strings),
                or a SQLAlchemy declarative model class. If a model class is provided, columns
                with foreign keys will be assigned the 'foreign_key' type.
            prompt: Description of the data to generate.
            sample_size: Number of records to generate.
            output_path: Optional CSV or JSON filepath to save results.

        Usage:
            # Register a generator for foreign keys
            generator.register_generator('foreign_key', lambda row, col: random.choice([1, 2, 3]))
            # Pass a SQLAlchemy model class directly
            generator.generate_data(MyModel, prompt, sample_size=10)

        Returns:
            DataFrame of generated records, or filepath if output_path is set.
        """
        # If schema is a SQLAlchemy model class, convert to dict
        if DeclarativeMeta is not None and isinstance(schema, DeclarativeMeta):
            schema = sqlalchemy_model_to_schema(schema)

        # 1) Identify which cols the LLM should handle vs. custom-only
        custom_cols = set()
        for col, dtype in schema.items():
            # Check if we have a column-specific generator
            if col in self.column_generators:
                custom_cols.add(col)
            # Check if we have a type-based generator
            elif dtype.lower() in self.type_generators:
                custom_cols.add(col)
        
        # Columns to be handled by LLM are those not handled by custom generators
        llm_schema = {
            col: dtype for col, dtype in schema.items()
            if col not in custom_cols
        }

        # 2) Generate LLM-driven columns (if any)
        if llm_schema:
            # Build Pydantic model for parsing
            fields = {col: (str, ...) for col in llm_schema}
            DynamicModel = create_model("DynamicModel", **fields)

            # Build prompt
            lines = [f"Generate {sample_size} records JSON objects with these fields:"]
            for col, dtype in llm_schema.items():
                lines.append(f"- {col}: {dtype}")
            lines.append(f"Description: {prompt}")
            full_prompt = "\n".join(lines)

            # Call the LLM
            ai_objs: List[DynamicModel] = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": full_prompt}],
                response_model=List[DynamicModel],
                temperature=self.temperature,
            )
            df = pd.DataFrame([obj.dict() for obj in ai_objs])
        else:
            # No LLM columns → start with empty rows
            df = pd.DataFrame([{}] * sample_size)

        # 3) Populate custom columns using the full row context
        for col in custom_cols:
            # First check if we have a column-specific generator
            if col in self.column_generators:
                gen_fn = self.column_generators[col]
            # Otherwise use the type-based generator
            else:
                gen_fn = self.type_generators[schema[col].lower()]
            
            # Apply the generator to create values for this column
            df[col] = df.apply(lambda row: gen_fn(row, col), axis=1)

        # 4) Optionally save to CSV or JSON
        if output_path:
            p = output_path.lower()
            if p.endswith(".csv"):
                df.to_csv(output_path, index=False)
            elif p.endswith(".json"):
                df.to_json(output_path, orient="records")
            else:
                raise ValueError("output_path must end with .csv or .json")
            return output_path

        return df
