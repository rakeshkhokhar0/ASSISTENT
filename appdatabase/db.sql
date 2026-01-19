INSERT INTO tasks (session_id,task_name,priority,planned_start,planned_end,status)
            values(2, 'Initial Setup', 1, '2024-07-01 09:00:00', '2024-07-01 11:00:00', 'ACTIVE');

INSERT INTO tasks (session_id,task_name,priority,planned_start,planned_end,status)
            values(2, 'Data Migration', 2, '2024-07-01 11:30:00', '2024-07-01 13:30:00', 'PENDING');

INSERT INTO tasks (session_id,task_name,priority,planned_start,planned_end,status)
            values(2, 'Testing', 3, '2024-07-02 13:00:00', '2024-07-02 15:00:00', 'PENDING');

INSERT INTO tasks (session_id,task_name,priority,planned_start,planned_end,status)
            values(2, 'Code Review', 4, '2024-07-02 10:00:00', '2024-07-02 12:00:00', 'PENDING');


UPDATE tasks SET status='PENDING' 
WHERE  session_id=2;
-- INSERT INTO tasks(session_id,task_name,planned_start,planned_end,status)
--             values(?,?,?,?,?)
--             """,(
--                 task['session_id'],
--                 task['task_name'],
--                 task['planned_start'],
--                 task['planned_end'],
--                 task['status']