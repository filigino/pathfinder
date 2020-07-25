# Pathfinding Visualizer
Visualizer for popular searching algorithms

## Usage

- Click anywhere to place the start node
- Click anywhere to place the end node
- Click anywhere to place barrier nodes
- Right click on a node to remove it

After the start and end nodes have been placed:
- Press D - Depth-first search (recursive)
- Press B - Breadth-first search
- Press A - A* search

**Notes**:
- Depth-first search crashes if the end node is too far away from the start node (too many recursive calls)
- A* search uses Manhattan distance for heuristic function
- To break f score ties, A* search uses the node that was arrived at first

## Demo

<img src="./README/GUI_demo.gif" width="35%" />
GUI
<br/>
<br/>

<img src="./README/DFS.gif" width="35%" />
Depth-first search
<br/>
<br/>

<img src="./README/BFS.gif" width="35%" />
Breadth-first search
<br/>
<br/>

<img src="./README/A-star.gif" width="35%" />
A* search

## Next Steps

- Add instructions
- Prevent depth-first search from crashing
- Add Dijkstra's algorithm
