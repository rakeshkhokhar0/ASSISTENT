"""
connect with model
Generate daily plan
Adjust remain plan
Suggest next task
"""
from typing import Tuple,List,Dict,Optional
import json 
from model_interface import call_model

def generate_day_plan(context:dict) -> Optional[List[dict]]:
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
                "order": int,
                "description": str,
                "time":str
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
    
    plan = _extract_json(raw_output)
    if not plan:
        return None
    
    # validate structure
    # print(plan)
    if not _validate_plan(plan):
        return None
    
    plan.sort(key=lambda x : x['order'])

    for idx,task in enumerate(plan,start=1):
        task['order'] = idx

    return plan 



def _build_prompt(context: Dict) -> str:
    lines = []
    lines.append("You are an AI study planner.")
    lines.append("Create a structured ONE-DAY study plan.")
    lines.append("Focus on logical learning progression, not urgency.")
    lines.append("")
    lines.append("Rules:")
    lines.append("- Tasks must be ordered by learning sequence (1 = learn first).")
    lines.append("- Each task must build on the previous one.")
    lines.append("- Keep tasks realistic for the available time.")
    lines.append("- Do NOT include explanations.")
    lines.append("- Output ONLY valid JSON.")
    lines.append("")

    lines.append("Context:")
    if context.get('current_topic'):
        lines.append(f"Current topic: {context['current_topic']}")

    if context.get('recent_tasks'):
        lines.append("recently completed tasks:")
        for task in context['recent_tasks']:
            lines.append(f"-{task}")

    if context.get('unfinished_tasks'):
        lines.append("unfinished tasks:")
        for task in context['unfinished_tasks']:
            lines.append(f"-{task}")

    
    lines.append(f"Today's goal: {context.get('goal','')}")
    lines.append(f"Available time: {context.get('time_hours',0)} hours")
    lines.append(f"Learning intensity: {context.get('intensity','normal')}")
    lines.append("")

    lines.append("Output format (JSON only):")
    lines.append(
        """
        
        [
            {
            "name": "Task name",
            "order": 1,
            "description": "Short description",
            "time": "2hrs"
            }
        ]
        """
    )

    return "\n".join(lines)
    
def modify_day_plan(plan:dict, instruction:str, context:dict) -> List|None:
    """
    Modify an existing day plan based on user instruction.

    current_plan: validated list of tasks
    instruction: user request describing changes
    context: same context used for initial planning
    """

    # built prompt for modify plan
    lines = []
    lines.append("You are an AI study planner.")
    lines.append("You are modifying an existing ONE-DAY study plan.")
    lines.append("Apply the user's requested changes carefully.")
    lines.append("")
    lines.append("Rules:")
    lines.append("- Keep logical learning progression.")
    lines.append("- Do NOT repeat completed content unnecessarily.")
    lines.append("- Keep workload realistic for the available time.")
    lines.append("- Output ONLY valid JSON.")
    lines.append("- Output the FULL updated plan.")
    lines.append("")

    lines.append("Current plan:")
    for task in plan:
        lines.append(
            f"{task['order']}. {task['name']}\nTime: {task['time']}"
        )

    lines.append("")
    lines.append("User requested change:")
    lines.append(instruction)
    lines.append("")

    lines.append("Context:")
    if context.get('current_topic'):
        lines.append(f"Current topic: {context['current_topic']}")

    if context.get('recent_tasks'):
        lines.append("recently completed tasks:")
        for task in context['recent_tasks']:
            lines.append(f"-{task}")

    if context.get('unfinished_tasks'):
        lines.append("unfinished tasks:")
        for task in context['unfinished_tasks']:
            lines.append(f"-{task}")

    
    lines.append(f"Today's goal: {context.get('goal','')}")
    lines.append(f"Available time: {context.get('time_hours',0)} hours")
    lines.append(f"Learning intensity: {context.get('intensity','normal')}")
    lines.append("")

    lines.append("Output format (JSON only):")
    lines.append(
        """
        
        [
            {
            "name": "Task name",
            "order": 1,
            "description": "Short description",
            "time": "2hrs"
            }
        ]
        """
    )

    prompt = "\n".join(lines)

    raw_output = call_model(prompt)

    new_plan = _extract_json(raw_output)
    if not new_plan:
        return None
    
    if not _validate_plan(new_plan):
        return None
    
    new_plan.sort(key=lambda x : x['order'])

    for idx,task in enumerate(plan,start=1):
        task['order'] = idx

    return new_plan 




def _validate_plan(plan: List[Dict]) -> bool:
    if not isinstance(plan, list) or not 1 <= len(plan):
        return False

    for task in plan:
        if not isinstance(task, dict):
            return False

        try:
            task['order'] = int(task["order"])
        except Exception:
            return False
        
        task["name"]=task["name"].strip()
        task["description"]=task["description"].strip()
        task["time"]=task["time"].strip()

        if not all(k in task for k in ("name", "order", "description","time")):
            return False

        if not isinstance(task["name"], str):
            return False

        if not isinstance(task["order"], int):
            return False

        if not isinstance(task["description"], str):
            return False
        if not isinstance(task["time"],str):
            return False
    return True


def _extract_json(text:str):

    # print(text)
    if not text:
        return None
        
    # print(json_text)
    start = text.find('[')
    end = text.find(']')

    if start == -1 or end == -1:
        return None
     
    try:
        return json.loads(text[start:end+1])
    except Exception:
        return None
