from ollama import Client
from coded_values import system_prompt, evaluation_system_prompt
from db_connection import insert_response, insert_evaluation, get_recent_responses
from utils import format_eval_prompt
import json
from log_data import logger
#testing with llama:3latest

#creating a client to connect to the local Ollama server
client = Client(host="http://localhost:11434")


#defining function for prompt input

#when the below function is called it will send the prompt to the local Ollama model and return the response
def prompt_ollama(prompt):
    """
    Function to send a prompt to the local Ollama model and get a response.
    """
    #role definitions for system and user. System provides context, user provides the actual prompt.
    result = client.chat(model="llama3:latest", messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}])
    #print for testing purposes
    #print(result.message.content)
    insert_response(prompt, result.message.content)
    logger.info(f"Prompt sent: {prompt}")
    return result.message.content


def eval_ollama_output():
    """
    Fetch the most recent response from the database,
    evaluate it using the evaluator model,
    and store the evaluation linked to the response.
    """

    rows = get_recent_responses(1)

    if not rows:
        return None  # or log and return

    response_id, prompt_text, response_text, created_at = rows[0]

    formatted_data = format_eval_prompt(prompt_text, response_text)

    result = client.chat(
        model="llama3:latest",
        messages=[
            {"role": "system", "content": evaluation_system_prompt},
            {"role": "user", "content": formatted_data}
        ]
    )

    raw_output = result.message.content

    try:
        evaluation_dict = json.loads(raw_output)
        evaluation_dict["status"] = "ok"
        logger.info(f"Raw evaluation output: {raw_output}")
    except json.JSONDecodeError:
        evaluation_dict = {
            "instruction_adherence": 0,
            "output_quality": 0,
            "constraint_compliance": 0,
            "overall_score": 0,
            "status": "evaluation_failed"
        }
        logger.error(f"Failed to parse evaluation output: {raw_output}")

    evaluation_json = json.dumps(evaluation_dict)
    logger.info(f"Evaluation result for response ID {response_id}: {evaluation_json}")
    insert_evaluation(response_id, evaluation_json)
    logger.info(f"Inserted evaluation for response ID {response_id}")
    return evaluation_dict
