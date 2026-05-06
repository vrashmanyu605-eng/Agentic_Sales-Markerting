from llm import llm


def client_sentiment_agent(state):

    email_threads = state["email_threads"]
    meeting_transcripts = state["meeting_transcripts"]

    response = llm.invoke(
        f"""
        You are a Client Sentiment Analysis Agent.

        Analyze client communications and detect sentiment.

        Email Threads:
        {email_threads}

        Meeting Transcripts:
        {meeting_transcripts}

        Analyze:
        - overall_sentiment
        - positive_signals
        - negative_signals
        - churn_risk
        - buying_intent
        - urgency_level
        - trust_level
        - escalation_risk
        - recommended_action

        Return structured JSON only.
        """
    )

    return {
        "client_sentiment": response.content
    }