def read_number_pairs(filename):
    """
    Read pairs of numbers from a file.
    
    Args:
    - filename (str): The path to the file to read.
    
    Returns:
    - list of tuple: A list of tuples where each tuple contains a pair of numbers.
    """
    number_pairs = []

    # Open the file for reading
    with open(filename, 'r') as f:
        # Loop through each line in the file
        for line in f:
            # Split the line by spaces to get the two numbers
            num1, num2 = map(int, line.split())
            
            # Append the numbers as a tuple to the list
            number_pairs.append((num1, num2))
    # pair: 
    # pair[i][0] : arrival time
    # pair[i][1] : peak time
    
    return number_pairs

# Calculate average value from an array 

def average(array):
    #limit to 1 decimal place
    # return sum(array)/len(array)
    return round(sum(array)/len(array), 1)

def fcfs(pairs):
    n = len(pairs)
    # print(pairs)
    # sort by arrival time
    processes = sorted(enumerate(pairs), key=lambda x: x[1][0])  # Sort by arrival
    # print(processes)
    Tanswer = [-1] * n
    Treturn = [-1] * n
    Twait = [-1] * n

    current_time = processes[0][1][0]

    for pid, (arrival, burst) in processes:
        if arrival > current_time:
            current_time = arrival
            
        Tanswer[pid] = current_time - arrival
        Twait[pid] = Tanswer[pid]
        Treturn[pid] = Tanswer[pid] + burst
        current_time += burst
        # print('')
        # print(' Tanswer[pid]',  Tanswer[pid])
        # print('Twait[pid]', Twait[pid])
        # print('Treturn[pid]', Treturn[pid])
        # print('')
    return Tanswer, Treturn, Twait


# sjf algorithim without preemp, returning all answer, return ans wait time, return ans turn around time
# small job first

# 1 - sort by arrival time
# 2 - sort by burst time
# 3 - add to queue
# 4 - pop from queue
# 5 - add to answer
# 6 - add to return
# 7 - add to wait
# 8 - repeat 4-7 until queue is empty
# 9 - add all arrived processes to queue
# 10 - repeat 4-9 until all processes are done
def sjf(pairs):
    n = len(pairs)
    # Add keys (pids) to the processes and sort by arrival time then burst time
    processes = sorted(enumerate(pairs), key=lambda x: (x[1][0], x[1][1]))  # Sort by arrival, then by burst

    # Initialize arrays
    Tanswer = [-1] * n
    Treturn = [-1] * n
    Twait = [-1] * n

    # print(processes)

    # Initially, only the process with the earliest arrival time can be considered
    current_time = processes[0][1][0]

    #start queue with first process
    queue = [processes[0]]

    del processes[0]

    while queue:
        # Process with the shortest burst time among those currently available
        # print(queue)
        current_process = min(queue, key=lambda x: x[1][1])
        # print(current_process)
        queue.remove(current_process)
        pid, (arrival, burst) = current_process
        # print(queue)

        # Record times
        Tanswer[pid] = current_time - arrival
        Twait[pid] = Tanswer[pid]
        Treturn[pid] = Tanswer[pid] + burst

        current_time += burst  # Move time forward to end of this process

        # Add all processes that have arrived by now to the queue
        arrived = [p for p in processes if p[1][0] <= current_time]
        queue.extend(arrived)

        # remove all arrived processes from the list of processes
        for p in arrived:
            processes.remove(p)

        # If queue is empty but there are still processes left
        if not queue and processes:
            # print('notQueue')
            queue.append(processes[0])
            current_time = processes[0][1][0]  # Jump forward in time
            del processes[0]

    return Tanswer, Treturn, Twait

