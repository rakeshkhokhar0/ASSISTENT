"""
connect with model
Generate daily plan
Adjust remain plan
Suggest next task
"""
from typing import Tuple,List,Dict,Optional
import json 
import re
from model_interface import call_model

def generate_day_plan(context:dict) -> Optional[Tuple[dict]]:
    """
    Generate a structured day plan using the model.

    Input:
        context = {
            "goal": str,
            "time_hours": int | float,
            "intensity": str,
            "unfinished_tasks": list[str]
        }

    Output:
        [
            {
                "name": str,
                "priority": int,
                "description": str
            },
            ...
        ]
        OR None if generation fails
    """


    #1. prompt builder
    prompt = _build_prompt(context)


    #2. call model
    raw_output = call_model(prompt)
    # print(raw_output)
    #3.parse model output
    try:
        plan = _extract_json(raw_output)
        if not plan:
            return None
    except:
        return None
    
    for task in plan:
        task['priority'] = _normalize_priority(task.get('priority'))

    final_plan = _sort_priority(plan)
    # validate structure
    # print(final_plan)
    if not _validate_plan(final_plan):#type: ignore
        return None
    
    return plan



def _build_prompt(context: Dict) -> str:
    return f"""
    Create a study plan for today.

    Goal:
    {context['goal']}

    Available time:
    {context['time_hours']} hours

    Intensity:
    {context['intensity']}

    Unfinished tasks:
    {', '.join(context['unfinished_tasks']) if context['unfinished_tasks'] else 'None'}

    Rules:
    - Maximum 6 tasks
    - Output ONLY valid JSON array
    - Each task must include: name, priority, description
    """



def _validate_plan(plan: List[Dict]) -> bool:
    if not isinstance(plan, list) or not (1 <= len(plan) <= 6):
        return False

    priorities = set()

    for task in plan:
        if not isinstance(task, dict):
            return False

        if not all(k in task for k in ("name", "priority", "description")):
            return False

        if not isinstance(task["name"], str):
            return False

        if not isinstance(task["priority"], int):
            return False

        if not isinstance(task["description"], str):
            return False

        if task["priority"] in priorities:
            return False

        priorities.add(task["priority"])

    return True


def _extract_json(text:str):

    # print(text)
    if not text:
        return None
    
    match = re.search(r"```json\s*(.*?)\s*```",text,flags=re.DOTALL)
    
    json_text = match.group(1)#type: ignore
    # print(json_text)
    start = json_text.find('[')
    end = json_text.find(']')

    if start == -1 or end == -1:
        return None
     
    try:
        return json.loads(json_text[start:end+1])
    except Exception:
        return None


def _normalize_priority(value):
    if isinstance(value,int):
        return value
    
    mapping = {
        "high": 1,
        "medium":2,
        "low":3
    }
    return mapping.get(str(value).lower())


def _sort_priority(plan:list):
    s_plan = sorted(plan,key=lambda d:d['priority'])
    # print(s_plan)
    for i in range(len(s_plan)):
        s_plan[i]['priority'] = i+1

    return s_plan



