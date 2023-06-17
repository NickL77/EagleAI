import logging
import requests
import yaml

import pprint

EVALUATION_ENDPOINT = "https://hawki-ai-apy-ru3xb.ondigitalocean.app/evaluate"

def evaluate(model_responses: dict, evaluation_config: str):

    evaluation_results = {}

    with open(evaluation_config) as f:
        evaluation_criteria = yaml.load(f, Loader=yaml.FullLoader)

    for test_name in model_responses:

        model_response = model_responses.get(test_name, None)
        criteria_ls = evaluation_criteria.get(test_name, {}).get("criteria", [])

        if not (evaluation_criteria and model_response and criteria_ls):
            logging.warning(f"Could not evaluate test case: { test_name }")
            continue

        request_body = {
                "generated_response": model_response,
                "criteria": criteria_ls
        }

        r = requests.post(url=EVALUATION_ENDPOINT, json=request_body)
        # print(r.json())

        evaluation_results[test_name] = r.json()

    # pprint.pprint(evaluation_results)
    pretty_print_results(evaluation_results)

def pretty_print_results(evaluation_results, verbose=False):
    # TODO: add verbse printing

    total_pass, total_fail = 0, 0
    
    pretty_string = "\n\n---EagleAI Evaluation Results------------------------------------\n\n"
    for test_name in evaluation_results:
        
        test_results_string = ""
        num_pass, num_fail = 0, 0
        for evaluation_result in evaluation_results[test_name]:
            pass_criteria = evaluation_result["pass"]
            criteria = evaluation_result["criteria"]
            reason = evaluation_result["reason"]
            if pass_criteria:
                test_results_string += f"  PASSED: { criteria } \n"
                num_pass += 1
                total_pass += 1
            else:
                test_results_string += f"  FAILED: { criteria } \n"
                test_results_string += f"    reason: { reason } \n"
                num_fail += 1
                total_fail += 1
        
        
        pretty_string += f"{ test_name } ({num_pass}/{num_fail + num_pass} passed):\n"
        pretty_string += test_results_string
        pretty_string += "\n"

    pretty_string += f"--------------------({total_pass}/{total_pass + total_fail} criteria passsed)-----------------------"
    pretty_string += "\n\n"
    print(pretty_string)
        
        
'''

def main():
    response_dict = {
    "artichokes": "Artichoke Basille's Pizza is a classic Berkeley establishment, originally from NYC, that offers large, delicious slices of pizza for a good price. The artichoke pizza is especially popular, with its creamy, rich flavor and generous amount of artichoke pieces. Other popular slices include the pepperoni and margarita. Service is fast and friendly, and the store is open late for late night cravings. However, some customers have noted that the pizza can be overly salty and the staff can be difficult to understand. Overall, Artichoke Basille's Pizza is a great spot for a cheap, filling meal.",
    "sliver": "The restaurant is average",
    "other-restaurant": "meh"
    }

    evaluate(response_dict, "evallm.yaml")

if __name__ == "__main__":
    main()
'''
