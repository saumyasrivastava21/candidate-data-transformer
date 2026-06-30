from typing import Any, Dict, List


class OutputValidationError(Exception):
    pass


class OutputValidator:
    """
    Validates projected output against runtime config.

    Supports:
    - required fields
    - string
    - string[]
    - number
    - object
    - boolean
    """

    def validate(self, output: Dict[str, Any], config: Dict[str, Any] | None = None) -> List[str]:
        errors = []

        if not isinstance(output, dict):
            return ["Output must be a JSON object"]

        if not config:
            return errors

        fields = config.get("fields", [])

        for field_config in fields:
            path = field_config.get("path")
            expected_type = field_config.get("type")
            required = field_config.get("required", False)

            value = output.get(path)

            if required and value is None:
                errors.append(f"Required field missing: {path}")
                continue

            if value is None:
                continue

            if expected_type:
                type_error = self._validate_type(path, value, expected_type)
                if type_error:
                    errors.append(type_error)

        return errors

    def validate_or_raise(self, output: Dict[str, Any], config: Dict[str, Any] | None = None) -> None:
        errors = self.validate(output, config)

        if errors:
            raise OutputValidationError("; ".join(errors))

    def _validate_type(self, path: str, value: Any, expected_type: str) -> str | None:
        if expected_type == "string":
            if not isinstance(value, str):
                return f"{path} must be string"

        elif expected_type == "string[]":
            if not isinstance(value, list):
                return f"{path} must be string[]"

            for item in value:
                if not isinstance(item, str):
                    return f"{path} must contain only strings"

        elif expected_type == "number":
            if not isinstance(value, int | float):
                return f"{path} must be number"

        elif expected_type == "object":
            if not isinstance(value, dict):
                return f"{path} must be object"

        elif expected_type == "boolean":
            if not isinstance(value, bool):
                return f"{path} must be boolean"

        else:
            return f"Unsupported type for {path}: {expected_type}"

        return None