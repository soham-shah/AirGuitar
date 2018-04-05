
plucked = [False for _ in range(5)]

loop = True
while loop:
    # time.sleep(0.1) # 0.5
    ch = ""
    try:
        ch = raw_input("Press q, w, e, r to plunk a stering (p to quit): ")
        print(ch)
    except:
        print("passed")
        pass
    if ch == 'q':
        print("got here")
        plucked[0] = True
    if ch == 'w':
        plucked[1] = True
    if ch == 'e':
        plucked[2] = True
    if ch == 'r':
        plucked[3] = True
    if ch == 'p':
        # Exit and write to file.
        loop = False
    else:
        pass