# from appdatabase.database_connection import DatabseConnection as db

# with db() as cursor:
#     cursor.execute(
#         """
#         INSERT INTO tasks (session_id,task_name,priority,planned_start,planned_end,status)
#             values(1, 'Initial Setup', 1, '2024-07-01 09:00:00', '2024-07-01 11:00:00', 'PENDING')
#         """
#     )
#     cursor.execute(
#         """
#         INSERT INTO tasks (session_id,task_name,priority,planned_start,planned_end,status)
#         values(1, 'Data Migration', 2, '2024-07-01 11:30:00', '2024-07-01 13:30:00', 'PENDING')
#         """
#     )
#     cursor.execute(
#         """
#         INSERT INTO tasks (session_id,task_name,priority,planned_start,planned_end,status)
#         values(1, 'Testing', 3, '2024-07-02 13:00:00', '2024-07-02 15:00:00', 'PENDING')
#         """
#     )
#     cursor.execute(
#         """
#         INSERT INTO tasks (session_id,task_name,priority,planned_start,planned_end,status)
#         values(1, 'Code Review', 4, '2024-07-02 10:00:00', '2024-07-02 12:00:00', 'PENDING')
#         """
#     )
    # cursor.execute(
    #     """
    #     UPDATE tasks SET status='PENDING' 
    #     WHERE  session_id=2;
    #     """
    # )

# print("inserted successfully")


# if command == "START":
#     global PENDING_CONFIRMATION_TASK_ID

#     if not payload:
#         return ("ERROR", "Task name is required.")

#     active_session = db.get_active_session()
#     if not active_session:
#         return ("ERROR", "No active day. Start the day first.")

#     session_id = active_session[0]
#     requested_name = payload.strip().lower()

#     # 1) If there is a PAUSED task with this name → resume immediately
#     paused = db.get_paused_task_by_priority(session_id)
#     if paused and paused[2].lower() == requested_name:
#         PENDING_CONFIRMATION_TASK_ID = None
#         db.resume_or_start_task(paused[0])
#         return ("OK", f"Resumed task: {paused[2]}")

#     # 2) Check today’s tasks
#     today_tasks = db.get_tasks_by_session(session_id)
#     requested_task = next((t for t in today_tasks if t[2].lower() == requested_name), None)

#     pending = db.get_pending_tasks_by_priority(session_id)
#     if not pending:
#         return ("ERROR", "No pending tasks available today.")

#     top_task = pending[0]

#     # 3) Planned task
#     if requested_task:
#         if requested_task[0] == top_task[0]:
#             PENDING_CONFIRMATION_TASK_ID = None
#             active = db.get_active_task(session_id)
#             if active:
#                 db.pause_task(active[0])
#             db.resume_or_start_task(requested_task[0])
#             return ("OK", f"Started task: {requested_task[2]}")
#         else:
#             PENDING_CONFIRMATION_TASK_ID = requested_task[0]
#             return (
#                 "OK",
#                 f"'{requested_task[2]}' is planned but not top priority.\n"
#                 f"Higher-priority task: '{top_task[2]}'.\n"
#                 "Start this task anyway? (yes / no)"
#             )

#     # 4) Out of plan
#     PENDING_CONFIRMATION_TASK_ID = None
#     return (
#         "OK",
#         f"'{payload}' is not in today’s plan.\n"
#         f"Suggested task: '{top_task[2]}'.\n"
#         "Start anyway? (yes / no)"
#     )


from planner import generate_day_plan
from pprint import pprint
plan = generate_day_plan({
    "goal": "Learn Python decorators",
    "time_hours": 3,
    "intensity": "normal",
    "unfinished_tasks": []
})
pprint(plan,width=100)

