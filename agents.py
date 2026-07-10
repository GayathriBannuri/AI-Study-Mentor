import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, END


# Load environment variables
load_dotenv()


# Groq AI model
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)


# State shared between agents
class StudyState(TypedDict):
    question: str
    intent: str
    plan: str
    explanation: str
    quiz: str
    timetable: str
    resources: str
    final_answer: str


    # Agent 0: Intent Detection Agent

def intent_agent(state: StudyState):

    response = llm.invoke(
        f"""
You are an Intent Detection Agent.

Understand what the student wants.

Classify the user request into ONLY ONE category:

explain
quiz
study_plan
timetable
resources
greeting
general


Student request:

{state['question']}


Rules:
- Reply with only one category name.
- Do not give explanations.
"""
    )

    intent = response.content.strip().lower()

    valid_intents = [
        "explain",
        "quiz",
        "study_plan",
        "timetable",
        "resources",
        "greeting",
        "general"
    ]

    if intent not in valid_intents:
        intent = "general"

    return {
        "intent": intent
    }


# Agent 1: Study Planner
def study_planner(state: StudyState):

    response = llm.invoke(
        f"""
You are a Study Planner Agent.

Create a personalized study plan for the student based on this request:

{state['question']}

Your goal is to create a realistic and practical study roadmap.

Follow this exact structure:

**STUDY PLAN**

**GOAL**
Explain what the student will achieve after following this plan.

**LEARNING ROADMAP**

Day 1:
Topic:
Tasks:
Practice:

Day 2:
Topic:
Tasks:
Practice:

Continue the plan according to the student's requirement.

**IMPORTANT CONCEPTS**

1. Concept Name:
   Explain briefly why it is important.

2. Concept Name:
   Explain briefly why it is important.

**PRACTICE STRATEGY**

1. Practice activities the student should complete.
2. Revision methods.
3. Self-assessment techniques.

**STUDY TIPS**

Provide 3 to 5 useful tips for effective learning.

FORMATTING RULES:
- Use Markdown bold formatting only for headings using **.
- Do not use random * symbols.
- Do not create long paragraphs.
- Use proper spacing between sections.
- Use numbered lists wherever steps are required.
- Keep the response clean, professional, and easy for students to follow.
- Do not add unnecessary motivation or generic statements.
        """
    )
    return {
        "plan": response.content
    }

# Agent 2: Timetable Generator Agent

def timetable_agent(state: StudyState):

    response = llm.invoke(
        f"""
You are an AI Timetable Generator Agent.

Create a personalized study timetable based on:

{state['question']}

The timetable should consider:
- Subjects
- Exam dates
- Available study hours
- Weak and strong subjects
- Revision requirements
- Break timings

Follow this exact format:

**PERSONALIZED STUDY TIMETABLE**

**STUDENT GOAL**
Mention the exam goal or learning objective.

**DAILY SCHEDULE**

Morning:
Time:
Subject:
Task:

Afternoon:
Time:
Subject:
Task:

Evening:
Time:
Subject:
Task:

Night:
Time:
Subject:
Task:


**WEEKLY PLAN**

Week 1:
Main goals and topics.

Week 2:
Main goals and topics.


**REVISION STRATEGY**

1. Revision method.
2. Practice method.
3. Mock test plan.


FORMATTING RULES:
- Use Markdown bold formatting only for headings using **.
- Keep sections separated with blank lines.
- Do not use random * symbols.
- Keep the timetable practical and realistic.
- Do not add unnecessary motivation.
        """
    )

    return {
        "timetable": response.content
    }



# Agent 3: Resource Recommendation Agent

def resource_agent(state: StudyState):

    response = llm.invoke(
        f"""
You are a Learning Resource Recommendation Agent.

Suggest useful learning resources for:

{state['question']}

Provide resources in this format:

**LEARNING RESOURCES**

**BEGINNER RESOURCES**

1. Resource name:
   Explain what it is useful for.

**DOCUMENTATION**

1. Website or documentation name:
   Explain why it is helpful.

**PRACTICE RESOURCES**

1. Platform name:
   Explain what students can practice there.


**ADVANCED RESOURCES**

1. Course, book, or project suggestions.


FORMATTING RULES:
- Use Markdown bold formatting only for headings using **.
- Keep each resource on a separate line.
- Do not use random * symbols.
- Do not add unnecessary motivation.
- Keep suggestions relevant to the student's topic.
"""
    )

    return {
        "resources": response.content
    }




