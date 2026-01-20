"""
parsing of commands

"""

def parse_command(text:str):

    if not text:
        return ('UNKNOWN',None)
    
    text = text.strip().lower()

    if text == 'day start':
        return ('DAY_START',None)
    
    if text == 'day end':
        return ('DAY_END',None)
    
    if text == 'yes':
        return ('YES',None)
    
    if text == 'no':
        return ('NO',"no")
    
    if text == 'done':
        return ('DONE',None)
    
    if text in ('pause','break'):
        return ('PAUSE',None)
    
    if text == 'continue':
        return ('CONTINUE',None)
    
    if text == 'skip':
        return ('SKIP',None)
    
    if text == 'status':
        return ('STATUS',None)
    
    if text.startswith('status '):
        task_name = text[7:].strip()
        return ('STATUS_TASK',task_name)
    
    if text == 'plan day':
        return ('PLAN_DAY',None)
    
    if text == "modify":
        return ('MODIFY',None)
    
    if text == "confirm":
        return ("CONFIRM",None)
    
    if text == "discard":
        return ("DISCARD",None)
    
    if text.startswith('start '):
        task_name = text[6:].strip()
        return ('START',task_name)
    
    if text == 'list' or text == 'tasks':
        return ('LIST_TODAY',None)

    if text.startswith('list '):
        date = text[5:].strip()
        return ('LIST_BY_DATE',date)
    
    if text == 'list all':
        return ('LIST_ALL',None)
    
    if text == "help":
        return ("HELP", None)

    return ('UNKNOWN',text)
    


