# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cg_jupyter_mux']

package_data = \
{'': ['*']}

install_requires = \
['jupyter_client>=8.0,<9.0']

entry_points = \
{'console_scripts': ['cg_jupyter_mux = cg_jupyter_mux.main:main']}

setup_kwargs = {
    'name': 'cg-jupyter-mux',
    'version': '0.1.1',
    'description': 'A multiplexer for the Jupyter kernel protocol using JSON Lines (JSONL) over stdin/stdout.',
    'long_description': '# cg-jupyter-mux\n\nA command-line tool that acts as a multiplexer for the Jupyter kernel protocol. It communicates with a specified Jupyter kernel, reading JSON Lines messages from standard input and writing JSON Lines messages (from selected channels) to standard output.\n\nThis tool allows programmatic interaction with Jupyter kernels using a simple stdin/stdout interface, suitable for integration into other tools or automated workflows.\n\n## Features\n\n* **Starts Jupyter Kernels:** Launches a kernel specified by name (e.g., `python3`, `bash`).\n* **JSON Lines Interface:** Reads input messages and writes output messages using the [JSON Lines](https://jsonlines.org/) format (one valid JSON object per line).\n* **Async I/O:** Uses `asyncio` for non-blocking communication with the kernel and stdin/stdout.\n* **Input Routing:** Automatically routes incoming messages from stdin to the appropriate kernel channel (`shell` or `stdin`) based on the message\'s `header.msg_type`.\n* **Filtered Output:** Forwards messages received from the kernel\'s `iopub` (broadcast) and `stdin` (input requests/replies) channels to stdout. **Messages from the `shell` channel (direct replies) are intentionally *not* written to stdout.**\n* **Graceful Shutdown:** Handles `Ctrl+C` and EOF on stdin to attempt a clean shutdown of the kernel.\n* **Configurable Verbosity:** Use `-v` for detailed debug logging to stderr.\n\n## Usage\n\n### Command\n\n```bash\ncg-jupyter-mux [-v] <kernel_name>\n```\n\n* **`<kernel_name>` (Required):** The name of the installed Jupyter kernel spec to start (e.g., `python3`). Run `jupyter kernelspec list` to see available kernel names.\n* **`-v`, `--verbose` (Optional):** Enable verbose debug logging, printed to stderr.\n\n### Input Format (stdin)\n\nThe tool expects **JSON Lines** on standard input. Each line must be a single, complete, valid JSON object representing a Jupyter protocol message.\n\n* **Structure:** Standard Jupyter message format (dictionary with `header`, `parent_header`, `metadata`, `content`, `buffers`).\n* **Routing:** The tool inspects the `header.msg_type` field to decide which kernel channel (`shell` or `stdin`) to send the message to. Common types include:\n    * Sent to `shell` channel: `execute_request`, `kernel_info_request`, `inspect_request`, `complete_request`, `shutdown_request`, `comm_open`, `comm_msg`, `comm_close`, etc.\n    * Sent to `stdin` channel: `input_reply`\n\n**Example Input Line (`execute_request`):**\n```json\n{"header": {"msg_id": "exec-abc-123", "username": "cli_user", "session": "session-xyz-789", "date": "2025-04-07T23:40:00Z", "msg_type": "execute_request", "version": "5.3"}, "parent_header": {}, "metadata": {}, "content": {"code": "print(\'Hello Kernel!\')\\nresult=1+2\\nresult", "silent": false, "store_history": true, "user_expressions": {}, "allow_stdin": false}, "buffers": []}\n```\n\n### Output Format (stdout)\n\nThe tool produces **JSON Lines** on standard output. Each line is a single, complete, valid JSON object representing a message received from the kernel.\n\n* **Source Channels:** Only messages from the kernel\'s `iopub` channel (status updates, execution results, output streams, display data, errors) and `stdin` channel (input requests like `input_request`) are output.\n* **Filtered Channels:** Messages received by the client on the `shell` channel (e.g., `execute_reply`, `kernel_info_reply`) are **not** printed to stdout.\n* **Date Format:** `datetime` objects within messages (like `header.date`) are serialized to ISO 8601 strings.\n\n**Example Output Line (`stream` message from `iopub`):**\n```json\n{"header": {"msg_id": "...", "username": "kernel", "session": "session-xyz-789", "date": "2025-04-07T23:40:01.123456Z", "msg_type": "stream", "version": "5.3"}, "parent_header": {"msg_id": "exec-abc-123", ...}, "metadata": {}, "content": {"name": "stdout", "text": "Hello Kernel!\\n"}, "buffers": [], "channel": "iopub"}\n```\n**Example Output Line (`execute_result` message from `iopub`):**\n```json\n{"header": {"msg_id": "...", "username": "kernel", "session": "session-xyz-789", "date": "2025-04-07T23:40:01.234567Z", "msg_type": "execute_result", "version": "5.3"}, "parent_header": {"msg_id": "exec-abc-123", ...}, "metadata": {}, "content": {"data": {"text/plain": "3"}, "execution_count": 1}, "buffers": [], "channel": "iopub"}\n```\n\n### Stopping the Multiplexer\n\n* **EOF:** Close the standard input stream that\'s piping data to `cg-jupyter-mux`. The tool will detect EOF and initiate a graceful shutdown.\n* **Ctrl+C:** Send an interrupt signal (`SIGINT`). The tool traps this and initiates a graceful shutdown.\n\n## Troubleshooting\n\n* **`jupyter_client.kernelspec.NoSuchKernel: No such kernel named <name>`:** Ensure the required kernel package (e.g., `ipykernel` for `python3`) is installed in the same Python environment where `cg-jupyter-mux` is run. Verify using `jupyter kernelspec list`. See Installation section.\n* **JSON Decode Errors:** Input must be strictly one valid JSON object per line. Check for syntax errors or multi-line objects.\n\n## License\n\nThis project is licensed under the MIT License. See the `LICENSE` file (if present) or the `license` field in `pyproject.toml` for details.\n\n```\n',
    'author': 'CodeGrade',
    'author_email': 'info@codegrade.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
