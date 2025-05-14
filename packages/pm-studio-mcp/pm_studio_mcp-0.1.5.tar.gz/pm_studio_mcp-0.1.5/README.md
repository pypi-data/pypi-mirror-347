# PM Studio MCP

PM Studio MCP is a Model Context Protocol (MCP) server for product management tasks. It provides a suite of tools and utilities to help product managers analyze user feedback, perform competitive analysis, generate data visualizations, and access structured data sources.

## Getting Started

   ```
   {
      "mcpServers": {
         "pm-studio-mcp": {
               "command": "uvx",
               "args": [
                  "pm-studio-mcp"
               ],
               "env": {
                  "WORKING_PATH": "{PATH_TO_YOUR_WORKSPACE}/working_dir/"
               },
               "disabled": false
         }
      }
   }
   ```
