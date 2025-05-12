"""
Titan Table Metadata Query Utility Class
"""

import os
import json
from datetime import datetime
from pm_studio_mcp.utils.titan_table_metadata import get_table_metadata, get_table_metadata_extended
from pm_studio_mcp.utils.titan_tables.table_metadata import TABLE_METADATA

class TitanMetadataUtils:
    @staticmethod
    def get_table_metadata_tool(table_name: str, working_path: str = None):
        """
        Get metadata information for a specified table and save to JSON file

        Args:
            table_name (str): Table name or keyword
            working_path (str, optional): Directory path to save the JSON file. If None, will use current directory.

        Returns:
            dict: Dictionary containing query results
                - status: Query status ("success" or "error")
                - message: Status message
                - result_path: Path to the saved JSON file (if successful)
                - table_name: Actual table name found (if using fuzzy matching)
                - sql_templates: SQL templates with placeholders (for template-based tables)
                - filter_columns: Filter configurations (for template-based tables)

        The saved JSON file contains:
                - sample: Sample data showing the table structure
                - description: Table description
                - sql_templates: SQL templates (for template-based tables)
                - filter_columns: Filter configurations (for template-based tables)
                - sample_query: Example query (only for legacy tables that don't use templates)
        """
        try:
            # Store original input for reference
            original_input = table_name

            # Get table metadata (standard version)
            metadata = get_table_metadata(table_name)

            # Try to get extended metadata (with SQL templates and filters)
            extended_metadata = get_table_metadata_extended(table_name)

            if metadata:
                # Find the actual table name that was matched
                actual_table_name = None
                for key in TABLE_METADATA.keys():
                    if TABLE_METADATA[key] == metadata:
                        actual_table_name = key
                        break

                # Generate output filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"table_metadata_{actual_table_name}_{timestamp}.json"

                # Determine output path
                if working_path:
                    os.makedirs(working_path, exist_ok=True)
                    output_path = os.path.join(working_path, output_filename)
                else:
                    output_path = output_filename

                # Prepare the result data structure
                result_metadata = {
                    "sample": metadata.get("sample", ""),
                    "description": metadata.get("description", "")
                }

                # Add extended metadata if available
                if extended_metadata:
                    if "sql_templates" in extended_metadata:
                        result_metadata["sql_templates"] = extended_metadata["sql_templates"]
                    if "filter_columns" in extended_metadata:
                        result_metadata["filter_columns"] = extended_metadata["filter_columns"]

                # Save metadata to JSON file
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result_metadata, f, ensure_ascii=False, indent=2)

                # Create a message based on whether fuzzy matching was used
                message = (f"Successfully retrieved metadata for table '{actual_table_name}'"
                          if original_input.lower() == actual_table_name.lower() else
                          f"Found table '{actual_table_name}' matching your query '{original_input}'")

                # Prepare return object
                return_obj = {
                    "status": "success",
                    "message": message,
                    "result_path": output_path,
                    "table_name": actual_table_name
                }

                # Add extended metadata to return object if available
                if extended_metadata:
                    if "sql_templates" in extended_metadata:
                        return_obj["sql_templates"] = extended_metadata["sql_templates"]
                    if "filter_columns" in extended_metadata:
                        return_obj["filter_columns"] = extended_metadata["filter_columns"]

                return return_obj
            else:
                # Return suggestions for similar tables
                suggestions = []
                for key in TABLE_METADATA.keys():
                    if any(word.lower() in key.lower() for word in original_input.split()):
                        suggestions.append(key)

                message = f"No metadata found for table '{original_input}'"
                if suggestions:
                    message += f". Did you mean: {', '.join(suggestions)}?"

                return {
                    "status": "error",
                    "message": message
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error retrieving table metadata: {str(e)}"
            }
