#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Web Crawler Utilities for PM Studio MCP

This module implements web crawling functionality using crawl4ai.
"""

import os
import json
import asyncio
from typing import Dict, Any, List, Optional, Union

# Import only the essential components from crawl4ai
from crawl4ai import AsyncWebCrawler

class CrawlerUtils:
    """Class that implements web crawling functionality."""
    
    @staticmethod
    def crawl_website(
        url: str, 
        max_pages: int = 5, 
        timeout: int = 30, 
        selectors: Optional[List[str]] = None,
        working_dir: str = "",
        deep_crawl: Optional[str] = None,
        question: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crawl a website and extract content.
        
        Args:
            url: URL to crawl
            max_pages: Maximum number of pages to crawl
            timeout: Timeout in seconds for each request
            selectors: CSS selectors to extract specific content (optional)
            working_dir: Directory to save output file
            deep_crawl: Strategy for deep crawling ('bfs' or 'dfs' or None)
            question: Specific question for LLM extraction (optional)
            
        Returns:
            Dictionary with crawl results and status
        """
        try:
            # Run the asynchronous crawl function in a synchronous context
            result = asyncio.run(CrawlerUtils._async_crawl_website(
                url=url,
                max_pages=max_pages,
                timeout=timeout,
                selectors=selectors,
                deep_crawl=deep_crawl,
                question=question
            ))
            
            # Save results to file
            output_filename = f"crawl_{url.replace('https://', '').replace('http://', '').split('/')[0]}.json"
            if working_dir:
                output_file = os.path.join(working_dir, output_filename)
            else:
                output_file = output_filename
                
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
                
            # Create a markdown summary
            markdown_summary = result.get("markdown", CrawlerUtils._generate_markdown_summary(result, url))
            summary_filename = output_file.replace('.json', '.md')
            
            with open(summary_filename, 'w', encoding='utf-8') as f:
                f.write(markdown_summary)
            
            return {
                "status": "success",
                "pages_crawled": len(result.get("pages", [])),
                "output_file": os.path.abspath(output_file),
                "summary_file": os.path.abspath(summary_filename)
            }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error crawling website: {str(e)}"
            }
    
    @staticmethod
    async def _async_crawl_website(
        url: str, 
        max_pages: int = 5,
        timeout: int = 30,
        selectors: Optional[List[str]] = None,
        deep_crawl: Optional[str] = None,
        question: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously crawl a website using crawl4ai.
        
        Args:
            url: URL to crawl
            max_pages: Maximum number of pages to crawl
            timeout: Timeout in seconds for each request
            selectors: CSS selectors to extract specific content
            deep_crawl: Strategy for deep crawling ('bfs' or 'dfs')
            question: Specific question for LLM extraction
            
        Returns:
            Dictionary with crawl results
        """
        # Create crawler options as keyword arguments
        kwargs = {
            "max_pages": max_pages,
            "timeout": timeout
        }
        
        # Add depth parameter if deep crawl is specified
        if deep_crawl:
            kwargs["max_depth"] = 5
        else:
            kwargs["max_depth"] = 2
            
        # Add crawl strategy if specified
        if deep_crawl:
            kwargs["crawl_strategy"] = deep_crawl.lower()
            
        # Add question parameter if specified
        if question:
            kwargs["question"] = question
            
        # Create and run the crawler with simplified API
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=url,
                **kwargs
            )
            
            # Convert result to dictionary, handling different crawl4ai versions
            result_dict = {
                "url": url,
                "markdown": getattr(result, 'markdown', '')
            }
            
            # Handle different result structures
            if hasattr(result, 'pages'):
                # Old version structure
                result_dict["pages"] = []
                for page in result.pages:
                    result_dict["pages"].append({
                        "url": page.url,
                        "title": page.title,
                        "text": page.text,
                        "html": page.html
                    })
            else:
                # New version structure
                result_dict["pages"] = []
                # Check if result itself has content attributes
                if hasattr(result, 'content') or hasattr(result, 'text'):
                    result_dict["pages"].append({
                        "url": url,
                        "title": getattr(result, 'title', 'No Title'),
                        "text": getattr(result, 'content', getattr(result, 'text', '')),
                        "html": getattr(result, 'html', '')
                    })
            
            # Add LLM extraction results if available
            if question and hasattr(result, 'llm_extraction'):
                result_dict["llm_extraction"] = result.llm_extraction
            
            return result_dict
    
    @staticmethod
    def _generate_markdown_summary(data: Dict[str, Any], url: str) -> str:
        """Generate a markdown summary of crawl results."""
        pages = data.get("pages", [])
        
        summary = f"# Web Crawl Results: {url}\n\n"
        summary += f"*Crawled {len(pages)} pages*\n\n"
        
        # Add LLM extraction results if available
        if "llm_extraction" in data:
            summary += "## LLM Extraction Results\n\n"
            summary += f"{data['llm_extraction']}\n\n"
        
        summary += "## Pages Crawled\n\n"
        
        for i, page in enumerate(pages, 1):
            title = page.get("title", "No title")
            page_url = page.get("url", "No URL")
            text_length = len(page.get("text", ""))
            
            summary += f"### {i}. {title}\n"
            summary += f"- URL: {page_url}\n"
            summary += f"- Content Length: {text_length} characters\n"
            summary += "\n"
            
        return summary