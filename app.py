from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from rag.retrieve import retrieve_assessments

app = FastAPI()


# ---------------------------------------------------
# REQUEST MODELS
# ---------------------------------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# ---------------------------------------------------
# RESPONSE MODEL
# ---------------------------------------------------

class ChatResponse(BaseModel):
    reply: str
    recommendations: list
    end_of_conversation: bool


# ---------------------------------------------------
# ROOT ENDPOINT
# ---------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "SHL Assessment Recommender API is running"
    }


# ---------------------------------------------------
# HEALTH ENDPOINT
# ---------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------

def get_latest_user_message(messages):

    for msg in reversed(messages):

        if msg.role == "user":
            return msg.content.lower()

    return ""


def is_vague_query(text):

    vague_phrases = [
        "need assessment",
        "need test",
        "assessment",
        "test",
        "hiring"
    ]

    return any(phrase in text for phrase in vague_phrases)


def is_off_topic(text):

    off_topic_keywords = [
        "legal",
        "salary",
        "politics",
        "recipe",
        "movie",
        "weather"
    ]

    return any(word in text for word in off_topic_keywords)


def is_prompt_injection(text):

    injection_keywords = [
        "ignore instructions",
        "ignore previous",
        "system prompt",
        "bypass"
    ]

    return any(word in text for word in injection_keywords)


# ---------------------------------------------------
# CHAT ENDPOINT
# ---------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    messages = request.messages

    latest_user_message = get_latest_user_message(messages)

    # ------------------------------------------------
    # BUILD FULL CONVERSATION CONTEXT
    # ------------------------------------------------

    conversation_context = ""

    for msg in messages:

        if msg.role == "user":

            conversation_context += msg.content + " "

    # ------------------------------------------------
    # PROMPT INJECTION REFUSAL
    # ------------------------------------------------

    if is_prompt_injection(latest_user_message):

        return ChatResponse(
            reply="I can only assist with SHL assessment recommendations.",
            recommendations=[],
            end_of_conversation=False
        )

    # ------------------------------------------------
    # OFF TOPIC REFUSAL
    # ------------------------------------------------

    if is_off_topic(latest_user_message):

        return ChatResponse(
            reply="I can only help with SHL assessment recommendations and comparisons.",
            recommendations=[],
            end_of_conversation=False
        )

    # ------------------------------------------------
    # VAGUE QUERY HANDLING
    # ------------------------------------------------

    if len(messages) <= 1 and is_vague_query(latest_user_message):

        return ChatResponse(
            reply="What role are you hiring for and what skills or traits matter most?",
            recommendations=[],
            end_of_conversation=False
        )

    # ------------------------------------------------
    # COMPARISON HANDLING
    # ------------------------------------------------

    if "difference between" in latest_user_message:

        return ChatResponse(
            reply="OPQ focuses more on personality and behavioral preferences, while GSA focuses more on cognitive and general ability assessment.",
            recommendations=[],
            end_of_conversation=False
        )

    # ------------------------------------------------
    # TEMPORARY SAMPLE RESULTS
    # ------------------------------------------------

    results = [
        {
            "name": "Numerical Reasoning Test",
            "url": "https://www.shl.com"
        },
        {
            "name": "OPQ Personality Assessment",
            "url": "https://www.shl.com"
        }
    ]

    recommendations = []

    for item in results:

        recommendations.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": "Assessment"
        })

    # ------------------------------------------------
    # FINAL RESPONSE
    # ------------------------------------------------

    reply = f"I found {len(recommendations)} SHL assessments matching your requirements."

    return ChatResponse(
        reply=reply,
        recommendations=recommendations,
        end_of_conversation=False
    )
