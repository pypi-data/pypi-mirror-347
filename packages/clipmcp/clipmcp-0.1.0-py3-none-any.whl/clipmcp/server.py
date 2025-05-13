#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
VideoMCP 服务器模块 (Refactored with FastMCP)
提供MCP接口以便Cursor等工具调用图像生成功能
"""

import os
import sys
import json
import asyncio
import traceback
import logging
import datetime
from typing import Optional, Dict, Any, Tuple

# --- FastMCP Import ---
from fastmcp import FastMCP
# --- End FastMCP Import ---

# 导入路径修正
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
     sys.path.insert(0, project_root)


# 导入服务模块 - Ensure correct relative import
try:
    from videomcp.services.image_service import FastMCP as ImageServiceClient # Rename to avoid conflict
except ImportError as e:
     logging.error(f"Failed to import ImageServiceClient: {e}")
     # Attempt import from current directory if running as script
     try:
         from services.image_service import FastMCP as ImageServiceClient
     except ImportError:
         logging.error("Failed to import ImageServiceClient from services directory as well.")
         sys.exit("Could not import necessary service modules.")

# --- Logging Setup (Simplified for FastMCP) ---
logging.basicConfig(
    level=logging.INFO, # Default to INFO, can be overridden by env var later
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)] # Log to stderr for MCP compatibility
)
logger = logging.getLogger("videomcp_server")

# --- Configuration Loading ---
ACCESS_KEY = os.environ.get("VIDEOMCP_ACCESS_KEY", "")
SECRET_KEY = os.environ.get("VIDEOMCP_SECRET_KEY", "")
API_BASE_URL = os.environ.get("VIDEOMCP_API_BASE_URL", "https://openapi.liblibai.cloud")
DOWNLOAD_DIR = os.environ.get("VIDEOMCP_DOWNLOAD_DIR", os.path.join(os.path.expanduser("~"), "Downloads", "VideoMCP"))
LOG_LEVEL = os.environ.get("VIDEOMCP_LOG_LEVEL", "INFO").upper()

# Apply log level from environment
log_level_numeric = getattr(logging, LOG_LEVEL, logging.INFO)
logger.setLevel(log_level_numeric)
# Also set root logger level if needed, or configure specific loggers
logging.getLogger().setLevel(log_level_numeric)


def _load_config_from_file_if_needed():
    """Loads config from file if environment variables are missing."""
    global ACCESS_KEY, SECRET_KEY, API_BASE_URL, DOWNLOAD_DIR

    if ACCESS_KEY and SECRET_KEY:
        logger.info("Using API keys from environment variables.")
        return

    logger.info("API keys not found in environment, attempting to load from config file...")
    config_path = os.path.join(os.path.expanduser("~"), ".videomcp", "config.json")
    example_config_path = os.path.abspath(os.path.join(script_dir, "..", "mcp.example.json"))

    loaded_from = None
    config_to_use = None

    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                ACCESS_KEY = config.get("access_key", ACCESS_KEY)
                SECRET_KEY = config.get("secret_key", SECRET_KEY)
                API_BASE_URL = config.get("api_base_url", API_BASE_URL)
                DOWNLOAD_DIR = config.get("download_dir", DOWNLOAD_DIR)
                logger.info(f"Loaded configuration from: {config_path}")
                loaded_from = config_path
                config_to_use = config
        except Exception as e:
            logger.warning(f"Failed to load config file {config_path}: {e}", exc_info=True)

    if not (ACCESS_KEY and SECRET_KEY) and os.path.exists(example_config_path):
         logger.info(f"Keys still missing, trying example config: {example_config_path}")
         try:
             with open(example_config_path, "r", encoding="utf-8") as f:
                 config = json.load(f)
                 mcp_config = config.get("mcpServers", {}).get("videomcp", {})
                 env_vars = mcp_config.get("env", {})
                 ACCESS_KEY = env_vars.get("VIDEOMCP_ACCESS_KEY", ACCESS_KEY)
                 SECRET_KEY = env_vars.get("VIDEOMCP_SECRET_KEY", SECRET_KEY)
                 API_BASE_URL = env_vars.get("VIDEOMCP_API_BASE_URL", API_BASE_URL)
                 DOWNLOAD_DIR = env_vars.get("VIDEOMCP_DOWNLOAD_DIR", DOWNLOAD_DIR)
                 logger.info(f"Loaded configuration from example file: {example_config_path}")
                 loaded_from = example_config_path
                 config_to_use = env_vars # Use the env part of the example
         except Exception as e:
             logger.warning(f"Failed to load example config file {example_config_path}: {e}", exc_info=True)

    if not (ACCESS_KEY and SECRET_KEY):
        logger.error("Failed to load API keys from environment or config files. Please set VIDEOMCP_ACCESS_KEY and VIDEOMCP_SECRET_KEY.")
        # Decide if you want to exit or continue with limited functionality
        # sys.exit(1) # Or raise an exception

    # Log final config values (mask sensitive keys)
    logger.info("Final Configuration:")
    logger.info(f"  ACCESS_KEY: {'*' * (len(ACCESS_KEY) - 4)}{ACCESS_KEY[-4:]}" if len(ACCESS_KEY) > 4 else "Not Set")
    # Avoid logging secret key directly
    logger.info(f"  SECRET_KEY: {'Set' if SECRET_KEY else 'Not Set'}")
    logger.info(f"  API_BASE_URL: {API_BASE_URL}")
    logger.info(f"  DOWNLOAD_DIR: {DOWNLOAD_DIR}")
    logger.info(f"  LOG_LEVEL: {LOG_LEVEL}")


# --- Initialize FastMCP ---
mcp = FastMCP("videomcp")
image_service_client: Optional[ImageServiceClient] = None

# --- MCP Tools ---

@mcp.tool()
async def test_connection() -> Dict[str, Any]:
    """
    Tests the connection to the image generation API using the configured credentials.

    Returns:
        A dictionary containing the connection status and details.
        Example success: {"status": "ok", "message": "API connection test successful...", "details": {...}}
        Example failure: {"status": "error", "message": "API connection test failed: ..."}
    """
    global image_service_client
    if not image_service_client:
        return {"status": "error", "message": "Image service client not initialized."}

    logger.info("Testing API connection via MCP tool...")
    try:
        # Use the test_connection method from the image service client
        result = await image_service_client.test_connection()

        if result and result.get("code") == 0:
            user_info = result.get("data", {}).get("userInfo", {})
            balance = user_info.get('balance', 'N/A')
            message = f"API connection test successful. User: {user_info.get('username', 'Unknown')}, Balance: {balance}"
            logger.info(message)
            return {"status": "ok", "message": message, "details": result.get("data", {})}
        else:
            error_msg = result.get("msg", "Unknown error") if result else "No response"
            message = f"API connection test failed: {error_msg}"
            logger.error(message)
            return {"status": "error", "message": message}
    except Exception as e:
        logger.error(f"API connection test exception: {e}", exc_info=True)
        return {"status": "error", "message": f"API connection test exception: {str(e)}"}

@mcp.tool()
async def generate_image(
    prompt: str,
    negative_prompt: Optional[str] = None,
    width: int = 768,
    height: int = 1024,
    img_count: int = 1,
    seed: int = -1,
    download: bool = True,
    use_ultra: bool = False,
    output_dir: Optional[str] = None # Allow overriding download dir per request
) -> Dict[str, Any]:
    """
    Generates images based on text prompts using the configured API.

    Args:
        prompt: The main text prompt describing the desired image.
        negative_prompt: Optional text prompt describing what to avoid in the image.
        width: The width of the generated image(s) in pixels. Default is 768.
        height: The height of the generated image(s) in pixels. Default is 1024.
        img_count: The number of images to generate. Default is 1.
        seed: The random seed for generation. -1 means random. Default is -1.
        download: Whether to automatically download the generated images. Default is True.
        use_ultra: Whether to use the 'ultra' quality/API endpoint if available. Default is False.
        output_dir: Optional specific directory to save downloaded images for this request. Overrides default.

    Returns:
        A dictionary containing the results of the image generation, including image URLs
        and local file paths if downloaded.
        Example: {"success": True, "images": [...], "downloaded_files": [...], "pointsCost": 10, ...}
                 {"success": False, "error": "Failed to generate image: ..."}
    """
    global image_service_client
    if not image_service_client:
         return {"success": False, "error": "Image service client not initialized."}

    logger.info(f"Received generate_image request: prompt='{prompt[:50]}...', count={img_count}, ultra={use_ultra}")

    # Handle custom output directory for this request
    original_download_dir = image_service_client.default_download_dir
    effective_download_dir = output_dir or DOWNLOAD_DIR # Use request-specific or global default
    if download and effective_download_dir:
        try:
            os.makedirs(effective_download_dir, exist_ok=True)
            image_service_client.default_download_dir = effective_download_dir
            logger.info(f"Using download directory for this request: {effective_download_dir}")
        except Exception as e:
            logger.error(f"Failed to create or set download directory {effective_download_dir}: {e}")
            download = False # Disable download if directory fails
            return {"success": False, "error": f"Failed to access output directory: {effective_download_dir}"}
    elif download:
        logger.warning("Download requested but no output directory specified (default or per-request). Disabling download.")
        download = False


    try:
        result = await image_service_client.text2img(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            img_count=img_count,
            seed=seed,
            download=download,
            use_ultra=use_ultra
            # Note: The underlying client might have different param names, adjust if needed
        )

        if result and result.get("code") == 0: # Assuming 'code' == 0 indicates success in the client's response
            logger.info(f"Image generation successful. Cost: {result.get('pointsCost')}, Balance: {result.get('accountBalance')}")
            # Add a success flag for clarity in MCP response
            response_data = result.get("data", {})
            response_data["success"] = True
            # Ensure downloaded_files path uses the correct directory
            if download and "downloaded_files" in response_data and effective_download_dir:
                 response_data["downloaded_files"] = [
                     os.path.join(effective_download_dir, os.path.basename(f))
                     for f in response_data["downloaded_files"]
                 ]

            return response_data
        else:
            error_msg = result.get("msg", "Unknown error") if result else "No response from API"
            logger.error(f"Image generation failed: {error_msg}")
            return {"success": False, "error": f"Image generation failed: {error_msg}"}

    except Exception as e:
        logger.error(f"Exception during image generation: {e}", exc_info=True)
        return {"success": False, "error": f"Internal server error during image generation: {str(e)}"}
    finally:
        # Restore original download directory if it was changed
        if download and effective_download_dir:
            image_service_client.default_download_dir = original_download_dir


# --- Main Execution ---
def main():
    """Initializes the service and runs the FastMCP server."""
    global image_service_client

    logger.info("Starting VideoMCP server...")

    # Load configuration
    _load_config_from_file_if_needed()

    # Check for essential configuration
    if not ACCESS_KEY or not SECRET_KEY:
         logger.critical("API Access Key or Secret Key is missing. Cannot start service.")
         sys.exit(1) # Exit if keys are absolutely required

    # Initialize the image service client
    try:
        logger.info(f"Initializing Image Service Client for API: {API_BASE_URL}")
        image_service_client = ImageServiceClient(
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            api_base_url=API_BASE_URL,
            download_dir=DOWNLOAD_DIR # Set default download dir
        )
        logger.info("Image Service Client initialized successfully.")
        # Optionally run an initial connection test here
        # asyncio.run(test_connection()) # Be careful running async code directly here

    except Exception as e:
        logger.critical(f"Failed to initialize Image Service Client: {e}", exc_info=True)
        sys.exit(1)

    # Run the FastMCP server using stdio transport
    logger.info("Starting FastMCP server with stdio transport...")
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.critical(f"FastMCP server failed: {e}", exc_info=True)
    finally:
        logger.info("VideoMCP server stopped.")

if __name__ == "__main__":
    main()