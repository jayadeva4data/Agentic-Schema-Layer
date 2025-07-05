from agent_base import Agent
from typing import Dict, Any, List

class MacroGeneratorAgent(Agent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        schema_metadata = input_data.get('schema_metadata', {})
        macros: List[str] = []
        for model, info in schema_metadata.get('models', {}).items():
            # Example: sum and count macros for each model
            macro_sum = f"""{{% macro sum_{model}_amount() %}}
    select sum(amount) from {{ ref('{model}') }}
{{% endmacro %}}"""
            macro_count = f"""{{% macro count_{model}() %}}
    select count(*) from {{ ref('{model}') }}
{{% endmacro %}}"""
            macros.extend([macro_sum, macro_count])
        input_data['macros'] = macros
        return input_data

    def describe(self) -> str:
        return "MacroGeneratorAgent: Generates example macros for each model (sum, count, etc.)." 