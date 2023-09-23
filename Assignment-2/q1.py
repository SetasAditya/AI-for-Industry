def first_come_first_serve(processes):
    num = len(processes)
    tot_turnaroundtime = 0
    tot_waitingtime = 0

    current_time = 0
    process_order = []

    for i in range(num):
        ready_processes = [p for p in processes if p[1] <= current_time]

        if not ready_processes:
            current_time += 1
            continue

        current_process = min(ready_processes, key=lambda x: x[1])
        process_order.append(current_process[0])

        process_id, arrival_time, burst_time, priority = current_process
        s_time = max(current_time, arrival_time)
        c_time = s_time + burst_time
        ta_time = c_time - arrival_time
        wait_time = ta_time - burst_time

        tot_turnaroundtime += ta_time
        tot_waitingtime += wait_time

        current_time = c_time
        processes.remove(current_process)

    avg_waiting_time = tot_waitingtime / num
    avg_turnaround_time = tot_turnaroundtime / num

    return process_order, avg_waiting_time, avg_turnaround_time

def shortest_job_first(processes):
    num = len(processes)
    tot_turnaroundtime = 0
    tot_waitingtime = 0
    # Sort processes based on the 3rd element (burst time)
    processes = sorted(processes, key=lambda x: x[2])
    current_time = 0
    process_order = []

    while processes:
        ready_processes = [p for p in processes if p[1] <= current_time]

        if not ready_processes:
            current_time += 1
            continue

        shortest_process = min(ready_processes, key=lambda x: x[2])
        process_order.append(shortest_process[0])

        process_id, arrival_time, burst_time, priority = shortest_process
        s_time = current_time
        c_time = s_time + burst_time
        ta_time = c_time - arrival_time
        wait_time = ta_time - burst_time

        tot_turnaroundtime += ta_time
        tot_waitingtime += wait_time

        current_time = c_time
        processes.remove(shortest_process)

    avg_waiting_time = tot_waitingtime / num
    avg_turnaround_time = tot_turnaroundtime / num

    return process_order, avg_waiting_time, avg_turnaround_time

def priority_scheduling(processes):
    num = len(processes)
    tot_turnaroundtime = 0
    tot_waitingtime = 0

    current_time = 0
    process_order = []

    while processes:
        ready_processes = [p for p in processes if p[1] <= current_time]

        if not ready_processes:
            current_time += 1
            continue

        highest_priority_process = min(ready_processes, key=lambda x: x[3])
        process_order.append(highest_priority_process[0])

        process_id, arrival_time, burst_time, priority = highest_priority_process
        s_time = current_time
        c_time = s_time + burst_time
        ta_time = c_time - arrival_time
        wait_time = ta_time - burst_time

        tot_turnaroundtime += ta_time
        tot_waitingtime += wait_time

        current_time = c_time
        processes.remove(highest_priority_process)

    avg_waiting_time = tot_waitingtime / num
    avg_turnaround_time = tot_turnaroundtime / num

    return process_order, avg_waiting_time, avg_turnaround_time

