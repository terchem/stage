init_seq = [3,2,3] # building block of a sequence n=3

n_max = 4
bloc_base = [22]
for seq in range(3,n_max):
    start = init_seq[0]
    finish = init_seq[-1]
    for index in range (len(init_seq)):
        if init_seq[index] == 2:
            init_seq[index] = 3
        else:
            init_seq[index] = 2
    init_seq.append(finish)
    init_seq.insert(0,start)
    combo = []
    for i in range(6):
        combo.append(init_seq)
        combo.insert(len(combo)-1,bloc_base)
    result = ''.join(str(x) for sublist in combo for x in sublist)
    print(seq)
    print(result)
    print(len(result))
