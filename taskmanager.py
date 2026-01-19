"""
Track tasks in real time
"""
from datetime import datetime
import appdatabase.database as db

HELP_TEXT = """
Available Commands:

Day Control:
- day start        : Start your day session
- day end          : End your day session

Task Control:
- start <task>     : Start a new task (auto-pauses current)
- pause / break    : Pause the current task
- continue         : Resume paused task
- done             : Complete current task
- skip             : Skip current task (explicit)

Information:
- status           : Show current active task
- plan             : Show today’s plan
- list / tasks     : List today’s tasks
- list YYYY-MM-DD  : List tasks by date
- list all         : List all tasks (admin)

Help:
- help             : Show this help message
""".strip()

global PENDING_CONFIRMATION_TASK_ID 
PENDING_CONFIRMATION_TASK_ID = None
def handle_command(command, payload):
    """
    main entry point to handle all commands
    """
    global PENDING_CONFIRMATION_TASK_ID
    if command == 'HELP':
        return ("OK ",HELP_TEXT)
    
    if command == 'DAY_START':
        active_session = db.get_active_session()

        if active_session:
            return ("ERROR","Day already started.")
        
        session_id = db.start_day_session()
        return ("OK","Day started successfully.")
    
    if command == "DAY_END":
        active_session = db.get_active_session()
        if not active_session:
            return ("ERROR","No active Day.")
        
        session_id = active_session[0]
        db.close_all_active_tasks(session_id)
        db.end_day_session(session_id)

        return ("OK","Day ended Successfully.")
    
    if command == 'STATUS':
        active_session = db.get_active_session()
        if not active_session:
            return ("ERROR","No active day. Start the day first.")
        
        session_id = active_session[0]
        active_task = db.get_active_task(session_id)

        if not active_task:
            return ("OK","No active task right now.")
        
        task_name = active_task[2]
        task_status = active_task[-1]

        return ("OK",f"Current task: {task_name} ({task_status}).")
    
    if command == 'DONE':
        # global PENDING_CONFIRMATION_TASK_ID
        active_session = db.get_active_session()
        if not active_session:
            return ("ERROR","No active session.")
        
        session_id = active_session[0]

        active_task = db.get_active_task(session_id)
        if not active_task:
            return ("ERROR","NO active task.")
        
        task_id = active_task[0]
        db.complete_task(task_id)
        
        # 1. for resume pause tasks 
        paused = db.get_paused_task_by_priority(session_id)
        if paused:
            paused_top = paused[0]
            paused_top_name =paused_top[2]
            PENDING_CONFIRMATION_TASK_ID = paused_top[0]
            return ("OK",f"Task Completed. You have an unfinished task: '{paused_top_name}'.\n""Would you like to resume this task?(yes/no)...")
        
        # 2. task in pending_task
        pending_task = db.get_pending_tasks_by_priority(session_id)

        if not pending_task:
            return ("OK","Task completed. All task for today is completed.")

        next_task = pending_task[0]
        next_task_id = next_task[0]
        next_task_name = next_task[2]
        PENDING_CONFIRMATION_TASK_ID = next_task_id

        return ("OK",f"Task completed. Next task suggestion : '{next_task_name}'""start this task now? (yes/no)...")

    if command =="YES":
        # global PENDING_CONFIRMATION_TASK_ID
        active_session = db.get_active_session()
        if not active_session:
            return ("ERROR","NO active session.")
        session_id = active_session[0]
        
        if not PENDING_CONFIRMATION_TASK_ID:
            return ("OK","No task to confirm.")
        
        task_id = PENDING_CONFIRMATION_TASK_ID
        PENDING_CONFIRMATION_TASK_ID = None
        active = db.get_active_task(session_id)
        if active:
            db.pause_task(active[0], "SWITCH")
        db.resume_or_start_task(task_id)

        return ("OK","Task started.")
    
    if command == "NO":
        # global PENDING_CONFIRMATION_TASK_ID
        PENDING_CONFIRMATION_TASK_ID = None

        active_session = db.get_active_session()
        if not active_session:
            return ("ERROR","NO active session.")
        
        session_id = active_session[0]

        paused_task = db.get_paused_task_by_priority(session_id)
        pending_task = db.get_pending_tasks_by_priority(session_id)
        task_list = []
        suggestion = None
        task_list.append("Okay, let’s choose what to do next.\n")
        if paused_task:
            task_list.append("Paused Task(Unfinished work):\n")
            for i, task in enumerate(paused_task, start = 1):
                task_list.append(f"{i}. {task[2]}")

            suggestion = paused_task[0]

        if pending_task:
            task_list.append("Pending tasks(not started yet)\n")
            for i, task in enumerate(pending_task, start=1):
                task_list.append(f"{i}. {task[2]}")
            if not suggestion:
                suggestion = pending_task[0]
            
        if not paused_task and not pending_task:
            return(
                "OK",
                "Great job \n\nAll tasks for today are completed.\n\n"
                "You can:\n"
                "- end day\n"
                "- plan new tasks\n"
                "- help"
            )

        task_list.append(f"Suggested task: {suggestion[2]}\n") #type: ignore
        task_list.append(f"Type:")
        task_list.append(f"-start <task name>")
        task_list.append(f"--help")

        return ("OK","\n".join(task_list))

    if command == "PAUSE":
        # global PENDING_CONFIRMATION_TASK_ID
        PENDING_CONFIRMATION_TASK_ID = None
        active_session = db.get_active_session()
        if not active_session:
            return ("ERROR", "No active session")
        
        session_id = active_session[0]
        active_task = db.get_active_task(session_id)
        if not active_task:
            return ("ERROR","No active task to pause")
        
        active_task_id = active_task[0]
        db.pause_task(active_task_id, "BREAK")
        return ("OK", "Task paused.")

    if command == "CONTINUE":
        # global PENDING_CONFIRMATION_TASK_ID
        PENDING_CONFIRMATION_TASK_ID = None

        active_session = db.get_active_session()
        if not active_session:
            return ("ERROR", "No active session.")

        session_id = active_session[0]
        break_task = db.get_break_pause_task(session_id)
        
        if not break_task:
            return ("ERROR","No active task to pause.")

        now = datetime.now()
        pause_time = datetime.fromisoformat(break_task[9])
        pause_duration = int((now - pause_time).total_seconds())
        pause_task_id = break_task[0]
        db.resume_task(pause_task_id,pause_duration) 

        return ("OK",f"Task resumed {break_task[2]}.")    

        # Completed tasks are not resumed. Restarting creates a new revision (future feature).

    if command == "SKIP":
        active_session = db.get_active_session()
        if not active_session:
            return ("ERROR","NO active day. Start the day first.")
        
        session_id = active_session[0]
        active_task = db.get_active_task(session_id)

        if not active_task:
            return ("ERROR","No active task.")
        
        active_task_id = active_task[0]
        db.skip_task(active_task_id)

        paused_task = db.get_paused_task_by_priority(session_id)
        pending_task = db.get_pending_tasks_by_priority(session_id)
        task_list = []
        suggestion = None
        task_list.append("Okay, let’s choose what to do next.\n")
        if paused_task:
            task_list.append("Paused Task(Unfinished work):\n")
            for i, task in enumerate(paused_task, start = 1):
                task_list.append(f"{i}. {task[2]}")

            suggestion = paused_task[0]

        if pending_task:
            task_list.append("Pending tasks(not started yet)\n")
            for i, task in enumerate(pending_task, start=1):
                task_list.append(f"{i}. {task[2]}")
            if not suggestion:
                suggestion = pending_task[0]
            
        if not paused_task and not pending_task:
            return(
                "OK",
                "Great job \n\nAll tasks for today are completed.\n\n"
                "You can:\n"
                "- end day\n"
                "- plan new tasks\n"
                "- help"
            )

        task_list.append(f"Suggested task: {suggestion[2]}\n") #type: ignore
        task_list.append(f"Type:")
        task_list.append(f"-start <task name>")
        task_list.append(f"--help")

        return ("OK","\n".join(task_list))

    if command == "START":
        # global PENDING_CONFIRMATION_TASK_ID
        if not payload:
            return ("ERROR","Task name required.")
        
        active_session = db.get_active_session()
        if not active_session:
            return ("ERROR","NO active day. Start the day first.")
        
        session_id = active_session[0]
        requested_task_name = payload.strip().lower()
        active_task = db.get_active_task(session_id)
        if active_task:
            if active_task[2].lower() == requested_task_name:
                return ("ERROR","Task is already active.")


        # if task in paused task  
        paused = db.get_paused_task_by_priority(session_id)
        if paused:
            for task in paused:
                if task[2].lower() == requested_task_name:
                    PENDING_CONFIRMATION_TASK_ID = None

                    if active_task:
                        db.pause_task(active_task[0],"SWITCH")
                    db.resume_or_start_task(task[0])
                    return ("OK",f"Resumed task '{requested_task_name}'")

        # Find requested task in today's plan
        todays_task = db.get_tasks_by_session(session_id)
        requested_task = next((task for task in todays_task if task[2].lower().strip() == requested_task_name),None)


        pending_tasks = db.get_pending_tasks_by_priority(session_id)
        if not pending_tasks:
            return ("ERROR", "No pending tasks available today.")
        next_task = pending_tasks[0]
        next_task_name = next_task[2]
        

        # if requested task in pending_task
        if requested_task:

            if paused:
                top_paused = paused[0]
                if top_paused[4] < requested_task[4]:  # priority comparison
                    PENDING_CONFIRMATION_TASK_ID = requested_task[0]
                    return (
                        "OK",
                        f"You have an unfinished higher-priority task paused: '{top_paused[2]}'.\n"
                        f"Do you want to start '{requested_task[2]}' anyway? (yes / no)..."
                    )

            if next_task[0] == requested_task[0]:
                PENDING_CONFIRMATION_TASK_ID = None
                active_task = db.get_active_task(session_id)

                if active_task:
                    db.pause_task(active_task[0],"SWITCH")

                db.resume_or_start_task(requested_task[0]) #type: ignore
                return ("OK", f"Started task: {requested_task[2]}") #type: ignore
            
            # Lower-priority planned task → confirmation needed
            PENDING_CONFIRMATION_TASK_ID = requested_task[0] #type: ignore
            return ("OK",f"'{requested_task[2]}' is planned for today but is not in top priority.\n"
                    f"Higher priority task '{next_task_name}'.\n"
                    f"Do you still want to start this task now? (yes / no)...")
        
        # if task is not today's plan
        PENDING_CONFIRMATION_TASK_ID = None
        return(
            "OK ",f"'{payload}' is not in today’s plan.\n"
        f"Suggested task: '{next_task_name}'.\n"
        "Would you like to start this task now? (yes / no)..."
        )

    if command == "STATUS_TASK":
        if not payload:
            return ("ERROR","Task name required.")
        raw_task_list  = db.get_all_task()
        task_name = payload.strip().lower()
        for task in raw_task_list:
            if task[2].lower() == task_name:
                return ("OK",f"{task[2]}: {task[-1]}")

    if command == "LIST_TODAY":
        active_session = db.get_active_session()
        if not active_session:
            return ("ERROR","No active session.")
        
        session_id = active_session[0]
        session_task = db.get_session_task(session_id)
        session_task_list = []
        session_task_list.append("Today's Plan\n\n")
        if not session_task:
            return ("ERROR","No planned task for today.")
        
        for i,task in enumerate(session_task,start=1):
            session_task_list.append(f"{i}. {task[2]}: {task[-1]}")

        return ("OK","\n".join(session_task_list))

    if command == "LIST_ALL":
        raw_task_list  = db.get_all_task()
        task_list = []
        for i,task in enumerate(raw_task_list,start=1):
            task_list.append(f"{i}. {task[2]}: {task[-1]}")

        return ("OK","\n".join(task_list))
    
    if command == "LIST_BY_DATE":
        if not payload:
            return ("ERROR","Date required.")
        
        FORMATS = (
                # Numeric
                "%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y",
                "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y",
                "%Y.%m.%d", "%d.%m.%Y",

                # Month names
                "%d %B %Y", "%d %b %Y",
                "%B %d %Y", "%b %d %Y",
                "%d %B, %Y", "%B %d, %Y"
        )
        user_date = None
        for fmt in FORMATS:
            try:
                user_date = datetime.strptime(payload.strip(), fmt).strftime("%Y-%m-%d")
                break
            except ValueError:
                continue
            
        if not user_date:
            return ("ERROR","Enter valid date.")
        session = db.get_session_by_date(user_date)
        if not session:
            return ("ERROR","Enter a valid date.")
        
        session_id = session[0]
        session_task = db.get_tasks_by_session(session_id)
        if not session_task:
            return ("ERROR",f"No planned task for '{user_date}'.")
        session_task_list = []
        session_task_list.append(f"Task's of '{user_date}'.\n\n")
        
        for i,task in enumerate(session_task,start=1):
            session_task_list.append(f"{i}. {task[2]}: {task[-1]}")

        return ("OK","\n".join(session_task_list))

    return ("ERROR","Not implemented yet.")