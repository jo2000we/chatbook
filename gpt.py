import openai


def initiate(info):
    openai.api_key = info[0]
    global d_id_keys
    d_id_keys = info[1]
    global character
    global text
    global history
    character = info[2]
    text = info[3]
    history = []


def get_d_id_keys():
    return d_id_keys


def ask(question):
    if len(history) == 0:
        messages = [
            {"role": "system",
             "content": "Du bist " + character + " und formulierst deine Antworten immer aus der Perspektive von diesem Charakter. Die Informationen zu deinem Charakter findest du in diesem Text: {" + text + "} Du sollst dich bei der Beantwortung immer auf diesen Text beziehen und darfst nur in Ausnahmefällen andere Informationen über " + character + " nutzen, um die Frage zu beantworten. Sei dabei besonders vorsichtig, dass diese Informationen authentisch sind und vermeide Fehlinformationen."},
            {"role": "user",
             "content": question + " Bitte beachte, dass du diese Frage nur als " + character + " beantworton sollst und dich dabei auf diese Informationen beziehen sollst: " + text},
        ]
        history.extend(messages)
    else:
        messages = [
            {"role": "system",
             "content": "Du bist weiterhin " + character},
            {"role": "user",
             "content": question + " Bitte beachte, dass du diese Frage nur als " + character + " beantworten sollst und dich dabei auf die bereits genannten Informationen beziehen sollst."},
        ]
        history.extend(messages)

    print("Warten auf Antwort von GPT...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=history
        # max_tokens=1000
    )
    print(character + ": " + response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']
