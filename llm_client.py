"""
LLM Client with Azure OpenAI Support
Configured for Cloud9AI Project Resource
"""

import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from openai import APIError, APITimeoutError, APIConnectionError

from prompt_templates import get_audit_analysis_prompt

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for interacting with Azure OpenAI API"""
    
    def __init__(self):
        """Initialize Azure OpenAI client with API credentials"""
        # Azure OpenAI configuration
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")  # Also called subscription_key
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        # Validate required configuration
        if not self.azure_endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT is required in environment variables")
        if not self.api_key:
            raise ValueError("AZURE_OPENAI_API_KEY (subscription_key) is required in environment variables")
        if not self.deployment_name:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME is required in environment variables")
        
        # Initialize Azure OpenAI client
        # Using AsyncAzureOpenAI for FastAPI async compatibility
        self.client = AsyncAzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            api_version=self.api_version
        )
        
        logger.info(f"Azure OpenAI Client Initialized")
        logger.info(f"  Endpoint: {self.azure_endpoint}")
        logger.info(f"  Deployment: {self.deployment_name}")
        logger.info(f"  API Version: {self.api_version}")
        
        self.max_retries = 3
        self.timeout = 120  # 2 minutes timeout
    
    async def generate_audit_analysis(self, company_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate AI audit analysis using Azure OpenAI.
        
        Args:
            company_data: Dictionary containing company and department information
            
        Returns:
            Dictionary containing LLM analysis or None if failed
        """
        try:
            # Generate prompt
            prompt = get_audit_analysis_prompt(company_data)
            
            logger.info(f"Sending request to Azure OpenAI...")
            
            # Call Azure OpenAI API with retries
            for attempt in range(self.max_retries):
                try:
                    response_text = await self._call_azure_openai_api(prompt, attempt + 1)
                    
                    if response_text:
                        # Parse and validate JSON response
                        parsed_response = self._parse_llm_response(response_text)
                        
                        if parsed_response:
                            logger.info("Successfully generated audit analysis")
                            return parsed_response
                        else:
                            logger.warning(f"Attempt {attempt + 1}: Failed to parse LLM response")
                    
                except Exception as e:
                    logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                    
                    if attempt < self.max_retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        logger.info(f"Retrying in {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
            
            # If all retries failed, return fallback response
            logger.error("All Azure OpenAI API attempts failed, generating fallback response")
            return self._generate_fallback_response(company_data)
            
        except Exception as e:
            logger.error(f"Error in generate_audit_analysis: {str(e)}", exc_info=True)
            return self._generate_fallback_response(company_data)
    
    async def _call_azure_openai_api(self, prompt: str, attempt: int) -> Optional[str]:
        """
        Make API call to Azure OpenAI.
        
        Args:
            prompt: The prompt to send to the LLM
            attempt: Current attempt number
            
        Returns:
            Response text from LLM or None
        """
        try:
            logger.info(f"Azure OpenAI API call attempt {attempt}")
            
            # Call Azure OpenAI Chat Completions API
            response = await self.client.chat.completions.create(
                model=self.deployment_name,  # This is your deployment name
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert AI Business Auditor specializing in digital transformation and AI maturity assessment. You provide detailed, objective analysis in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=2048,
                top_p=0.9,
                frequency_penalty=0,
                presence_penalty=0,
                timeout=self.timeout
            )
            
            # Extract the response text
            if response.choices and len(response.choices) > 0:
                response_text = response.choices[0].message.content
                logger.info(f"Received response from Azure OpenAI (length: {len(response_text)} chars)")
                
                # Log token usage if available
                if response.usage:
                    logger.info(f"Token usage - Prompt: {response.usage.prompt_tokens}, "
                              f"Completion: {response.usage.completion_tokens}, "
                              f"Total: {response.usage.total_tokens}")
                
                return response_text
            else:
                logger.error("No choices in Azure OpenAI response")
                return None
                
        except APITimeoutError:
            logger.error(f"Azure OpenAI request timeout on attempt {attempt}")
            return None
        except APIConnectionError as e:
            logger.error(f"Cannot connect to Azure OpenAI: {str(e)}")
            return None
        except APIError as e:
            logger.error(f"Azure OpenAI API error on attempt {attempt}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt}: {str(e)}", exc_info=True)
            return None
    
    def _parse_llm_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """
        Parse and validate LLM response.
        
        Args:
            response_text: Raw text response from LLM
            
        Returns:
            Parsed JSON dict or None if invalid
        """
        try:
            # Clean response text
            response_text = response_text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Find JSON object
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}")
            
            if start_idx == -1 or end_idx == -1:
                logger.error("No JSON object found in response")
                return None
            
            json_text = response_text[start_idx:end_idx + 1]
            
            # Parse JSON
            parsed = json.loads(json_text)
            
            # Validate structure
            if not self._validate_response_structure(parsed):
                logger.error("Response structure validation failed")
                return None
            
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            logger.debug(f"Response text: {response_text[:500]}")
            return None
        except Exception as e:
            logger.error(f"Error parsing response: {str(e)}")
            return None
    
    def _validate_response_structure(self, response: Dict[str, Any]) -> bool:
        """
        Validate that the response has required fields.
        
        Args:
            response: Parsed response dictionary
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check summary section
            if "summary" not in response:
                logger.error("Missing 'summary' field")
                return False
            
            summary = response["summary"]
            required_summary_fields = ["personalized_summary", "overall_risk_score", "ai_maturity_level"]
            for field in required_summary_fields:
                if field not in summary:
                    logger.error(f"Missing '{field}' in summary")
                    return False
            
            # Check sections
            if "sections" not in response or not isinstance(response["sections"], list):
                logger.error("Missing or invalid 'sections' field")
                return False
            
            # Validate each section
            for section in response["sections"]:
                if not all(key in section for key in ["section_name", "level", "drawbacks"]):
                    logger.error("Section missing required fields")
                    return False
                
                if not isinstance(section["drawbacks"], list):
                    logger.error("Drawbacks must be a list")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return False
    
    def _generate_fallback_response(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a fallback response when LLM fails.
        
        Args:
            company_data: Original company data
            
        Returns:
            Fallback audit analysis
        """
        company_name = company_data.get('company_name', 'the organization')
        industry = company_data.get('industry', 'their industry')
        departments = company_data.get('departments', {})
        
        sections = []
        for dept_name in departments.keys():
            sections.append({
                "section_name": dept_name,
                "level": "Medium",
                "drawbacks": [
                    {
                        "title": "Limited Automation",
                        "details": f"The {dept_name} department shows opportunities for increased automation and AI integration."
                    },
                    {
                        "title": "Manual Data Processing",
                        "details": "Current processes rely on manual data handling, limiting scalability and real-time insights."
                    }
                ]
            })
        
        return {
            "summary": {
                "personalized_summary": f"{company_name} operates in the {industry} sector and demonstrates foundational digital capabilities. However, significant opportunities exist for AI integration across departments to enhance operational efficiency and decision-making capabilities.",
                "overall_risk_score": 60,
                "ai_maturity_level": "Medium"
            },
            "sections": sections
        }
