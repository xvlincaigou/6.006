import rubik

from collections import deque

def get_path(visited, current):
    location = current
    path = []
    while visited[location][0] is not None:
        location, move, _ = visited[location]
        path.append(move)
    path.reverse()
    return path

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    start_queue = deque([start])
    end_queue = deque([end])
    start_visited = {start: (None, None, 0)}
    end_visited = {end: (None, None, 0)}

    while True:
        if start_queue.__len__() == 0 and end_queue.__len__() == 0:
            break
        # print('start_queue:', start_queue.__len__(), 'end_queue:', end_queue.__len__())

        if start_queue.__len__() > 0:
            current_start = start_queue.popleft()
            if start_visited[current_start][2] <= 7:
                for move in rubik.quarter_twists:
                    new_position = rubik.perm_apply(move, current_start)
                    if new_position not in start_visited.keys():
                        start_visited[new_position] = (current_start, move, start_visited[current_start][2] + 1)
                        start_queue.append(new_position)

        if end_queue.__len__() > 0:
            current_end = end_queue.popleft()
            if end_visited[current_end][2] <= 7:
                for move in rubik.quarter_twists:
                    new_position = rubik.perm_apply(rubik.perm_inverse(move), current_end)
                    if new_position not in end_visited.keys():
                        end_visited[new_position] = (current_end, move, end_visited[current_end][2] + 1)
                        end_queue.append(new_position)

        if current_start in end_visited:
            start_path = get_path(start_visited, current_start)
            end_path = get_path(end_visited, current_start)
            end_path.reverse()
            return start_path + end_path
        
        if current_end in start_visited:
            start_path = get_path(start_visited, current_end)
            end_path = get_path(end_visited, current_end)
            end_path.reverse()
            return start_path + end_path
    
    return None