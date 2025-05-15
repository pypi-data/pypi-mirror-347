
import requests
import json
import time
import base64
import os
from typing import Dict, Union, Optional, Type
from pydantic import BaseModel


class VisionClient:
    def __init__(self, token: str, base_url: str = "http://localhost:8000"):
        self.token = token
        self.base_url = base_url.rstrip("/")

    def extract(
        self,
        file: Union[str, bytes],
        schema: Union[Dict, Type[BaseModel]],
        filename: str = "document.pdf",
        mime_type: str = "application/pdf"
    ) -> Dict:
        """
        Submits a PDF and schema to the extractor API.
        file: str (file path or base64) or bytes
        schema: dict or Pydantic model
        """
        # Process schema
        if isinstance(schema, type) and issubclass(schema, BaseModel):
            schema_payload = {
                "schema": self._pydantic_to_extraction_schema(schema)}
        elif isinstance(schema, dict):
            schema_payload = {"schema": schema}
        else:
            raise ValueError(
                "Schema must be a dict or a Pydantic BaseModel class.")

        # Read file content
        if isinstance(file, str):
            if os.path.exists(file):
                with open(file, "rb") as f:
                    file_bytes = f.read()
            else:
                try:
                    file_bytes = base64.b64decode(file)
                except Exception:
                    raise ValueError("Invalid file path or base64 string.")
        elif isinstance(file, bytes):
            file_bytes = file
        else:
            raise ValueError(
                "File must be a valid path, bytes, or base64 string.")

        files = {
            "pdf_file": (filename, file_bytes, mime_type),
            "schema": ("schema.json", json.dumps(schema_payload), "application/json")
        }

        response = requests.post(
            f"{self.base_url}/v1/vision/extract",
            files=files,
            headers={"Authorization": f"Bearer {self.token}"}
        )
        response.raise_for_status()
        return response.json()

    def _pydantic_to_extraction_schema(self, model: Type[BaseModel]) -> dict:
        schema = {}
        for field_name, field in model.model_fields.items():
            field_type = field.annotation
            schema[field_name] = {
                "type": self._python_type_to_str(field_type),
                "description": field.description or ""
            }
        return schema

    def _python_type_to_str(self, t):
        if t == str:
            return "string"
        elif t == int:
            return "INTEGER"
        elif t == float:
            return "NUMBER"
        elif t == bool:
            return "BOOLEAN"
        else:
            return "string"
