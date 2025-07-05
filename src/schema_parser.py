import os
import json
import yaml
import re
from typing import Dict, Any

class SchemaParser:
    def __init__(self, dbt_project_path: str):
        self.dbt_project_path = dbt_project_path
        self.metadata = {"models": {}, "macros": {}, "docs": {}}

    def parse_models(self):
        models_path = os.path.join(self.dbt_project_path, "models")
        for root, _, files in os.walk(models_path):
            for file in files:
                if file.endswith(".sql"):
                    model_name = file[:-4]
                    self.metadata["models"][model_name] = {"columns": []}
                    # Simple column extraction: look for 'select ... as col' patterns
                    with open(os.path.join(root, file)) as f:
                        sql = f.read()
                        columns = re.findall(r"as ([a-zA-Z0-9_]+)", sql)
                        self.metadata["models"][model_name]["columns"] = list(set(columns))
                elif file.endswith(".yml") or file.endswith(".yaml"):
                    with open(os.path.join(root, file)) as f:
                        yml = yaml.safe_load(f)
                        if yml and "models" in yml:
                            for model in yml["models"]:
                                name = model.get("name")
                                if name:
                                    if name not in self.metadata["models"]:
                                        self.metadata["models"][name] = {"columns": []}
                                    # Add column info
                                    cols = model.get("columns", [])
                                    self.metadata["models"][name]["columns"] = [c["name"] for c in cols if "name" in c]
                                    # Add relationships if present
                                    if "relationships" in model:
                                        self.metadata["models"][name]["relationships"] = model["relationships"]
                                    # Add description if present
                                    if "description" in model:
                                        self.metadata["models"][name]["description"] = model["description"]

    def parse_macros(self):
        macros_path = os.path.join(self.dbt_project_path, "macros")
        for root, _, files in os.walk(macros_path):
            for file in files:
                if file.endswith(".sql"):
                    with open(os.path.join(root, file)) as f:
                        sql = f.read()
                        macros = re.findall(r"macro ([a-zA-Z0-9_]+)\(", sql)
                        for macro in macros:
                            self.metadata["macros"][macro] = {"definition": ""}  # Optionally store definition

    def parse_docs(self):
        # Parse docs from .yml files and .md files in the dbt project
        docs_path = os.path.join(self.dbt_project_path, "models")
        for root, _, files in os.walk(docs_path):
            for file in files:
                if file.endswith(".yml") or file.endswith(".yaml"):
                    with open(os.path.join(root, file)) as f:
                        yml = yaml.safe_load(f)
                        if yml and "models" in yml:
                            for model in yml["models"]:
                                if "description" in model:
                                    self.metadata["docs"][model["name"]] = model["description"]
                elif file.endswith(".md"):
                    with open(os.path.join(root, file)) as f:
                        content = f.read()
                        self.metadata["docs"][file[:-3]] = content.strip()

    def extract_metadata(self) -> Dict[str, Any]:
        self.parse_models()
        self.parse_macros()
        self.parse_docs()
        return self.metadata

    def export_metadata(self, output_path: str):
        with open(output_path, 'w') as f:
            json.dump(self.metadata, f, indent=2) 