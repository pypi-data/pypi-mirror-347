# PM Studio MCP

PM Studio MCP is a Model Context Protocol (MCP) server for product management tasks. It provides a suite of tools and utilities to help product managers analyze user feedback, perform competitive analysis, generate data visualizations, and access structured data sources.

## Getting Started

   ```
   {
      "mcpServers": {
         "pm-studio-mcp": {
               "command": "uvx",
               "args": [
                  "pm-studio-mcp"],
               "env": {
                  "WORKING_PATH": "{PATH_TO_YOUR_WORKSPACE}/working_dir/"
               }
         }
      }
   }
   ```

## Tools
- **Feedback Analysis**: Process and analyze user feedback from various sources
- **Profile Analysis**: Generate user profiles and segment users based on their characteristics
- **Data Visualization**: Create charts and visual representations of data
- **Document Conversion**: Convert various document formats to Markdown
- **Data Integration**: Query and analyze data from Titan database and other sources
- **Social Media Analysis**: Scrape and analyze content from Reddit and other platforms
