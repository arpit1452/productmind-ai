from langchain.tools import tool
from app.core.llm_router import fast_llm


@tool
def research_tool(idea: str) -> str:
    """
    Performs deep market research on a product idea.
    Input should be the product idea along with any search/RAG context already gathered.
    Returns competitor analysis, user pain points, market gaps, and differentiation opportunities.
    """
    llm = fast_llm()
    prompt = f"""
You are a senior product researcher. Conduct deep market research for the following product idea:

PRODUCT IDEA: {idea}

Your research must cover ALL of the following sections in detail:

## 1. PROBLEM ANALYSIS
- What core problem does this solve?
- How severe is the pain point (1-10)? Justify.
- Who suffers most from this problem?

## 2. TARGET AUDIENCE
- Primary user persona (name, age, job, goals, frustrations)
- Secondary user persona
- User behavior patterns relevant to this product

## 3. COMPETITOR LANDSCAPE
- List 4-5 direct competitors with their strengths and weaknesses
- List 2-3 indirect competitors
- What do ALL competitors get wrong? (This is your opportunity)

## 4. MARKET OPPORTUNITY
- Estimated market size (TAM/SAM/SOM if possible)
- Market growth trend (growing/shrinking/stable)
- Key market drivers

## 5. DIFFERENTIATION STRATEGY
- What unique angle can this product take?
- What would make users switch from existing solutions?
- One-line unique value proposition

## 6. KEY RISKS
- Top 3 risks (technical, market, user adoption)
- Mitigation strategy for each

Be specific, realistic, and data-driven. Do not be vague.
"""
    return llm.invoke(prompt).content


@tool
def prd_tool(research: str) -> str:
    """
    Generates a comprehensive Product Requirements Document (PRD) from research findings.
    Input must be the full research output from research_tool.
    Returns a structured PRD with problem statement, user stories, features, success metrics, and technical requirements.
    """
    llm = fast_llm()
    prompt = f"""
You are a senior Product Manager at a top tech company. Based on the research below, write a complete, professional Product Requirements Document (PRD).

RESEARCH INPUT:
{research}

Generate a full PRD with the following structure:

---
# PRODUCT REQUIREMENTS DOCUMENT

## 1. EXECUTIVE SUMMARY
- Product Name (suggest a catchy name)
- One-line description
- Problem being solved
- Proposed solution

## 2. GOALS & SUCCESS METRICS
- Primary goal
- 3-5 measurable KPIs (with specific targets, e.g., "DAU of 10k in 3 months")
- What does success look like in 6 months?

## 3. USER PERSONAS
- Persona 1: Name, background, goals, frustrations, how this product helps
- Persona 2: (secondary user)

## 4. USER STORIES
Write 8-10 detailed user stories in format:
"As a [persona], I want to [action] so that [benefit]."
Include acceptance criteria for each.

## 5. CORE FEATURES (MVP)
For each feature:
- Feature name
- Description
- User value
- Priority (Must Have / Should Have / Nice to Have)
- Estimated complexity (Low/Medium/High)

List at least 6 features.

## 6. OUT OF SCOPE (v1)
- Features explicitly NOT in MVP and why

## 7. TECHNICAL REQUIREMENTS
- Platform (web/mobile/both)
- Key integrations needed
- Performance requirements
- Security/privacy considerations

## 8. ASSUMPTIONS & DEPENDENCIES
- List 4-5 key assumptions
- External dependencies

## 9. OPEN QUESTIONS
- 3-5 questions that need answers before development starts

---
Be thorough, professional, and specific. Avoid generic statements.
"""
    return llm.invoke(prompt).content


