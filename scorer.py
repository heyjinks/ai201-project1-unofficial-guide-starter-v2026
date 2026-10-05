def judge(question, expects, answer, results) -> bool:
    if not answer:
        return False

    answer_lower = answer.lower()

    if isinstance(expects, str):
        expects = [expects]

    return any(expected.lower() in answer_lower for expected in expects)