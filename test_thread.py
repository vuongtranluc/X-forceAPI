import threading
import time
import random
random.seed(2)

data = [
    {
        "a": 1,
        "b": -1
    }, {
        "a": 2,
        "b": -2
    }, {
        "a": 3,
        "b": -3
    }, {
        "a": 4,
        "b": -4
    }, {
        "a": 5,
        "b": -5
    }, {
        "a": 6,
        "b": -6
    }
]
timesleep = [1, 2, 3, 4, 5, 2]

def worker(row, i):
    time.sleep(timesleep[i]) 
    row["a"] = row["b"] + 1


def testThread():
    tt = time.time()
    g = []
    i = 0
    for row in data:
        t = threading.Thread(target=worker, args=(row,i,))
        i = i+1
        t.start()
        g.append(t)
        # t.join()
        # print(t)
    # print(data, "//")
    while (any([x.is_alive() for x in g])):
        pass
    # time.sleep(3)
    return [time.time() - tt, data]