def RR(pairs, quantum):
    n = len(pairs)
    # Add pids keys to process mantaining the same order
    # processes = sorted(enumerate(pairs))  
    processes = sorted(enumerate(pairs), key=lambda x: x[1][0])  # Sort by arrival
    # print(processes)
    

    # # Initialize arrays
    Tanswer = [-1] * n
    Treturn = [-1] * n
    Twait = [-1] * n
    auxTwait = [-1] * n
    auxTanswer = [-1] * n
    auxTreturn = [-1] * n
    firstArrival = [-1] * n

    # Initially, only the process with the earliest arrival time can be considered
    current_time = processes[0][1][0]

    queue = [processes[0]]
    del processes[0]

    while queue:
        # Process with the shortest burst time among those currently available
        current_process = queue[0]
        pid, (arrival, burst) = current_process

        if arrival > current_time:
            current_time = arrival

        if Tanswer[pid] == -1:
            Tanswer[pid] = current_time - arrival
            auxTanswer[pid] = Tanswer[pid]
            firstArrival[pid] = arrival
            # print('Tanswer[pid]', Tanswer[pid])

        if Twait[pid] == -1:
            Twait[pid] = Tanswer[pid]
            auxTreturn[pid] = current_time
        else:
            Twait[pid] += current_time - auxTreturn[pid]
            # print('Twait[pid]', pid, Twait[pid])
        


        if (burst <= quantum) and (burst >= 0) :
            current_time += burst
            # set return time IJ
            # Treturn[pid] = (current_time) 
            auxTreturn[pid] = current_time
            Treturn[pid] = ( current_time - firstArrival[pid]) 

            # if pid == n-1:
            # print('tamo naeue', Treturn[pid], burst)  
            #     Twait[pid] += current_time - auxTreturn[pid]
            # Add all processes that have arrived by now to the queue
            queue.remove(current_process)
            arrived = [p for p in processes if p[1][0] <= current_time]
            queue.extend(arrived)

             # remove all arrived processes from the list of processes
            for p in arrived:
                processes.remove(p)
        else:
            current_time += quantum
            auxTanswer[pid] = current_time
            # set return time
            auxTreturn[pid] = current_time
            queue.remove(current_process)

            # Add all processes that have arrived by now to the queue
            arrived = [p for p in processes if p[1][0] <= current_time]
            queue.extend(arrived)
            queue.append((pid, (current_time, burst - quantum)))

            # remove all arrived processes from the list of processes
            for p in arrived:
                processes.remove(p)
        
        
        # If queue is empty but there are still processes left
        if not queue and processes:
            queue.append(processes[0])
            current_time = processes[0][1][0]
            # print('notQueue', Twait, n, pid)
            del processes[0]
        
    # print('Tanswer', Tanswer)
    # print('Twait', Twait)
    # print('Treturn', Treturn)
        
    return Tanswer, Treturn, Twait

# pairs = read_number_pairs('testes/teste1.txt')
# pairs = read_number_pairs('testes/teste2.txt')
# pairs = read_number_pairs('testes/teste3.txt')
# pairs = read_number_pairs('testes/teste4.txt')
# pairs = read_number_pairs('testes/teste5.txt')
# pairs = read_number_pairs('testes/teste6.txt')
# pairs = read_number_pairs('testes/teste7.txt')
# pairs = read_number_pairs('testes/teste8.txt')
pairs = read_number_pairs('testes/teste9.txt')
# pairs = read_number_pairs('testes/teste10.txt')


# print(pairs)
Tanswer, Treturn, Twait = fcfs(pairs)
avgTanswer = average(Tanswer)
avgTreturn = average(Treturn)
avgTwait = average(Twait)
print("FCFS: ", avgTreturn, avgTanswer, avgTwait)
# print("FCFS: ", "Treturn: ", avgTreturn, "Tanswer: ", avgTanswer, "Twait: ", avgTwait)

Tanswer, Treturn, Twait = sjf(pairs)
avgTanswer = average(Tanswer)
avgTreturn = average(Treturn)
avgTwait = average(Twait)
print("SJF: ", avgTreturn, avgTanswer, avgTwait)
# print("SJF: ", "Treturn: ", avgTreturn, "Tanswer: ", avgTanswer, "Twait: ", avgTwait)

Tanswer, Treturn, Twait = RR(pairs, 2)
avgTanswer = average(Tanswer)
avgTreturn = average(Treturn)
avgTwait = average(Twait)
print("RR: ", avgTreturn, avgTanswer, avgTwait)
# print("RR: ", "Treturn: ", avgTreturn, "Tanswer: ", avgTanswer, "Twait: ", avgTwait)
    


