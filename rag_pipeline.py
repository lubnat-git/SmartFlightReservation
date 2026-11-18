import requests

from knowledge_base.search_knowledge import search_knowledge


SIMILARITY_THRESHOLD = 0.40

OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "qwen3:1.7b"


def retrieve_context(question, top_k=3):
    results = search_knowledge(question, top_k=top_k)

    relevant_results = [
        result for result in results
        if result["similarity"] >= SIMILARITY_THRESHOLD
    ]

    if not relevant_results:
        return "No relevant information found in the knowledge base.", []

    context_parts = []

    for result in relevant_results:
        context_parts.append(
            f"Source: {result['source']}\n"
            f"Information: {result['text']}"
        )

    context = "\n\n".join(context_parts)

    return context, relevant_results


def generate_answer(question, context):

    prompt = f"""
You are a travel assistant for a flight reservation system.

Answer the user's question using ONLY the information
provided in the knowledge base context.

STRICT RULES:
1. Do not invent policies, prices, services, or features.
2. Do not use external airline information.
3. Do not assume features that are not documented.
4. If the answer is unavailable in the context, say:
   "I don't have enough information in my knowledge base to answer that."
5. Keep answers clear, concise, and accurate.
6. Clearly identify simulated features as simulated.

KNOWLEDGE BASE CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "think": False,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 150
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    answer = response.json().get("response", "").strip()

    if not answer:
        return (
            "I couldn't generate an answer. "
            "Please try again."
        )

    return answer


def ask_travel_assistant(question):

    if not question or not question.strip():
        return {
            "answer": "Please enter a travel-related question.",
            "sources": []
        }

    context, sources = retrieve_context(question)

    if not sources:
        return {
            "answer": (
                "I don't have enough relevant information "
                "in my knowledge base to answer that question."
            ),
            "sources": []
        }

    try:
        answer = generate_answer(question, context)

        return {
            "answer": answer,
            "sources": sorted(
                set(source["source"] for source in sources)
            )
        }

    except requests.RequestException:
        return {
            "answer": (
                "The travel assistant is temporarily unavailable. "
                "Please try again later."
            ),
            "sources": []
        }


if __name__ == "__main__":

    question = input("Ask your travel question: ")

    result = ask_travel_assistant(question)

    print("\nTRAVEL ASSISTANT")
    print("================")

    print(result["answer"])

    print("\nSOURCES")

    for source in result["sources"]:
        print("-", source)