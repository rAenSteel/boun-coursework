// Ahmet Ensar Usta

import java.util.ArrayList;

public class BFSPathFinder {

    //neighbor exploration order: up, down, left, right
    private static final int[] DR = { -1, 1, 0, 0 };
    private static final int[] DC = { 0, 0, -1, 1 };

    public ArrayList<Position> getFullShortestPath(Position start,
                                                   Position goal,
                                                   MapData mapData) {
        if (start == null || goal == null || mapData == null) {
            return null;
        }

        //edge case for start==goal, return a single-element path instead of null
        if (start.equals(goal)) {
            ArrayList<Position> single = new ArrayList<Position>();
            single.add(start);
            return single;
        }

        int rows = mapData.getRows();
        int cols = mapData.getCols();

        //bound check for start and goal positions
        if (!mapData.isInside(start.getRow(), start.getCol())) {
            return null;
        }
        if (!mapData.isInside(goal.getRow(), goal.getCol())) {
            return null;
        }

        //walls are also invalid moves, so this also checks for walls
        if (!mapData.isValidMove(start.getRow(), start.getCol())) {
            return null;
        }
        if (!mapData.isValidMove(goal.getRow(), goal.getCol())) {
            return null;
        }

        boolean[][] visited = new boolean[rows][cols];
        Position[][] parent = new Position[rows][cols];

        Queue<Position> queue = new Queue<Position>();
        queue.enqueue(start);
        visited[start.getRow()][start.getCol()] = true;

        boolean found = false;

        while (!queue.isEmpty()) {
            Position current = queue.dequeue();

            if (current.equals(goal)) {
                found = true;
                break;
            }

            int r = current.getRow();
            int c = current.getCol();

            // Explore neighbors in the order defined by DR and DC
            for (int i = 0; i < 4; i++) {
                int nr = r + DR[i];
                int nc = c + DC[i];

                if (!mapData.isValidMove(nr, nc)) {
                    continue;
                }
                if (visited[nr][nc]) {
                    continue;
                }

                visited[nr][nc] = true;
                parent[nr][nc] = current;
                queue.enqueue(new Position(nr, nc));
            }
        }

        if (!found) {
            return null;
        }

        //reconstruct path by following parent pointers from goal back to start
        ArrayList<Position> reversePath = new ArrayList<Position>();
        Position cur = goal;
        while (cur != null) {
            reversePath.add(cur);
            if (cur.equals(start)) {
                break;
            }
            cur = parent[cur.getRow()][cur.getCol()];
        }

        // Reverse manually (avoid relying on Collections.reverse, which is not allowed in the spec)
        ArrayList<Position> path = new ArrayList<Position>();
        for (int i = reversePath.size() - 1; i >= 0; i--) {
            path.add(reversePath.get(i));
        }

        return path;
    }
}
