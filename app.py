import streamlit as st
from collections import deque
import heapq

# Define the maze, start, and end points
MAZE = [
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0]
]
START, END = (0, 0), (6, 6)

def get_neighbors(pos):
    r, c = pos
    neighbors = []
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(MAZE) and 0 <= nc < len(MAZE[0]) and MAZE[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors

# --- Algorithms ---
def solve_bfs():
    queue = deque([START])
    visited = {START}
    parent = {START: None}
    explored_count = 0
    
    while queue:
        curr = queue.popleft()
        explored_count += 1
        if curr == END:
            break
        for n in get_neighbors(curr):
            if n not in visited:
                visited.add(n)
                parent[n] = curr
                queue.append(n)
                
    return path_from_parent(parent), explored_count

def solve_astar():
    def h(p): return abs(p[0]-END[0]) + abs(p[1]-END[1]) # Manhattan
    open_set = [(0 + h(START), 0, START)]
    parent = {START: None}
    g_score = {START: 0}
    visited = set()
    explored_count = 0
    
    while open_set:
        _, curr_g, curr = heapq.heappop(open_set)
        if curr in visited: continue
        visited.add(curr)
        explored_count += 1
        if curr == END: break
        
        for n in get_neighbors(curr):
            tg = curr_g + 1
            if n not in g_score or tg < g_score[n]:
                g_score[n] = tg
                parent[n] = curr
                heapq.heappush(open_set, (tg + h(n), tg, n))
                
    return path_from_parent(parent), explored_count

def path_from_parent(parent):
    if END not in parent: return []
    path, curr = [], END
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    return path[::-1]

# --- Streamlit Frontend ---
st.title("🤖 Pathfinding Algorithm Test Bench")
st.write("Select an algorithm to view the shortest path and see performance metrics.")

algo_choice = st.selectbox("Choose Algorithm:", ["Breadth-First Search (Blind)", "A* Search (Heuristic)"])

if algo_choice == "Breadth-First Search (Blind)":
    path, explored = solve_bfs()
else:
    path, explored = solve_astar()

path_set = set(path)

# Display Metrics
col1, col2 = st.columns(2)
col1.metric("Path Length (Steps)", len(path) if path else "No Path Found")
col2.metric("Explored States", explored)

# Render Grid Visuals
grid_html = "<div style='display: grid; grid-template-columns: repeat(7, 40px); gap: 4px;'>"
for r in range(len(MAZE)):
    for c in range(len(MAZE[0])):
        if (r, c) == START: color = "#4CAF50; color: white; font-weight: bold;"  # Start Green
        elif (r, c) == END: color = "#F44336; color: white; font-weight: bold;"   # End Red
        elif (r, c) in path_set: color = "#2196F3"                                # Path Blue
        elif MAZE[r][c] == 1: color = "#333333"                                   # Wall Grey
        else: color = "#E0E0E0"                                                   # Path White
        
        label = "S" if (r, c) == START else "G" if (r, c) == END else ""
        grid_html += f"<div style='width:40px; height:40px; background-color:{color}; display:flex; align-items:center; justify-content:center; border-radius:4px;'>{label}</div>"
grid_html += "</div>"

st.markdown(grid_html, unsafe_allow_html=True)