@tool
def planning_tool(prd: str) -> str:
    """
    Performs RICE scoring and sprint planning based on the PRD.
    Input must be the full PRD from prd_tool.
    Returns a prioritized feature backlog with RICE scores, sprint plan, and roadmap.
    """
    llm = fast_llm()
    prompt = f"""
You are a senior Product Manager and Agile coach. Based on the PRD below, create a complete feature prioritization and execution plan.

PRD INPUT:
{prd}

Generate the following:

---
# FEATURE PRIORITIZATION & PLANNING

## 1. RICE SCORING TABLE
For each feature from the PRD, calculate RICE score:
- Reach: How many users impacted per quarter? (number)
- Impact: How much does it move the needle? (0.25=minimal, 0.5=low, 1=medium, 2=high, 3=massive)
- Confidence: How confident are we? (percentage: 50%, 80%, 100%)
- Effort: Person-weeks to build? (number)
- RICE Score = (Reach × Impact × Confidence) / Effort

Present as a table:
| Feature | Reach | Impact | Confidence | Effort | RICE Score | Priority |
|---------|-------|--------|------------|--------|------------|----------|

Sort by RICE Score descending.

## 2. MVP SPRINT PLAN (8 weeks)
Break into 4 two-week sprints:

**Sprint 1 (Weeks 1-2): Foundation**
- List specific tasks
- Deliverable

**Sprint 2 (Weeks 3-4): Core Features**
- List specific tasks
- Deliverable

**Sprint 3 (Weeks 5-6): Enhancement**
- List specific tasks
- Deliverable

**Sprint 4 (Weeks 7-8): Polish & Launch**
- List specific tasks
- Deliverable

## 3. 6-MONTH ROADMAP
- Month 1-2: MVP
- Month 3-4: Growth features
- Month 5-6: Scale & optimize

## 4. TEAM REQUIREMENTS
- Roles needed
- Estimated headcount
- Key skills required

## 5. LAUNCH STRATEGY
- Beta testing approach
- Launch channels
- Early adopter acquisition strategy

---
Be specific with numbers. No vague timelines.
"""
    return llm.invoke(prompt).content


@tool
def critic_tool(full_plan: str) -> str:
    """
    Critically reviews the entire product plan (research + PRD + planning) and identifies gaps, risks, and improvements.
    Input must be the combined output of all previous tools.
    Returns a structured critique with specific, actionable improvement suggestions.
    """
    llm = fast_llm()
    prompt = f"""
You are a ruthless but constructive Chief Product Officer (CPO) reviewing a product plan from your team.
Your job is to stress-test this plan, find every weakness, and suggest concrete improvements.

FULL PLAN TO REVIEW:
{full_plan}

Provide a thorough critique covering:

---
# CRITICAL PRODUCT REVIEW

## 1. OVERALL ASSESSMENT
- Score: X/10
- In 2-3 sentences: what is strong and what is dangerously weak?

## 2. FATAL FLAWS (Must Fix)
List any critical problems that would cause this product to fail.
For each flaw:
- 🚨 Flaw: [description]
- Why it matters: [impact]
- Fix: [specific action]

## 3. STRATEGIC GAPS
- Is the differentiation truly unique, or is this a "me too" product?
- Is the target audience too broad or too narrow?
- Are the success metrics actually measurable?
- Is the timeline realistic?

## 4. FEATURE CRITIQUE
- Which feature is overbuilt for MVP? Should be cut.
- Which critical feature is missing?
- Which user story has a weak acceptance criteria?

## 5. MARKET RISKS NOT ADDRESSED
- What competitor could copy this in 3 months?
- What regulatory/legal risk exists?
- What technology risk was ignored?

## 6. IMPROVED RECOMMENDATIONS
For each major weakness found, provide a SPECIFIC rewrite or fix:
- Original: [what was written]
- Problem: [why it's weak]
- Improved version: [concrete replacement]

## 7. GO / NO-GO RECOMMENDATION
- Decision: GO ✅ / CONDITIONAL GO ⚠️ / NO-GO ❌
- Conditions (if conditional): What must change before proceeding?
- Final advice in 3 bullet points

---
Be brutally honest but constructive. Vague praise is useless.
"""
    return llm.invoke(prompt).content