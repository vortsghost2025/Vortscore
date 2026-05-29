def safe_response(answer, confidence):
    if confidence < 0.2:
        return "I'm not confident enough to answer that.", "low"
    elif confidence < 0.5:
        return answer, "uncertain"
    return answer, "confident"
