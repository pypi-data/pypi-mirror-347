from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from datetime import datetime
import requests
import pandas as pd
import os
import importlib.util
import sys
import re

# Import table metadata module
from pm_studio_mcp.utils.titan_table_metadata import get_table_metadata
from pm_studio_mcp.constant import (
    TITAN_ENDPOINT,
    TITAN_SCOPE
)

class TitanQuery:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TitanQuery, cls).__new__(cls)
        return cls._instance

    def __init__(self, user_alias=None):
        if self._initialized:
            return

        # Read USER_ALIAS from environment variables
        if user_alias is not None:
            self.user_alias = user_alias
        elif 'USER_ALIAS' in os.environ:
            self.user_alias = os.environ['USER_ALIAS']
            print(f"Using configured user alias from environment: {self.user_alias}")
        else:
            # Set default value for testing
            self.user_alias = "default_user"
            print(f"Using default user alias for testing: {self.user_alias}")

        # Read credentials directly from environment variables
        if 'TITAN_CLIENT_ID' in os.environ:
            self.titan_client_id = os.environ['TITAN_CLIENT_ID']
        else:
            raise ValueError("TITAN_CLIENT_ID environment variable must be set")

        if 'MICROSOFT_TENANT_ID' in os.environ:
            self.microsoft_tenant_id = os.environ['MICROSOFT_TENANT_ID']
        else:
            raise ValueError("MICROSOFT_TENANT_ID environment variable must be set")

        self.endpoint = TITAN_ENDPOINT
        self.titan_scope = TITAN_SCOPE
        self.credential = InteractiveBrowserCredential(
            client_id=self.titan_client_id, tenant_id=self.microsoft_tenant_id
        )
        self.access_token = (
            "Bearer " + self.credential.get_token(self.titan_scope).token
        )
        self._initialized = True

    def query_data_from_titan_tool(self, query_str, table, output_dir):
        """
        Query data from Titan tool and save directly to file

        Args:
            query_str (str): Query string
            table (str): Table name
            output_dir (str): Output directory path, defaults to current directory

        Returns:
            dict: Dictionary containing:
                - 'file_path': Path to the output file
                - 'row_count': Total number of rows
                - 'message': Status message
        """
        try:
            api_headers = {
                "Authorization": self.access_token,
                "Content-Type": "application/json",
            }
            api_body = {
                "query": query_str,
                "TableName": table,
                "UserAlias": self.user_alias,
                "CreatedTimeUtc": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "UseCache": True,
                "UseDefaultDatabaseName": True,
            }

            response = requests.post(self.endpoint, json=api_body, headers=api_headers)

            # Check response status code
            if response.status_code != 200:
                return {
                    'file_path': None,
                    'row_count': 0,
                    'message': f"API request failed with status code {response.status_code}: {response.text}"
                }

            # Try to parse JSON response
            try:
                response_json = response.json()
            except ValueError as e:
                return {
                    'file_path': None,
                    'row_count': 0,
                    'message': f"Failed to parse API response as JSON: {str(e)}"
                }

            # Check response structure
            if "Result" not in response_json or "data" not in response_json["Result"]:
                return {
                    'file_path': None,
                    'row_count': 0,
                    'message': f"Invalid API response structure: {response_json}"
                }

            # Create output directory if it doesn't exist
            #if output_dir is None:
            #  output_dir = os.getcwd()
            #os.makedirs(output_dir, exist_ok=True)

            # Generate output file path
            output_file = os.path.join(output_dir, f"titan_query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

            # Convert data to DataFrame and get information
            try:
                data = pd.DataFrame(response_json["Result"]["data"])
                # Save to CSV
                data.to_csv(output_file, index=False)

                # Prepare return information
                result = {
                    'file_path': output_file,
                    'row_count': len(data),
                    'message': 'Successfully retrieved data from Titan'
                }

                print(f"Successfully saved query results to: {output_file}")
                print(f"Total rows: {result['row_count']}")
                return result

            except Exception as e:
                return {
                    'file_path': None,
                    'row_count': 0,
                    'message': f"Failed to save data to CSV: {str(e)}"
                }

        except requests.exceptions.RequestException as e:
            return {
                'file_path': None,
                'row_count': 0,
                'message': f"API request failed: {str(e)}"
            }
        except Exception as e:
            return {
                'file_path': None,
                'row_count': 0,
                'message': f"Unexpected error: {str(e)}"
            }

    @staticmethod
    def generate_sql_from_template(table_name, template_name, filter_values, extended_metadata=None):
        """
        Generate SQL query from a template without requiring authentication

        Args:
            table_name (str): Table name (case-insensitive, supports fuzzy matching)
            template_name (str): Name of the SQL template to use (case-insensitive, partial match supported)
            filter_values (dict): Dictionary of filter names and values to replace in the template
                                  Only the filters provided will be replaced in the template
            extended_metadata (dict, optional): Pre-fetched extended metadata with SQL templates.
                                               If not provided, will be fetched using table_name.

        Returns:
            dict: Dictionary containing:
                - 'status': 'success' or 'error'
                - 'sql': Generated SQL query (if successful)
                - 'message': Status or error message
                - 'available_templates': List of available templates (if error due to template not found)
                - 'matched_table': The actual table name that was matched (if different from input)
        """
        try:
            # Try to get the actual table name using fuzzy matching if extended_metadata is not provided
            actual_table_name = None
            if extended_metadata is None:
                # Import here to avoid circular imports
                from pm_studio_mcp.utils.titan_table_metadata import get_table_metadata, get_table_metadata_extended
                from pm_studio_mcp.utils.titan_tables.table_metadata import TABLE_METADATA

                # Try to get the actual table name using enhanced fuzzy matching
                matched_metadata = None

                # Normalize input table_name for better matching
                normalized_input = table_name.lower().replace(' ', '_').strip()

                # Special handling for common tables
                if normalized_input in ['kpi_dailyuser', 'kpidailyuser', 'kpi_daily_user', 'kpi daily user', 'dailyuser', 'daily_user', 'daily user']:
                    print(f"Special case recognized: '{table_name}' -> 'KPI_DailyUser'")
                    for key, value in TABLE_METADATA.items():
                        if key == 'KPI_DailyUser':
                            matched_metadata = value
                            actual_table_name = key
                            break

                # Create variations of the input for more robust matching
                input_variations = [
                    normalized_input,                 # Normalized version (lowercase with underscores)
                    normalized_input.replace('_', ''),  # No underscores
                    table_name.lower().strip(),       # Original lowercase without normalization
                    table_name.lower().replace('_', ' ').strip(),  # Spaces instead of underscores
                    # Add more variants for common patterns
                    'kpi_' + normalized_input if not normalized_input.startswith('kpi_') else normalized_input,
                    normalized_input.replace('kpi_', '')  # Without KPI prefix
                ]

                # First try exact match with any variation
                for key, value in TABLE_METADATA.items():
                    key_lower = key.lower()
                    key_normalized = key_lower.replace(' ', '_')

                    for variation in input_variations:
                        if variation == key_lower or variation == key_normalized:
                            matched_metadata = value
                            actual_table_name = key
                            print(f"Exact table match found: '{actual_table_name}'")
                            break

                    if matched_metadata:
                        break

                # If no exact match, try fuzzy match
                if not matched_metadata:
                    best_match = None
                    best_score = 0
                    close_matches = []

                    for key, value in TABLE_METADATA.items():
                        key_lower = key.lower()
                        key_normalized = key_lower.replace(' ', '_')

                        # Try each variation against the table name
                        for variation in input_variations:
                            # Check for full containment (one is substring of the other)
                            if variation in key_normalized or key_normalized in variation:
                                # Calculate match score based on length ratio and position
                                longer = max(len(variation), len(key_normalized))
                                shorter = min(len(variation), len(key_normalized))

                                # Higher score for substring at beginning and for more exact matches
                                position_factor = 1.0
                                if key_normalized.startswith(variation) or variation.startswith(key_normalized):
                                    position_factor = 1.3  # Increased bonus for prefix match

                                # Score calculation with higher weight for longer matches
                                score = (shorter / longer) * position_factor

                                # Extra bonus for KPI_ prefix if input has it
                                if "kpi" in variation and "kpi" in key_normalized:
                                    score += 0.1

                                # Save all good matches for later analysis
                                if score > 0.25:  # Lower threshold to catch more candidates
                                    close_matches.append((key, value, score))

                                    # Update best match if this is better
                                    if score > best_score:
                                        best_score = score
                                        best_match = (key, value)

                    # Sort close matches by score for better decision making
                    close_matches.sort(key=lambda x: x[2], reverse=True)

                    # If we have multiple close matches, use the one with highest score
                    if close_matches:
                        if len(close_matches) == 1 or close_matches[0][2] > close_matches[1][2] + 0.15:
                            # Clear winner - use it
                            actual_table_name = close_matches[0][0]
                            matched_metadata = close_matches[0][1]
                            print(f"Fuzzy table match found: '{actual_table_name}' (score: {close_matches[0][2]:.2f})")
                        elif len(close_matches) > 1 and close_matches[0][2] > 0.4:
                            # Use the best match if it's reasonably good
                            actual_table_name = close_matches[0][0]
                            matched_metadata = close_matches[0][1]
                            print(f"Using best fuzzy match: '{actual_table_name}' (score: {close_matches[0][2]:.2f})")

                if not matched_metadata:
                    return {
                        'status': 'error',
                        'message': f"No matching table found for '{table_name}'. Please check the table name.",
                        'available_tables': list(TABLE_METADATA.keys())[:10]  # List some available tables as suggestion
                    }

                # Get extended metadata with SQL templates
                extended_metadata = get_table_metadata_extended(actual_table_name)
                print(f"Fetching extended metadata completed: {'successful' if extended_metadata else 'failed'}")

            if not extended_metadata:
                return {
                    'status': 'error',
                    'message': f"Could not find extended metadata for table '{table_name}'."
                }

            # Check if SQL templates exist
            if 'sql_templates' not in extended_metadata or not extended_metadata['sql_templates']:
                # Try to import the module directly to check for SQL_TEMPLATES
                try:
                    import importlib
                    try_names = [
                        actual_table_name or table_name,
                        (actual_table_name or table_name).lower()
                    ]

                    for try_name in try_names:
                        try:
                            module_path = f"utils.titan_tables.{try_name}"
                            print(f"Attempting to import {module_path}...")
                            module = importlib.import_module(module_path)

                            if hasattr(module, 'SQL_TEMPLATES'):
                                print(f"Found SQL_TEMPLATES in module {module_path}")
                                extended_metadata['sql_templates'] = module.SQL_TEMPLATES
                                break
                        except ImportError:
                            continue
                except Exception as e:
                    print(f"Error trying to manually import module: {str(e)}")

                # If still no templates found
                if 'sql_templates' not in extended_metadata or not extended_metadata['sql_templates']:
                    return {
                        'status': 'error',
                        'message': f"No SQL templates found for table '{table_name}'. The table may not support template-based queries."
                    }

            # Try to find a matching template by name with enhanced fuzzy matching
            templates = extended_metadata['sql_templates']
            matched_template_name = None

            # Normalize input template name for better matching
            normalized_template_name = template_name.lower().replace(' ', '_').strip()

            # First try exact match (case insensitive)
            for t in templates:
                if t["name"].lower() == normalized_template_name:
                    matched_template_name = t["name"]
                    print(f"Exact template match found: '{matched_template_name}'")
                    break

            # If no exact match, try partial and fuzzy matches
            if not matched_template_name:
                # Generate variations of the input template name
                template_variations = [
                    normalized_template_name,
                    normalized_template_name.replace('_', ''),
                    normalized_template_name.replace('_', ' ')
                ]

                partial_matches = []
                close_matches = []

                for t in templates:
                    t_name_lower = t["name"].lower()
                    t_name_normalized = t_name_lower.replace(' ', '_')

                    # Check for direct substring matches
                    for variation in template_variations:
                        if variation in t_name_normalized or t_name_normalized in variation:
                            match_score = min(len(variation), len(t_name_normalized)) / max(len(variation), len(t_name_normalized))
                            partial_matches.append((t["name"], match_score))
                            break

                    # Check for word similarity - split by both underscores and spaces for better matching
                    input_words = set(normalized_template_name.replace('_', ' ').split())
                    template_words = set(t_name_lower.replace('_', ' ').split())
                    common_words = input_words.intersection(template_words)

                    if common_words:
                        # Calculate similarity score based on ratio of common words
                        similarity = len(common_words) / max(len(input_words), len(template_words))

                        # Give priority to templates with all key words
                        # Check for common keywords in data domain
                        key_terms = ["dau", "upscaled", "region", "retention", "date", "channel"]
                        input_key_terms = [term for term in key_terms if term in normalized_template_name]
                        template_key_terms = [term for term in key_terms if term in t_name_lower]

                        common_key_terms = set(input_key_terms).intersection(set(template_key_terms))
                        if len(common_key_terms) > 0:
                            # Bonus for matching key terms
                            key_term_match_ratio = len(common_key_terms) / len(input_key_terms) if input_key_terms else 0
                            similarity += key_term_match_ratio * 0.3

                        # Bonus for matching first word and word order
                        if normalized_template_name.split('_')[0] == t_name_lower.split('_')[0]:
                            similarity += 0.2  # Boost score for matching first word

                        if similarity > 0.3:  # Lower threshold to catch more potential matches
                            close_matches.append((t["name"], similarity))

                # Sort matches by relevance - higher scores first
                partial_matches.sort(key=lambda x: x[1], reverse=True)
                close_matches.sort(key=lambda x: x[1], reverse=True)

                # Combine matches, prioritizing close matches over partial matches
                all_matches = [name for name, _ in close_matches] + [name for name, _ in partial_matches]

                # Remove duplicates while preserving order
                unique_matches = []
                for match in all_matches:
                    if match not in unique_matches:
                        unique_matches.append(match)

                if len(unique_matches) == 1:
                    # Single match found
                    matched_template_name = unique_matches[0]
                    print(f"Using closest matching template: '{matched_template_name}'")
                elif len(unique_matches) > 1:
                    # Multiple matches, return error with options
                    return {
                        'status': 'error',
                        'message': f"Multiple templates match '{template_name}'. Please specify one of: {', '.join(unique_matches)}",
                        'available_templates': unique_matches,
                        'matched_table': actual_table_name if actual_table_name != table_name else None
                    }
                else:
                    # No matches found, provide list of available templates
                    available_templates = [t["name"] for t in templates]
                    return {
                        'status': 'error',
                        'message': f"No template matches '{template_name}'. Available templates: {', '.join(available_templates)}",
                        'available_templates': available_templates,
                        'matched_table': actual_table_name if actual_table_name != table_name else None
                    }

            # Use the matched template name if found
            if matched_template_name:
                template_name = matched_template_name

            # Find the template
            template = None
            for t in templates:
                if t["name"].lower() == template_name.lower():
                    template = t
                    break

            # This should not happen if our matching logic above is correct, but just in case
            if not template:
                available_templates = [t["name"] for t in templates]
                return {
                    'status': 'error',
                    'message': f"Template '{template_name}' not found. Available templates: {', '.join(available_templates)}",
                    'available_templates': available_templates
                }

            # Get table filter metadata if available
            filter_metadata = extended_metadata.get('filter_columns', {})

            # Create a consolidated filter values dictionary
            consolidated_filters = {}

            # Check for missing required filters
            if 'required_filters' in template:
                for req_filter in template['required_filters']:
                    if req_filter not in filter_values:
                        return {
                            'status': 'error',
                            'message': f"Missing required filter: {req_filter}",
                            'required_filters': template.get('required_filters', [])
                        }

            # Add explicitly provided filters to the consolidated dictionary
            consolidated_filters.update(filter_values)

            # For all filters in template that weren't provided, use default values if available
            for opt_filter in template.get('optional_filters', []):
                if opt_filter not in consolidated_filters:
                    # Parse filter name to get filter category and specific field
                    # For example, "tenant_type_value" -> "tenant_type", "data_type" -> "data_type"
                    filter_parts = opt_filter.split('_')
                    filter_category = '_'.join(filter_parts[:-1]) if filter_parts[-1] == "value" else opt_filter

                    # Look up default value if available
                    if filter_category in filter_metadata and "default_value" in filter_metadata[filter_category]:
                        consolidated_filters[opt_filter] = filter_metadata[filter_category]["default_value"]
                        print(f"Using default value for {opt_filter}: {consolidated_filters[opt_filter]}")

            # Make a copy of the template SQL
            sql = template['template']

            # Replace placeholders with values from the consolidated filters
            for key, value in consolidated_filters.items():
                sql = sql.replace(f"{{{key}}}", str(value))

            # Check if any placeholders remain unreplaced
            import re
            remaining_placeholders = re.findall(r"\{([^}]+)\}", sql)
            if remaining_placeholders:
                return {
                    'status': 'error',
                    'message': f"Missing values for placeholders: {', '.join(remaining_placeholders)}",
                    'available_placeholders': remaining_placeholders
                }

            # Add additional context to the response
            result = {
                'status': 'success',
                'sql': sql,
                'message': f"Successfully generated SQL from template '{template_name}'",
                'template_used': template_name
            }

            # Include the matched table name if it's different from the input
            if actual_table_name and actual_table_name != table_name:
                result['matched_table'] = actual_table_name

            return result

        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            print(f"Error in generate_sql_from_template: {str(e)}")
            print(f"Traceback: {error_traceback}")
            return {
                'status': 'error',
                'message': f"Error generating SQL from template: {str(e)}"
            }
