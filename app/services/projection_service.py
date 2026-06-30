from typing import Any, Dict, List

from app.models.candidate import CandidateProfile


class ProjectionService:
    """
    Converts internal CandidateProfile into requested output shape.

    Supports:
    - field subset selection
    - renaming/remapping using "from"
    - include_confidence toggle
    - include_provenance toggle
    - missing value policy: null / omit / error
    """

    def project(self, candidate: CandidateProfile, config: Dict[str, Any] | None = None) -> Dict[str, Any]:
        candidate_dict = candidate.to_clean_dict()

        if not config:
            return candidate_dict

        output: Dict[str, Any] = {}

        fields = config.get("fields", [])
        include_confidence = config.get("include_confidence", True)
        include_provenance = config.get("include_provenance", True)
        on_missing = config.get("on_missing", "null")

        for field_config in fields:
            output_path = field_config.get("path")
            source_path = field_config.get("from", output_path)
            required = field_config.get("required", False)

            value = self._get_path(candidate_dict, source_path)

            if value is None:
                if required or on_missing == "error":
                    raise ValueError(f"Missing required field: {source_path}")

                if on_missing == "omit":
                    continue

                output[output_path] = None
                continue

            value = self._strip_metadata(
                value,
                include_confidence=include_confidence,
                include_provenance=include_provenance,
            )

            output[output_path] = value

        return output

    def _get_path(self, data: Dict[str, Any], path: str) -> Any:
        """
        Supported path examples:
        full_name
        full_name.value
        emails[0]
        emails[0].value
        phones[0]
        skills[].value
        skills[].name
        """

        if not path:
            return None

        # Assignment config says skills[].name,
        # but our internal Skill model stores the skill string as "value".
        path = path.replace(".name", ".value")

        # Smart default:
        # If user asks full_name, return field value not wrapper.
        smart_value_paths = {
            "full_name": "full_name.value",
            "current_company": "current_company.value",
            "current_title": "current_title.value",
        }

        if path in smart_value_paths:
            path = smart_value_paths[path]

        # If user asks emails[0], return emails[0].value
        if path.startswith("emails[") and path.endswith("]"):
            path = path + ".value"

        # If user asks phones[0], return phones[0].value
        if path.startswith("phones[") and path.endswith("]"):
            path = path + ".value"

        if "[]" in path:
            return self._get_array_projection(data, path)

        current: Any = data

        for part in path.split("."):
            if current is None:
                return None

            if "[" in part and "]" in part:
                field_name = part.split("[")[0]
                index_text = part.split("[")[1].split("]")[0]

                if not isinstance(current, dict):
                    return None

                arr = current.get(field_name)

                if not isinstance(arr, list):
                    return None

                try:
                    index = int(index_text)
                except ValueError:
                    return None

                if index < 0 or index >= len(arr):
                    return None

                current = arr[index]
            else:
                if not isinstance(current, dict):
                    return None

                current = current.get(part)

        return current

    def _get_array_projection(self, data: Dict[str, Any], path: str) -> List[Any]:
        """
        Example:
        skills[].value
        emails[].value
        """

        array_name, child_path = path.split("[]", 1)
        array_name = array_name.strip()
        child_path = child_path.lstrip(".")

        arr = data.get(array_name)

        if not isinstance(arr, list):
            return []

        result = []

        for item in arr:
            if not child_path:
                result.append(item)
                continue

            current = item

            for part in child_path.split("."):
                if not isinstance(current, dict):
                    current = None
                    break

                current = current.get(part)

            if current is not None:
                result.append(current)

        return result

    def _strip_metadata(
        self,
        value: Any,
        include_confidence: bool,
        include_provenance: bool,
    ) -> Any:
        if isinstance(value, list):
            return [
                self._strip_metadata(item, include_confidence, include_provenance)
                for item in value
            ]

        if isinstance(value, dict):
            cleaned = {}

            for key, val in value.items():
                if key == "confidence" and not include_confidence:
                    continue

                if key == "provenance" and not include_provenance:
                    continue

                cleaned[key] = self._strip_metadata(
                    val,
                    include_confidence,
                    include_provenance,
                )

            return cleaned

        return value