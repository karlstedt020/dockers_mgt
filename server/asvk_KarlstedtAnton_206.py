total_sum = 0
timer = 0
ans = 0
current_sum = 0

#the graph is supposed to be connected

def dfs(vertex, parent, weights, used, tin, fup, net, cutpoints):
    global total_sum
    global timer
    total_sum += weights[vertex]
    used[vertex] = True
    tin[vertex] = timer
    fup[vertex] = timer
    timer += 1
    children = 0
    for to in net[vertex]:
        if to == parent:
            continue
        if used[to]:
            fup[vertex] = min(fup[vertex], tin[to])
        else:
            dfs(to, vertex, weights, used, tin, fup, net, cutpoints)
            fup[vertex] = min(fup[vertex], fup[to])
            if fup[to] >= tin[vertex] and parent is not None:
                cutpoints.append(vertex)
            children += 1
    if parent == None and children > 1:
        cutpoints.append(vertex)

def getAnswer(vertex, parent, weights, used, net):
    global ans
    global current_sum
    if parent is not None:
        current_sum += weights[vertex]
    used[vertex] = True
    for to in net[vertex]:
        if used[to] or to == parent:
            continue
        getAnswer(to, vertex, weights, used, net)
        if parent is None:
            ans += current_sum**2
            current_sum = 0

#process function receives data from file created by server and returnes the answer
def process():
    import json
    global total_sum
    global timer
    global current_sum
    tin = {}
    fup = {}
    used = {}
    net = {}
    vertex_list = []
    weights = {}
    cutpoints = []
    best_ans = -1
    ans_list = []
    try:
        cfg = json.load(open("input.json"))
        weights = cfg['vertexes']
        vertex_list = cfg['vertexes'].keys()
        for vert, weight in cfg['vertexes'].items():
            used[vert] = False
            net[vert] = []
        for edge in cfg['edges']:
            net[edge[0]].append(edge[1])
            net[edge[1]].append(edge[0])
        #finished processing data from file
        #now we will find all cutpoints in order to make the calculations faster - answer for not-cutpoint vertexes will be calculated for O(1), for cutpoints for O(n)
        #cutpoints search algorithm taken from emax algo
        for v in vertex_list:
            if not used[v]:
                dfs(v, None, weights, used, tin, fup, net, cutpoints)
        cutpoints = set(cutpoints)
        other = [x for x in vertex_list if x not in cutpoints]
        for v in other:
            current_sum = (total_sum - weights[v])**2 + weights[v]
            if best_ans == -1:
                best_ans = current_sum
                ans_list.append(v)
            elif best_ans == current_sum:
                ans_list.append(v)
            elif best_ans > current_sum:
                ans_list = []
                best_ans = current_sum
                ans_list.append(v)
        #processed not-cutpoints nodes, now it's cutpoint's time
        #getAnswer fuction gets the answer if the vertex with parent == None is removed
        for v in cutpoints:
            used = {}
            current_sum = 0
            global ans
            ans = 0
            for vertex in vertex_list:
                used[vertex] = False
            getAnswer(v, None, weights, used, net)
            ans += weights[v]
            if best_ans == -1:
                best_ans = current_sum
                ans_list.append(v)
            elif best_ans == ans:
                ans_list.append(v)
            elif best_ans > ans:
                ans_list = []
                best_ans = ans
                ans_list.append(v)
        timer = 0
        total_sum = 0
        return ans_list
    except KeyError:
        print("Invalid format of the input, check the lists and maps names in the input format")
        return {"answer": "invalid input"}
    except IndexError:
        print("Invalid format of the input, check the edges format")
        return {"answer": "invalid input"}
    except TypeError:
        print("Invalid format of the input, check the amount of people for each tower")
        return {"answer": "invalid input"}