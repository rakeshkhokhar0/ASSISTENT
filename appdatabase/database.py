from typing import List,Dict,Optional,Tuple
from datetime import datetime
from appdatabase.database_connection import DatabaseConnection as db


def create_tables()-> None:
    with db() as cursor:

        # user profile table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_profile(
            id INTEGER  PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            assistant_name TEXT NOT NULL,
            purpose TEXT,
            planning_style TEXT,
            start_time TEXT,
            end_time TEXT,
            break_style TEXT,
            created_at TEXT
            )
            """
        )

        # daily session table 
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS day_session(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_date TEXT,
            start_time TEXT,
            end_time TEXT,
            status TEXT
            )
            """
        )

        #task table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            task_name TEXT,
            description TEXT,
            order_by INTEGER DEFAULT 0,
            actual_start TEXT,
            actual_end TEXT,
            pause_start TEXT,
            pause_reason TEXT,
            total_pause INTEGER DEFAULT 0,
            time TEXT,
            status TEXT,
            FOREIGN KEY(session_id) REFERENCES day_session(id)
            )  
            """
        )


def is_user_exist() -> bool:
    with db() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*) FROM user_profile
            """
        )
        exist = cursor.fetchone()[0] > 0

    return exist  


def save_user_profile(profile) -> None:
    with db() as cursor:
        cursor.execute(
            """
            INSERT INTO user_profile (user_name,assistant_name,purpose,planning_style,start_time,end_time,break_style,created_at)
            VALUES(?,?,?,?,?,?,?,?)
            """,(
                profile['user_name'],
                profile['assistant_name'],
                profile['purpose'],
                profile['planning_style'],
                profile['start_time'],
                profile['end_time'],
                profile['break_style'],
                datetime.now().isoformat()
            )
        )


def get_user_profile() -> Optional[Dict]:#user details
    with db() as cursor:
        cursor.execute(
            """
            SELECT * FROM user_profile LIMIT 1
            """
        )
        row = cursor.fetchone()


    if not row:
        return None
    keys = ["id","user_name","assistant_name","purpose","planning_style","start_time","end_time","break_style","created_at"]

    return dict(zip(keys,row))


def get_active_session() ->Optional[Tuple]:#active session data or none*
    with db() as cursor:
        cursor.execute(
            """
            SELECT * FROM day_session WHERE status = 'ACTIVE' LIMIT 1
            """
        )
        row = cursor.fetchone()

    if not row:
        return None
    return row


def start_day_session() -> Optional[int]:#session id
    with db() as cursor:
        cursor.execute(
            """
        INSERT INTO day_session(session_date,start_time,status)
        values(?,?,?)
        """,(datetime.now().date().isoformat(),datetime.now().isoformat(),"ACTIVE")
        )
        session_id = cursor.lastrowid

    return session_id


def end_day_session(session_id) -> None:
    with db() as cursor:
        cursor.execute(
            """
            UPDATE day_session SET end_time = ? ,status = 'CLOSED'
            WHERE id = ?
            """,(datetime.now().isoformat(),session_id)
        )


def insert_task(task) -> None:
    with db() as cursor:
        cursor.execute(
            """
            INSERT INTO tasks(session_id,task_name,description,order,time,status)
            values(?,?,?,?,?)
            """,(
                task['session_id'],
                task['name'],
                task["description"],
                task["order"],
                task['time'],
                task['status']
            )
        )


def get_tasks_by_session(session_id) -> List:
    with db() as cursor:
        cursor.execute(
            """
            SELECT * FROM tasks WHERE session_id = ?
            """,(session_id,)
        )
        return cursor.fetchall()


def get_active_task(session_id) -> Tuple:
    with db() as cursor:
        cursor.execute(
            """
            SELECT * FROM tasks WHERE session_id = ? AND status = 'ACTIVE' LIMIT 1
            """,(session_id,)
        )
        task = cursor.fetchone()

    return task


def update_task_status(task_id,status) -> None:
    with db() as cursor:
        cursor.execute(
            """
            UPDATE tasks SET status = ? WHERE id = ?
            """,(status,task_id)
        )


