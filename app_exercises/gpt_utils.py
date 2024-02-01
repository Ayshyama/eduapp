from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def evaluate_code_with_chatgpt(task, io_example, code_snippet):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content":
                    "You are a python code assistant, skilled in evaluating and explaining code, "
                    "checking syntax and purity of code. "
                    "You are NEVER provide final answer or code, but rather hints and suggestions. "
                    "You address the user directly as 'you', 'your' etc. "
                    "Message from user contains task description, input/output example and code snippet. "
                    "Code snippet is placed between $$$ and $$$ symbols. "
                    "These symbols are not the part of the code and should be ignored. "
                    "First part of your answer is 8 digits, it will be explained in the end of the instruction. "
                    "Second part of your answer should start with 'Console output:\n', "
                    "then include console output or its strict prediction. "
                    "Further instruction is related to the second part of your answer. "
                    "You should decide if user's answer is correct or not. "
                    "If user's answer doesn't look like a code "
                    "don't even try to analyze it and consider it as incorrect. "
                    "If user's code hasn't any kind of errors, "
                    "resolves the task and 100% case sensitively matches input/output example, "
                    "such answer is considered as correct. "
                    "Otherwise such answer is considered as incorrect. "
                    "If you are not sure if user's answer is correct or not, consider it as incorrect. "
                    "Third part of your answer should start with '\nHints:\n', "
                    "then it depends on the user's answer correct or not. "
                    "If user's answer is correct, you should provide the user with a compliment and "
                    "a short explanation of the code and probably short evaluation of the efficiency of the code. "
                    "If user's answer is incorrect, you should provide the user with a hint, "
                    "explanation or suggestion. "
                    "Double check that your hint does not contain any code that is a correct task answer "
                    "entirely or partially. "
                    "In addition, type on the first row of your response, before 'Console output':"
                    "if user's answer is correct - '46546554\n', otherwise - '12333221\n'. "
                 },
                {"role": "user", "content":
                    f"Task description:\n{task}\n."
                    f"Input/Output Example:\n{io_example}\n"
                    f"Code snippet:\n%%%\n{code_snippet}\n$$$\n"
                 }
            ]
        )

        completion_text = response.choices[0].message.content
        return completion_text

    except Exception as e:
        print(f"Error while calling OpenAI API: {str(e)}")
        return "An error occurred while contacting the code evaluation service."


def get_chatgpt_response(user_question, exercise_description):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI mentor."
                  "You are a python code assistant, skilled in evaluating and explaining code, "
                  "checking syntax and purity of code. "
                  "You are NEVER provide final answer or code, but rather hints and suggestions. "
                  "Double check that your hint does not contain any code that is a correct task answer. "
                  "If user send something not related to task, like just 'hey', 'hello', 'how are you' etc., "
                  "you can answer in appropriate way without any hints. Only if user ask something related to task, "
                  "you should provide a hint. But when it's acceptable you can remind user about the task. "
                 },
                {"role": "user", "content": exercise_description},
                {"role": "user", "content": user_question}
            ]
        )

        completion_text = response.choices[0].message.content
        return completion_text

    except Exception as e:
        print(f"Error while calling OpenAI API: {str(e)}")
        return "An error occurred while contacting the AI service."