def round_robin(processes, time_quantum):
    num = len(processes)

    timer, max_process_index = 0, 0
    avg_waiting_time, avg_turnaround_time = 0, 0

    def queue_updation(queue, timer, arrival, n, max_process_index):
        zero_index = -1
        for i in range(n):
            if queue[i] == 0:
                zero_index = i
                break

        if zero_index == -1:
            return
        queue[zero_index] = max_process_index + 1

    def check_new_arrival(timer, arrival, n, max_process_index, queue):
        if timer <= arrival[n-1]:
            new_arrival = False
            for j in range(max_process_index + 1, n):
                if arrival[j] <= timer:
                    if max_process_index < j:
                        max_process_index = j
                        new_arrival = True

            if new_arrival:
                queue_updation(queue, timer, arrival, n, max_process_index)

    def queue_maintenance(queue, n):
        for i in range(n-1):
            if queue[i+1] != 0:
                queue[i], queue[i+1] = queue[i+1], queue[i]

    tq = time_quantum
    n = num
    arrival = [0] * n
    burst = [0] * n
    wait = [0] * n
    turn = [0] * n
    queue = [0] * n
    temp_burst = [0] * n
    complete = [False] * n
    process_order = []

    for i in range(n):
        arrival[i] = processes[i][1]

    for i in range(n):
        burst[i] = processes[i][2]
        temp_burst[i] = burst[i]

    for i in range(n):
        complete[i] = False
        queue[i] = 0

    while timer < arrival[0]:
        timer += 1
    queue[0] = 1

    while True:
        flag = True
        for i in range(n):
            if temp_burst[i] != 0:
                flag = False
                break

        if flag:
            break

        for i in range(n and queue[i] != 0):
            counter = 0
            while counter < tq and temp_burst[queue[0] - 1] > 0:
                temp_burst[queue[0] - 1] -= 1
                timer += 1
                counter += 1
                check_new_arrival(timer, arrival, n, max_process_index, queue)
                process_order.append(f"P{queue[0]}")

            if temp_burst[queue[0] - 1] == 0 and not complete[queue[0] - 1]:
                turn[queue[0] - 1] = timer
                complete[queue[0] - 1] = True
                process_order.append(f"P{queue[0]}")

            idle = True
            if queue[n - 1] == 0:
                for k in range(n):
                    if queue[k] != 0:
                        if not complete[queue[k] - 1]:
                            idle = False
            else:
                idle = False

            if idle:
                timer += 1
                check_new_arrival(timer, arrival, n, max_process_index, queue)

            queue_maintenance(queue, n)

    for i in range(n):
        turn[i] = turn[i] - arrival[i]
        wait[i] = turn[i] - burst[i]

    for i in range(n):
        avg_waiting_time += wait[i]
        avg_turnaround_time += turn[i]

    avg_waiting_time = avg_waiting_time/n
    avg_turnaround_time = avg_turnaround_time/n
    
    return process_order, avg_waiting_time, avg_turnaround_time

if __name__ == "__main__":
    # Input processes: [["P1", "00:00", 30, 3], ["P2", "00:10", 20, 1], ["P3", "00:15", 40, 4], ["P4", "00:20", 15, 2]]
    processes = [["P1", 0, 24, 3], ["P2", 4, 3, 1], ["P3",5, 3, 4], ["P4",6, 12, 2]]

    algorithms = ["FCFS", "SJF", "Priority", "Round Robin"]

    results = {}  # Store results for each algorithm

    for algorithm in algorithms:
        if algorithm == "FCFS":
            process_order, avg_waiting_time, avg_turnaround_time = first_come_first_serve(processes.copy())
        elif algorithm == "SJF":
            process_order, avg_waiting_time, avg_turnaround_time = shortest_job_first(processes.copy())
        elif algorithm == "Priority":
            process_order, avg_waiting_time, avg_turnaround_time = priority_scheduling(processes.copy())
        elif algorithm == "Round Robin":
            time_quantum = 4  # Replace with your desired time quantum
            process_order, avg_waiting_time, avg_turnaround_time = round_robin(processes.copy(), time_quantum)

        results[algorithm] = (avg_waiting_time, avg_turnaround_time, process_order)

    # Print results for all algorithms
    for algorithm, (avg_waiting_time, avg_turnaround_time, process_order) in results.items():
        print(f"{algorithm}:")
        print(f"Process Order: {' -> '.join(process_order)}")
        print(f"Average Waiting Time: {avg_waiting_time}")
        print(f"Average Turnaround Time: {avg_turnaround_time}")
        print()

    # Select the best algorithm based on average waiting and turnaround time
    best_algorithm = min(results, key=lambda k: (results[k][0], results[k][1]))
    print(f"The best algorithm is: {best_algorithm}")