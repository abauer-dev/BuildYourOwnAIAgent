## 🤖 Building an AI Coding Agent from Scratch

This is a learning project and it's remarkable how a small, well-chosen set of tool calls is all it takes to produce a working coding agent.

### 🧠 Core Idea

This AI coding agent is built from scratch on a set of simple but powerful tool calls. No frameworks like LangChain, just the raw **Google Gemini API**.

### 🔧 Fundamental Tools

The agent's capabilities are defined by four core tools:

| Tool | Description |
|------|-------------|
| 🗂️ `get_files_info` | Explore and locate files within the workspace |
| 📖 `get_file_content` | Read and inspect source code from files |
| ▶️ `run_python_file` | Execute functions and run code directly |
| ✏️ `write_file` | Create and modify files |

### ⚙️ How It Works

The agent runs inside an **agent loop** aka a `for` loop with an upper limit of 20 iterations that can exit early once the agent determines it has completed its task. At each step, the agent retains **memory of all past tool calls and their results**, allowing it to reason over its own history and make informed decisions.

### 🧪 Testing

To put the agent through its paces, I intentionally introduced a bug into the provided `calculator` directory and simply asked:

> *"Fix the bug: `3 + 7 * 2` shouldn't be `20`"*

No file paths, no hints, no extra context, and it figured it out. The agent explored the codebase, identified the operator precedence issue, and fixed it on its own.

### ⚠️ A Word of Caution

Be **very careful** about giving an LLM direct access to your filesystem and Python interpreter.

What I've built is essentially a toy version of tools like Cursor's Agentic Mode, or Claude Code. And even those production-grade tools aren't perfectly secure. This is a learning project, not a hardened tool.

> 🚨 **Do not use this agent in any environment you care about.** Treat it as a proof of concept only, and never expose it to sensitive files or systems. And don't encourage anyone to use this toy agent as-is!
