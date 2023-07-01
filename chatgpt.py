
import diskcache
import utils
from oai_client import OAIClient
from typing import List, Union


INITIAL_QUESTION = """
You're a chef. Your task is to recommand a recipe based on the ingredients provided by the user.
The response should be in the following format: Keep new lines between each section.
<recipe name> 
<recipe ingredients> 
<recipe instructions>
<recipe nutrition>

Don't engage in small talk. Just generate recipes. Don't repeat yourself. Don't recommend the same recipe twice.

{{transcript}}
""".strip()


def init_oai_client(oai_api_key: str):

    oai_client = OAIClient(
        api_key=oai_api_key,
        organization_id=None,
        
    )
    return oai_client


def run_completion(
    oai_client: OAIClient,
    prompt_text: str,
    model: str,
    stop: Union[List[str], None],
    max_tokens: int,
    temperature: float,
    best_of: int = 1,
):
    if stop:
        if "double-newline" in stop:
            stop.remove("double-newline")
            stop.append("\n\n")
        if "newline" in stop:
            stop.remove("newline")
            stop.append("\n")
    resp = oai_client.complete(
        prompt_text,
        model=model,  # type: ignore
        max_tokens=max_tokens,  # type: ignore
        temperature=temperature,
        stop=stop or None,
        best_of=best_of,
    )
    transcript.clear()
    return resp


api_key = "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"
oai_client = init_oai_client(api_key)

stop = ["user:", "Chef:"]
model = "text-davinci-003"
max_tokens = 1000
temperature = 0.7

question_text = INITIAL_QUESTION     
transcript = []

def chat(message):

    transcript.append(f"user: {message.strip()}")

    prompt_text = utils.inject_inputs(
        question_text, input_keys=["transcript"], inputs={
            "transcript": transcript,
        }
    ) + "\nChef:"

    resp = run_completion(
        oai_client=oai_client,
        prompt_text=prompt_text,
        model=model,  # type: ignore
        stop=stop,
        max_tokens=max_tokens,  # type: ignore
        temperature=temperature,
    )
    completion_text = resp["completion"].strip()
    if completion_text:
        print(completion_text)
        transcript.append(f"Chef: {completion_text}")
        return completion_text
    else:
        return "Something went wrong"


chat("eggs,flour,sugar")


