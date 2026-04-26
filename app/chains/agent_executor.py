from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

from app.tools.core_tools import research_tool, prd_tool, planning_tool, critic_tool
from app.tools.search_tool import search_tool
from app.tools.rag_tool import rag_tool
from app.core.llm_router import fast_llm


def create_agent():
    llm = fast_llm()
    tools = [
        search_tool,
        rag_tool,
        research_tool,
        prd_tool,
        planning_tool,
        critic_tool,
    ]

    system_prompt = """You are an expert AI Product Manager with 15+ years of experience.

Your mission: take a raw product idea and transform it into a complete professional product plan using your tools.

## TOOLS AVAILABLE
You have access to these tools:

{tools}

## HOW TO USE TOOLS
Use a json blob to specify a tool by providing an "action" key (tool name) and an "action_input" key (tool input).

Valid "action" values: "Final Answer" or {tool_names}

Provide only ONE action per $JSON_BLOB, as shown:

```
{{
  "action": "$TOOL_NAME",
  "action_input": "$INPUT"
}}
```

Follow this format EXACTLY:

Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}
```

## TOOL USAGE STRATEGY

1. FIRST call search_tool with a specific market query about the product idea
2. THEN call rag_tool if documents are available
3. THEN call research_tool passing the idea + search findings
4. THEN call prd_tool passing the full research output
5. THEN call planning_tool passing the full PRD
6. FINALLY call critic_tool passing ALL previous outputs combined.
   Your input to critic_tool MUST include:
   - The full research_tool output
   - The full prd_tool output  
   - The full planning_tool output
   Do NOT pass just the search results. Combine all three outputs into one string.

## RULES
- NEVER skip search_tool - always start with market research
- Pass FULL outputs between tools - never truncate
- Only use tool names from: {tool_names}
- Base everything on tool outputs, never hallucinate

## FINAL ANSWER FORMAT
Structure your Final Answer as:

# PRODUCT PLAN: [Product Name]

## Market Intelligence
[Key findings from search]

## Research Summary
[Key insights from research_tool]

## Product Requirements Document
[Full PRD]

## Feature Prioritization & Roadmap
[RICE scores and sprint plan]

## Critical Review & Recommendations
[Critique and final recommendation]
"""

    human_prompt = """{input}

{agent_scratchpad}

(reminder to respond in a JSON blob no matter what)"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", human_prompt),
    ])

    agent = create_structured_chat_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=20,
        max_execution_time=600,
        return_intermediate_steps=True,
    )