
import json
import re
import os
import inspect
import threading
from typing import Callable, Dict, Any, List
import pyttsx3

from aeon.config import AEON_MODEL
from aeon.core.llm import LLM
from aeon.core.persona import SYSTEM_PROMPT
from aeon.utils.io import output, error, confirm, user_input
import aeon.scripts as scripts

class Engine:
    def __init__(self, output_handler: Callable[[str], None] = output):
        self.llm = LLM()
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.tools: Dict[str, Callable] = {}
        # Force mode: if True, dangerous tools run without confirmation
        self.force_mode = os.getenv("AEON_FORCE_MODE", "true").lower() == "true"
        self.output_handler = output_handler
        
        # Voice Engine
        try:
            self.tts_engine = pyttsx3.init()
            # Optional: Configure voice here if needed
            # voices = self.tts_engine.getProperty('voices')
            # self.tts_engine.setProperty('voice', voices[0].id) 
        except Exception as e:
            self.output_handler(f"Warning: Voice engine failed to initialize: {e}")
            self.tts_engine = None

        self._register_all_scripts()
        self._inject_tool_definitions()

    def _register_all_scripts(self):
        """Registers all functions from aeon.scripts as tools."""
        # inspect.getmembers returns all functions in the module
        for name, func in inspect.getmembers(scripts, inspect.isfunction):
            # We treat all loaded scripts as tools
            self.tools[name] = func
        self.output_handler(f"Registered {len(self.tools)} automation tools from library.")

    def _inject_tool_definitions(self):
        """Adds tool definitions to the system prompt."""
        tools_doc = "\n\nAvailable Tools (Invoke using JSON format: {\"tool\": \"name\", \"args\": {...}} inside a code block):\n"
        # Only list a few key ones to save context, or list names if too many.
        # With 179 tools, listing all descriptions is too big. We list names and a generic instruction.
        tools_doc += "You have access to a vast library of tools. Here are some categories and examples:\n"
        tools_doc += "- File Ops: read_file, write_file, list_files, delete_file, zip_directory, etc.\n"
        tools_doc += "- System Ops: open_application, run_command, shutdown_system, etc.\n"
        tools_doc += "- Web Ops: search_web, get_page_text, download_file, etc.\n"
        tools_doc += "- Net Ops: ping_host, scan_ports, etc.\n"
        tools_doc += "- Text Ops: to_uppercase, generate_password, etc.\n"
        tools_doc += "\nUse your knowledge of standard naming conventions to guess the tool if needed, or ask 'help(function_name)' via your own internal reasoning.\n"
        
        tools_doc += "\nRESPONSE FORMAT:\n"
        tools_doc += "If you want to speak to the user, just write text.\n"
        tools_doc += "If you want to use a tool, write ONLY the JSON object in a markdown code block like:\n"
        tools_doc += "```json\n{\"tool\": \"tool_name\", \"args\": {\"arg1\": \"val\"}}\n```\n"
        
        # Update system prompt
        self.history[0]["content"] += tools_doc

    def speak(self, text: str):
        """Speaks the text using TTS engine in a separate thread."""
        if not self.tts_engine:
            return
            
        def _run():
            try:
                # Remove code blocks and special chars for smoother speech
                clean_text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
                clean_text = clean_text.replace("*", "").replace("`", "").strip()
                if clean_text:
                    self.tts_engine.say(clean_text)
                    self.tts_engine.runAndWait()
            except Exception as e:
                pass # Voice should not crash the system

        threading.Thread(target=_run, daemon=True).start()

    def run_loop(self):
        """Main agent loop."""
        self.output_handler(f"AEON System Online (Model: {self.llm.model})")
        while True:
            try:
                user_msg = user_input()
                if not user_msg:
                    continue
                
                if user_msg.lower() in ["exit", "quit", "shutdown"]:
                    self.output_handler("Shutting down system.")
                    break

                self.chat(user_msg)

            except KeyboardInterrupt:
                self.output_handler("\nInterrupted.")
                break
            except Exception as e:
                error(f"System Error: {e}")

    def chat(self, user_msg: str) -> str:
        """
        Processes a user message and returns the aggregated text response.
        Useful for Web UI integration.
        """
        self.history.append({"role": "user", "content": user_msg})
        return self._process_turn()

    def _process_turn(self) -> str:
        """Processes a single turn of conversation (Thought -> Tool -> Response)."""
        max_turns = 5 
        current_turn = 0
        final_text_response = ""

        while current_turn < max_turns:
            # Thinking...
            response = self.llm.chat(json.dumps(self.history[-1]), str(self.history[0]["content"]))
            
            # Use regex to find JSON code blocks
            tool_calls = re.findall(r"```json\s*(\{.*?\})\s*```", response, re.DOTALL)
            
            text_response = re.sub(r"```json\s*\{.*?\}\s*```", "", response, flags=re.DOTALL).strip()
            
            if text_response:
                self.output_handler(text_response)
                # Speak the response
                self.speak(text_response)
                final_text_response += text_response + "\n"

            if not tool_calls:
                self.history.append({"role": "assistant", "content": response})
                break

            self.history.append({"role": "assistant", "content": response})
            
            for tool_json in tool_calls:
                try:
                    call_data = json.loads(tool_json)
                    tool_name = call_data.get("tool")
                    tool_args = call_data.get("args", {})
                    
                    if tool_name not in self.tools:
                        result = f"Error: Unknown tool '{tool_name}'"
                    else:
                        func = self.tools[tool_name]
                        # In Force Mode, we execute immediately.
                        # Since user asked for "INDEPENDENT WITHOUT PERMISSION", we default to running.
                        self.output_handler(f"[EXEC] {tool_name}({tool_args})")
                        try:
                            # Verify arg count or just try calling
                            result = func(**tool_args)
                        except TypeError as te:
                             result = f"Argument Error: {te}"
                        except Exception as e:
                             result = f"Execution Error: {e}"
                    
                    self.history.append({"role": "user", "content": f"Tool Output ({tool_name}): {result}"})
                    
                except json.JSONDecodeError:
                    self.history.append({"role": "user", "content": "Error: Invalid JSON for tool call."})
            
            current_turn += 1
        
        return final_text_response.strip()


