#!/usr/bin/python3


from all_ipsandnames import pi_data_table
from term_utils import terminal, ping_pi, current_py_processes, mem_check, reboot
import smtplib
import datetime as dt

#pi_data_table format is [(pi name1, pi IP1), (pi name2, pi IP2),... etc]
#print(pi_data_table)

email_results = True

print("####{} check_all_ok.py####".format(dt.datetime.now().strftime('%Y-%m-%d_%H_%M')))

def python_process_check():
    processes = []
    for pi in pi_data_table:
        print("Checking python processes in {}".format(pi))
        reachable = ping_pi(pi[1])
        if not reachable:
            statement = "NA"
        else:
            py_processes = current_py_processes(pi[1])
            if not py_processes:
                statement= "Problem: no python processes running."
            else:
                if "Puzzle" in pi[0] and len(py_processes.split("\n")) >= 3:
                    statement = "Puzzle rfid and video running"
                elif "Observ" in pi[0] and len(py_processes.split("\n")) >= 2:
                    statement ="Observation network photos running"
                elif "Feeder" in pi[0] and len(py_processes.split("\n")) >= 2:
                    statement ="Feeder network photos running"
                elif "Social" in pi[0] and len(py_processes.split("\n")) >= 2:
                    statement ="Social network photos running"
                else:
                    statement ="processes running in {}:{}. Problem with one or more processes.".format(pi[0],py_processes)
        processes += [statement]
    return processes

def memory_check():
    memory = []
    for pi in pi_data_table:
        print("Checking memory in {}".format(pi))
        reachable = ping_pi(pi[1])
        if not reachable:
            print("{} not responding to pings".format(pi[0]))
            info = "NA"
        else:
            info = mem_check(pi[1])
        memory += [info]
    return memory

def server_check():
    server = []
    for pi in pi_data_table:
        print("Checking server mount in {}".format(pi))
        reachable = ping_pi(pi[1])
        if not reachable:
            print("{} not responding to pings".format(pi[0]))
            info = "NA"
        else:
            info = terminal("ssh pi@{} '[ -d \"/home/pi/mnt/Videos_GRETI\" ] && echo \"Server is mounted\" || echo \"Server is NOT mounted\"'".format(pi[1]))
        server += [info]
    return server


processes = python_process_check()
memory = memory_check()
server_status = server_check()
status = ""
for i in range(len(pi_data_table)):
    status += "{} @ {} {}. Memory {}% full. {}.\n".format(pi_data_table[i][0], pi_data_table[i][1], processes[i], memory[i], server_status[i])

print(status)

if email_results:
    user = 'greti.lab.updates@gmail.com'
    password = 'greti2019'
    sent_from = 'greti.lab.updates@gmail.com'
    to = 'mchimento@ab.mpg.de'
    subject = 'global pi report'
    body = status
    email_text = 'From:{}\nTo:{}\nSubject:{}\n{}'.format(sent_from,to,subject,body)

    try:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(user,password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print("Email Sent!")
        
    except:
        print("error in check_ok email")

for i in range(len(pi_data_table)):
    if "NOT" in server_status[i] or "Problem" in processes[i]:
        reboot(pi_data_table[i][1])
        pass

