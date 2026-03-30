# 🤖 AI Engineering Hub

A comprehensive reference and implementation repo covering the full AI engineering stack — from raw HTTP requests to production-grade agentic systems.

Whether you're calling an LLM API for the first time or orchestrating a multi-agent workflow with memory and tool use, this repo has practical examples, patterns, and notes to guide you. Modules are designed to be standalone but progressive — each one builds on concepts introduced in the previous.

---

## What's Inside

**Requests & API Basics** — The foundation. Direct SDK and HTTP calls to LLM providers (OpenAI, Anthropic, Groq) with no frameworks in the way. Covers chat completions, streaming, structured outputs, async requests, and rate limit handling. Understanding raw API calls makes you a better consumer of every framework that abstracts over them.

**RAG (Retrieval-Augmented Generation)** — Ground your model in real data without fine-tuning. Covers document loading, chunking strategies, embedding models, vector stores (FAISS, Chroma, Pinecone), similarity and hybrid search, reranking, and end-to-end pipeline construction. Evaluation with Ragas and LangSmith included.

**LangSmith** — Observability for LLM apps. Covers tracing (automatic and manual via `@traceable`), building datasets from production runs, writing custom evaluators, running prompt experiments, and integrating evals into CI/CD. Essential for debugging chains and agents when things go wrong.

**LangChain** — Composable building blocks. Covers LCEL and the pipe syntax, prompt templates, tool creation, memory, output parsers, and retrieval chains. Focuses on understanding the Runnable interface and how to compose modular, reusable pipelines.

**LangGraph** — Stateful, graph-based workflows for AI. Covers `StateGraph`, typed state, conditional edges, checkpointing, human-in-the-loop breakpoints, subgraphs, and parallel execution. The go-to framework when your workflow needs cycles, branching, or persistent state across steps.

**Agents** — LLMs that reason and act. Covers the ReAct pattern, tool-calling agents, multi-agent architectures (supervisor, hierarchical, swarm), short and long-term memory, and agent evaluation. Includes common failure modes and guardrails for production use.

---

> Built for engineers who want to understand AI systems from the ground up, not just call a wrapper.
