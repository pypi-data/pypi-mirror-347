"""
Titan Table Metadata Query Utility Class
"""

import os
import json
from datetime import datetime
from pm_studio_mcp.utils.titan_table_metadata import get_table_metadata, get_table_metadata_extended, find_table_by_template_name
from pm_studio_mcp.utils.titan_tables.table_metadata import TABLE_METADATA

class TitanMetadataUtils:
    @staticmethod
    def get_table_metadata_tool(table_name: str, working_path: str = None):
        """
        Get metadata information for a specified table name. This tool only performs exact and fuzzy matching on table names,
        and does not search for SQL templates (use find_templates_tool for that purpose).

        Args:
            table_name (str): Table name or keyword (e.g., "EdgeMacECSRetentionV1", "mac ecs", "kpi daily")
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
                - sql_templates: SQL templates (if table supports templates)
                - filter_columns: Filter configurations (if table supports templates)
                - sample_query: Example query (only for legacy tables)
        """
        try:
            # Store original input for reference
            original_input = table_name.strip()
            
            # Search for table by name
            metadata = get_table_metadata(original_input)
            
            if metadata:
                # Find the actual table name that was matched
                actual_table_name = None
                for key in TABLE_METADATA.keys():
                    if TABLE_METADATA[key] == metadata:
                        actual_table_name = key
                        break

                if not actual_table_name:
                    return {
                        "status": "error",
                        "message": f"Internal error: Could not find matched table name for '{original_input}'"
                    }

                # Get extended metadata with SQL templates and filters
                extended_metadata = get_table_metadata_extended(actual_table_name)

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

                # Create appropriate message
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
                    # First try direct substring matching
                    if original_input.lower() in key.lower():
                        suggestions.append(key)
                    else:
                        # Then try word-level matching
                        if any(word.lower() in key.lower() for word in original_input.split()):
                            suggestions.append(key)

                # Only keep top 5 most relevant suggestions                    
                suggestions = suggestions[:5]

                message = f"No table found matching '{original_input}'"
                if suggestions:
                    message += f". Did you mean: {', '.join(suggestions)}?"
                else:
                    message += ". Try using more specific table name keywords."
                    message += "\nFor SQL template search, use the template search tool."
                
                return {
                    "status": "error",
                    "message": message,
                    "suggestions": suggestions
                }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error retrieving table metadata: {str(e)}"
            }

    @staticmethod
    def find_templates_tool(template_keyword: str, working_path: str = None):
        """
        Search for SQL templates based on template name or description keyword.
        This specialized tool only looks for SQL templates, making it more precise than the general metadata tool.

        Args:
            template_keyword (str): SQL template keyword to search for (e.g., "mac dau", "retention by browser")
            working_path (str, optional): Directory path to save the JSON file. If None, will use current directory.

        Returns:
            dict: Dictionary containing search results
                - status: Search status ("success" or "error")
                - message: Status message with summary of found templates
                - template_matches: List of matching templates with their table info:
                    - table: Table name containing the template
                    - template: Template name
                    - description: Template description
                - result_path: Path to the saved JSON file (if templates found)
                If no matches found, returns error status with suggestions
        """
        try:
            # Search for templates matching the keyword
            template_matches = find_table_by_template_name(template_keyword)
            
            if not template_matches:
                # No matches found - collect suggestions
                all_templates = []
                for table_name, metadata in TABLE_METADATA.items():
                    if 'sql_templates' in metadata:
                        for template in metadata['sql_templates']:
                            if 'name' in template and 'description' in template:
                                all_templates.append((table_name, template['name'], template['description']))
                
                # Get up to 5 random templates as suggestions
                import random
                suggestions = random.sample(all_templates, min(5, len(all_templates)))
                
                return {
                    "status": "error",
                    "message": f"No SQL templates found matching '{template_keyword}'",
                    "suggestions": [
                        {"table": t[0], "template": t[1], "description": t[2]} 
                        for t in suggestions
                    ]
                }
            
            # Format template matches
            matches = []
            for table_name, template_name, template_desc in template_matches:
                # Get table metadata for additional details
                table_metadata = get_table_metadata(table_name)
                extended_metadata = get_table_metadata_extended(table_name)
                
                match_info = {
                    "table": table_name,
                    "template": template_name,
                    "description": template_desc,
                    "table_description": table_metadata.get("description", "") if table_metadata else "",
                }
                
                # Add filter information if available
                if extended_metadata and "filter_columns" in extended_metadata:
                    match_info["filter_columns"] = extended_metadata["filter_columns"]
                
                matches.append(match_info)
            
            # Create a summary message
            if len(matches) == 1:
                message = f"Found template '{matches[0]['template']}' in table '{matches[0]['table']}'"
            else:
                message = f"Found {len(matches)} matching templates across {len(set(m['table'] for m in matches))} tables"
            
            # Save detailed results to file
            output_path = None
            if working_path:
                os.makedirs(working_path, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"template_search_{timestamp}.json"
                output_path = os.path.join(working_path, output_filename)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "query": template_keyword,
                        "matches": matches
                    }, f, ensure_ascii=False, indent=2)
            
            return {
                "status": "success",
                "message": message, 
                "template_matches": matches,
                "result_path": output_path
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error searching for SQL templates: {str(e)}"
            }
