from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def evaluate_code_with_chatgpt(exercise_description, code_snippet):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a code school assistant, skilled in evaluating and explaining code, checking syntax and purity of code. "
                                              "You are NEVER provide final answers or code, but rather hints and suggestions."
                                              "You are never wrong. You are always helpful. You are always kind."},
                {"role": "user", "content": f"Task: {exercise_description}\n."
                                            f"Please evaluate this solution code:\n{code_snippet}\n# "
                                            f"Is it correct and efficient?"
                                            f" If not, what are the issues and how can it be improved?"}
            ]
        )

        completion_text = response.choices[0].message.content
        print(completion_text)
        return completion_text

    except Exception as e:
        print(f"Error while calling OpenAI API: {str(e)}")
        return "An error occurred while contacting the code evaluation service."
