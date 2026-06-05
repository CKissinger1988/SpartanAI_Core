import asyncio
import json
import requests
import os
import logging
from typing import Optional

# Attempt to import MCP, fallback to manual JSON-RPC if needed
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent, ImageContent
    from mcp.server.stdio import stdio_server
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

# Apex-Grade Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [MCP-BRIDGE] - %(levelname)s - %(message)s')
logger = logging.getLogger("LMS_MCP_Bridge")

class LMS_MCP_Bridge:
    """
    Sovereign MCP Bridge for LM-Studio integration.
    Allows the Supreme Cortex to utilize GCP-hosted LM-Studio resources via the Model Context Protocol.
    """
    def __init__(self, host="136.107.205.246", port=1234):
        self.base_url = f"http://{host}:{port}/v1"
        self.server_name = "spartan-lms-bridge"
        
        if MCP_AVAILABLE:
            self.server = Server(self.server_name)
            self._register_tools()
        else:
            logger.warning("MCP library not found. Bridge will operate in raw JSON-RPC mode.")

    def _register_tools(self):
        """Registers the tactical tools available to the MCP client."""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="lms_inference",
                    description="Execute high-cognition inference on the GCP LM-Studio node.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "prompt": {"type": "string", "description": "The neural directive for the model."},
                            "model": {"type": "string", "description": "Specific model ID (optional)."},
                            "temperature": {"type": "number", "description": "Cognitive entropy (0.0 to 1.0)."}
                        },
                        "required": ["prompt"]
                    }
                ),
                Tool(
                    name="lms_status",
                    description="Audit the health and loaded models of the LM-Studio node.",
                    inputSchema={"type": "object", "properties": {}}
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            if name == "lms_inference":
                return await self.execute_inference(arguments.get("prompt"), arguments.get("model"), arguments.get("temperature", 0.7))
            elif name == "lms_status":
                return await self.check_node_status()
            else:
                raise ValueError(f"Unknown tactical tool: {name}")

    async def execute_inference(self, prompt: str, model: Optional[str] = None, temp: float = 0.7) -> list:
        """Routes inference request to LM-Studio."""
        payload = {
            "model": model or "loaded-model",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temp
        }
        try:
            logger.info(f"Delegating inference to {self.base_url}...")
            response = requests.post(f"{self.base_url}/chat/completions", json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            result = data['choices'][0]['message']['content']
            if MCP_AVAILABLE:
                return [TextContent(type="text", text=result)]
            return [{"type": "text", "text": result}]
        except Exception as e:
            logger.error(f"Inference failure: {e}")
            msg = f"FATAL: Cognitive link severed. Reason: {str(e)}"
            if MCP_AVAILABLE:
                return [TextContent(type="text", text=msg)]
            return [{"type": "text", "text": msg}]

    async def check_node_status(self) -> list:
        """Audits the remote node."""
        try:
            response = requests.get(f"{self.base_url}/models", timeout=10)
            response.raise_for_status()
            models = response.json()
            status_report = f"NODE STATUS: ONLINE\nMODELS: {json.dumps(models, indent=2)}"
            if MCP_AVAILABLE:
                return [TextContent(type="text", text=status_report)]
            return [{"type": "text", "text": status_report}]
        except Exception as e:
            msg = f"NODE STATUS: UNREACHABLE\nERROR: {str(e)}"
            if MCP_AVAILABLE:
                return [TextContent(type="text", text=msg)]
            return [{"type": "text", "text": msg}]

    async def run(self):
        """Starts the bridge."""
        if not MCP_AVAILABLE:
            print("ERROR: Run 'pip install mcp' to enable standard protocol support.")
            return

        logger.info(f"Initializing {self.server_name} on stdio...")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )

if __name__ == "__main__":
    bridge = LMS_MCP_Bridge()
    if MCP_AVAILABLE:
        asyncio.run(bridge.run())
    else:
        # Simple health check if running standalone without MCP lib
        async def main():
            status = await bridge.check_node_status()
            print(status[0].get("text") if isinstance(status[0], dict) else status[0].text)
        
        asyncio.run(main())
