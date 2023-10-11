def read_file(file):
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
            first_line = int(lines[0])
            remaining_lines = [int(line) for line in lines[1:]]
            return first_line, remaining_lines
    except FileNotFoundError:
        return None, []
    

# FIFO Scheduling Algorithm
def fifo(frameSize, list):
    # initialize page fault counter
    pageFault = 0
    frame = []

    for i in range(len(list)):
        if len(frame) < frameSize:
            if list[i] not in frame:
                frame.append(list[i])
                pageFault += 1
        else:
            if list[i] not in frame:
                frame.pop(0)
                frame.append(list[i])
                pageFault += 1
    return pageFault


# OTM OTIMUM Scheduling Algorithm
def otm(frameSize, list):
    pageFault = 0
    frame = []
    auxList = {}

    # the keys are the numbers in the list and the values are all index of the number in the list
    for i in range(len(list)):
        if list[i] not in auxList:
            auxList[list[i]] = [i]
        else:
            auxList[list[i]].append(i)

    for i in range(len(list)):
        # Removing atual list element index from auxList
        auxList[list[i]].pop(0)
        #if the list is not in the frame, add it to the frame
        if list[i] not in frame:
            #if list not filled, fill it. 
            #else find the number that has the largest index in the list to change it.
            if len(frame) < frameSize:
                    frame.append(list[i])
                    pageFault += 1
            else:
                # if list[i] not in frame:
                    # find the number that has the largest index in the list
                farestFrameKey = -1
                for j in range(len(frame)):
                    if auxList[frame[j]]:
                        if (auxList[frame[j]][0] > farestFrameKey):
                            farestFrameKey = j
                    else:
                        #get first item who has no index in the list
                        farestFrameKey = j
                        break
                frame[farestFrameKey] = list[i]
                pageFault += 1

    return pageFault

#LRU Least Recently Used 

def lru (frameSize, list):
    pageFault = 0
    frame = []
    auxList = {}
    
    for i in range(len(list)):
        auxList[list[i]] = i # save the latest index of the number in the list
        if list[i] not in frame:
            if len(frame) < frameSize:
                frame.append(list[i])
                pageFault += 1
            else:
                farestFrameKey = i
                smallerIndex = i
                for j in range(len(frame)):
                    if auxList[frame[j]]:
                        if (auxList[frame[j]] < smallerIndex):
                            smallerIndex = auxList[frame[j]]
                            farestFrameKey = j
                    else:
                        farestFrameKey = j
                        break
                frame[farestFrameKey] = list[i]
                pageFault += 1
    return pageFault

   
frameSize, list = read_file('input.txt')
print('FIFO ', fifo(frameSize, list))
print('OTM: ', otm(frameSize, list))
print('LRU: ', lru(frameSize, list))

# for i in range(0, 10):
#     frameSize, list = read_file('testes/teste' + str(i) + '.txt')
#     print('------------', i, '-------------')
#     print('FIFO ', fifo(frameSize, list))
#     print('OTM: ', otm(frameSize, list))
#     print('LRU: ', lru(frameSize, list))

        

   