def update_task_actual_time(task_id) -> None:
    with db() as cursor:
        cursor.execute(
            """
            UPDATE tasks SET actual_start = ?, status = 'ACTIVE' WHERE id = ?
            """,(datetime.now().isoformat(),task_id)
        )


def pause_task(task_id,reason:str) -> None:
    with db() as cursor:
        cursor.execute(
            """
            UPDATE tasks SET pause_start = ?, status = 'PAUSED',pause_reason = ? WHERE id = ?
            """,(datetime.now().isoformat(),reason,task_id)
        )


def get_paused_task_by_priority(session_id) -> Optional[List[tuple]]:
    with db() as cursor:
        cursor.execute(
            """
            SELECT * FROM tasks WHERE status = 'PAUSED' AND pause_reason = 'SWITCH' and session_id = ? AND actual_end IS NULL ORDER BY priority ASC
            """,(session_id,)
        )
        return cursor.fetchall()


def get_break_pause_task(session_id):
    with db() as cursor:
        cursor.execute(
            """
            SELECT * FROM tasks WHERE session_id = ? AND STATUS = "PAUSED" AND pause_reason = "BREAK"
            """,(session_id,)
        )
        return cursor.fetchone()


def resume_task(task_id,pause_time) -> None:
    with db() as cursor:
        cursor.execute(
            """
            UPDATE tasks SET total_pause = total_pause + ?, status = "ACTIVE", pause_start = NULL,pause_reason = NULL WHERE id = ?
            """,(pause_time,task_id)
        )


def resume_or_start_task(task_id) -> None:
    with db() as cursor:
        cursor.execute(
            """
            SELECT status FROM tasks WHERE id = ?
            """,(task_id,)
        )
        row = cursor.fetchone()
        if not row:
            return
        
        status = row[0]

        if status == "PENDING":
            cursor.execute(
                """
                UPDATE tasks SET status = "ACTIVE",actual_start = CURRENT_TIMESTAMP WHERE id = ?
                """,(task_id,)
            )
        elif status =="PAUSED":
            cursor.execute(
                """
                UPDATE tasks SET status = "ACTIVE" , pause_start = NULL, pause_reason = NULL WHERE id = ?
                """,(task_id,)
            )


def complete_task(task_id) -> None:
    with db() as cursor:
        cursor.execute(
            """
            UPDATE tasks SET actual_end = ?, status = 'COMPLETED' WHERE id = ?
            """,(datetime.now().isoformat(),task_id)
        )


def get_unfinished_task(session_id) -> List:
    return get_pending_tasks_by_priority(session_id)


def get_pending_tasks_by_priority(session_id):
    with db() as cursor:
        cursor.execute(
            """
            SELECT * FROM  tasks WHERE  status = 'PENDING' AND session_id = ? ORDER BY priority ASC
            """,(session_id,)
        )
        return cursor.fetchall()


def close_all_active_tasks(session_id) -> None:
    with db() as cursor:
        cursor.execute(
            """
            UPDATE tasks
            SET status = 'PENDING'
            WHERE session_id = ?
            AND status = 'ACTIVE'
            """,
            (session_id,)
        )


def get_last_closed_session() -> Tuple:
    with db() as cursor:
        cursor.execute(
            """
            SELECT * FROM day_session WHERE status = "CLOSED" ORDER BY id DESC LIMIT 1
            """
        )
        return cursor.fetchone()


def skip_task(task_id) -> None:
    with db() as cursor:
        cursor.execute(
            """
            UPDATE tasks SET status = 'SKIPPED' WHERE id = ?
            """,(task_id,)
        ) 


def get_all_task() -> List:
    with db() as cursor:
        cursor.execute(
            """
            SELECT * FROM tasks
            """
        )
        return cursor.fetchall()
    

def get_session_task(session_id) ->list:
    with db() as cursor:
        cursor.execute(
            """
            SELECT * FROM tasks WHERE session_id = ?
            """,(session_id,)
        )
        return cursor.fetchall()
    

def get_session_by_date(date) -> Tuple:
    with db() as cursor:
        cursor.execute(
            """
            SELECT * FROM day_session WHERE session_date = ?
            """,(date,)
        )
        return cursor.fetchone()






