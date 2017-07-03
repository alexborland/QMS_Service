import QMS_Service
import time

QMS = QMS_Service.QMS_Service(
    "servername",# replace with the name or IP that hosts your QMC
    "domain\\username",# replace with domain and username
    "Pa$$w0rD"# replace with password
)
q = QMS.api

# Print a raw list of tasks:
print(q.GetTasks())

# If the API reference asks for an enumerated argument,
# you can pass it as text in a single-element list
print(q.GetServices(["All"]))


# To run a task, we need its GUID, which we can look up by task name
task_name = "Your task name here"
task_id = q.FindTask(name = task_name)['ID']
q.RunTask(task_id)


# An EDX task can be triggered and monitored by getting its execution id
task_name = "EDX_Task_Name"
edx_taskid = q.FindEDX(task_name)[0]['ID']
edx_qdsid = q.FindEDX(task_name)[0]['QDSID']
exec_id = q.TriggerEDXTask(
    qdsID = edx_qdsid,
    taskNameOrID = edx_taskid,
    password = "EDX_TEST"
)['ExecId']
print(exec_id)
time.sleep(5)
while q.GetEDXTaskStatus(edx_qdsid, exec_id)['TaskStatus'] == 'Running':
    time.sleep(5)
    print(q.GetEDXTaskStatus(edx_qdsid, exec_id))