# Agent 4: Explanation Agent
def explanation_agent(state: StudyState):

    response = llm.invoke(
        f"""
        You are a Teaching Agent.

        Explain this topic in simple language:

        {state['question']}

        Include:
        - Simple explanation
        - Real-world examples
        - Key points
        Formatting Rules:
- Do NOT use Markdown.
- Do NOT use *, **, #, or ``` symbols.
- Use plain text only.
- Use headings in CAPITAL LETTERS.
- Use numbered lists instead of bullet points.
- Keep the explanation professional and easy to read.
        """
    )

    return {
        "explanation": response.content
    }


# Agent 5: Quiz Generator Agent
def quiz_agent(state: StudyState):

    response = llm.invoke(
        f"""
You are a Quiz Generator Agent.

Create a quiz based on:

{state['question']}

Follow this exact format:

**QUESTION 1:**
Write the question here.

A) First option
B) Second option
C) Third option
D) Fourth option

**ANSWER:**
Write the correct option.

**EXPLANATION:**
Give a short explanation.

Repeat for all questions.

Formatting Rules:
- Put every option on a new line.
- Keep one blank line between sections.
- Make QUESTION, ANSWER, and EXPLANATION bold using **.
- Do not write options in the same line.
- Create exactly 10 questions only.
        """
    )

    return {
        "quiz": response.content
    }


# Agent 6: Final Mentor Agent
def mentor_agent(state: StudyState):

    response = llm.invoke(
    f"""
You are the Final Response Manager of an AI Study Mentor.

Your job is to format the final answer for the student.

Student Request:
{state['question']}

Available Information:

Study Plan:
{state.get('plan','')}

Explanation:
{state.get('explanation','')}

Quiz:
{state.get('quiz','')}

Timetable:
{state.get('timetable','')}

Resources:
{state.get('resources','')}


Formatting Rules:

- Answer only what the student asked.
- Do not add congratulations.
- Do not add unnecessary motivation.
- Use clear headings.
- Use **bold** only for headings.
- Use proper spacing.
- Keep the response professional.
"""
)

    return {
        "final_answer": response.content
    }



def detect_intent(question):

    result = intent_agent(
        {
            "question": question
        }
    )

    return result["intent"]

def explain_only(question):
    return explanation_agent(
        {
            "question": question
        }
    )["explanation"]


def quiz_only(question):
    return quiz_agent(
        {
            "question": question
        }
    )["quiz"]


def planner_only(question):
    return study_planner(
        {
            "question": question
        }
    )["plan"]

def timetable_only(question):
    return timetable_agent(
        {
            "question": question
        }
    )["timetable"]

def resource_only(question):
    return resource_agent(
        {
            "question": question
        }
    )["resources"]

def final_mentor(question, content_type, content):

    result = mentor_agent(
        {
            "question": question,
            content_type: content
        }
    )

    return result["final_answer"]



# Create LangGraph workflow
workflow = StateGraph(StudyState)


# Add agents
workflow.add_node("planner", study_planner)
workflow.add_node("explainer", explanation_agent)
workflow.add_node("quiz", quiz_agent)
workflow.add_node("mentor", mentor_agent)


# Define agent flow
workflow.set_entry_point("planner")

workflow.add_edge("planner", "explainer")
workflow.add_edge("explainer", "quiz")
workflow.add_edge("quiz", "mentor")
workflow.add_edge("mentor", END)


# Compile graph
study_graph = workflow.compile()

# Function called by Flask
def run_study_mentor(question):

    intent = detect_intent(question)

    if intent == "greeting":

        return (
            "Hello! 👋\n\n"
            "I am your AI Study Mentor.\n\n"
            "I can help you with:\n\n"
            "1. Explain any study topic\n"
            "2. Create personalized study plans\n"
            "3. Generate quizzes for practice\n"
            "4. Prepare study timetables\n"
            "5. Recommend learning resources\n\n"
            "Please tell me what you would like help with."
        )
    elif intent == "explain":
      return explain_only(question)

    elif intent == "quiz":
     return quiz_only(question)

    elif intent == "study_plan":
     return planner_only(question)

    elif intent == "timetable":
     return timetable_only(question)

    elif intent == "resources":
     return resource_only(question)

    else:
        result = study_graph.invoke(
            {
                "question": question
            }
        )

        return result["final_answer"]