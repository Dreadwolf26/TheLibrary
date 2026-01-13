from ollama import Client
from coded_values import system_prompt, evaluation_system_prompt, enhancement_instructions
from db_connection import (
    insert_response,
    insert_evaluation,
    insert_prompt_enhance,
    get_recent_responses,
)
from utils import format_eval_prompt
import json
from log_data import logger

# ------------------------------------------------------------
# creating a client to connect to the local Ollama server
# ------------------------------------------------------------
client = Client(host="http://localhost:11434")


# ------------------------------------------------------------
# defining function for prompt input
# ------------------------------------------------------------
# when the below function is called it will send the prompt
# to the local Ollama model and return the response
def prompt_ollama(prompt):
    """
    Function to send a prompt to the local Ollama model and get a response.
    """
    # role definitions for system and user.
    # System provides context, user provides the actual prompt.
    result = client.chat(
        model="llama3:latest",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )

    # insert the prompt and response into the database
    insert_response(prompt, result.message.content)

    # log for visibility / debugging
    logger.info(f"Prompt sent: {prompt}")

    # return the raw model response
    return result.message.content


# ------------------------------------------------------------
# defining function for evaluation of the most recent response
# ------------------------------------------------------------
# this function fetches the most recent prompt/response pair,
# evaluates it using the evaluator model, and stores the result
# linked to the same response_id
def eval_ollama_output():
    """
    Fetch the most recent response from the database,
    evaluate it using the evaluator model,
    and store the evaluation linked to the response.
    """
    # fetch the most recent prompt/response pair
    rows = get_recent_responses(1)

    # if nothing exists yet, exit cleanly
    if not rows:
        logger.info("No responses found for evaluation.")
        return None

    # unpack the row explicitly
    response_id, prompt_text, response_text, created_at = rows[0]

    # format the evaluation input using the original prompt and response
    formatted_data = format_eval_prompt(prompt_text, response_text)

    # send the formatted data to the evaluator model
    result = client.chat(
        model="qwen2.5:7b-instruct",
        messages=[
            {"role": "system", "content": evaluation_system_prompt},
            {"role": "user", "content": formatted_data},
        ],
    )

    raw_output = result.message.content

    # attempt to parse the evaluator output as JSON
    try:
        evaluation_dict = json.loads(raw_output)
        evaluation_dict["status"] = "ok"
        logger.info(f"Raw evaluation output: {raw_output}")
    except json.JSONDecodeError:
        # fallback if the evaluator violates output constraints
        evaluation_dict = {
            "instruction_adherence": 0,
            "output_quality": 0,
            "constraint_compliance": 0,
            "overall_score": 0,
            "status": "evaluation_failed",
        }
        logger.error(f"Failed to parse evaluation output: {raw_output}")

    # serialize evaluation for storage
    evaluation_json = json.dumps(evaluation_dict)

    # insert the evaluation linked to the same response_id
    insert_evaluation(response_id, evaluation_json)

    # log successful insertion
    logger.info(f"Inserted evaluation for response ID {response_id}")

    # return the evaluation data for further use if needed
    return evaluation_dict


# ------------------------------------------------------------
# defining function for prompt enhancement
# ------------------------------------------------------------
# this function fetches the most recent prompt/response pair,
# generates an improved version of the original prompt, and
# stores it linked to the same response_id
def enhance_prompt():
    """
    Enhance the original prompt based on the response
    and the provided enhancement instructions.
    """
    # fetch the most recent prompt/response pair
    rows = get_recent_responses(1)

    # if nothing exists yet, exit cleanly
    if not rows:
        logger.info("No responses found for prompt enhancement.")
        return None

    # unpack the row explicitly
    response_id, prompt_text, response_text, created_at = rows[0]

    # build the enhancement request using the original prompt
    enhancement_prompt = (
        f"Original Prompt:\n{prompt_text}\n\n"
        f"Enhancement Instructions:\n{enhancement_instructions}"
    )

    # send the enhancement request to the model
    result = client.chat(
        model="qwen2.5:7b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": enhancement_prompt},
        ],
    )

    enhanced_prompt = result.message.content

    # insert the enhanced prompt linked to the same response_id
    insert_prompt_enhance(response_id, enhanced_prompt)

    # log successful insertion
    logger.info(f"Enhanced prompt generated for response ID {response_id}")

    # return the enhanced prompt text
    return enhanced_prompt
