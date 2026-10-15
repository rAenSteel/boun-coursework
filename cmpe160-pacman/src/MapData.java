// Starter code provided by the CMPE 160 course staff
public class MapData {

    private final char[][] originalMap;
    private char[][] map;
    private final int rows;
    private final int cols;
    private final Position playerStart;
    private final Position pinkyStart;
    private final Position inkyStart;
    private final Position blinkyStart;
    private final Position[] corners;

    public MapData(char[][] map,
                   Position playerStart,
                   Position pinkyStart,
                   Position inkyStart,
                   Position blinkyStart,
                   Position[] corners) {
        this.rows = map.length;
        this.cols = map[0].length;
        this.originalMap = new char[rows][cols];
        for (int i = 0; i < rows; i++) {
            this.originalMap[i] = map[i].clone();
        }
        this.map = deepCopy(originalMap);
        this.playerStart = playerStart;
        this.pinkyStart = pinkyStart;
        this.inkyStart = inkyStart;
        this.blinkyStart = blinkyStart;
        this.corners = corners;
    }

    private char[][] deepCopy(char[][] src) {
        char[][] copy = new char[src.length][];
        for (int i = 0; i < src.length; i++) {
            copy[i] = src[i].clone();
        }
        return copy;
    }


    public void resetMap() {
        this.map = deepCopy(originalMap);
    }

    public void restorePellet(int row, int col) {
        if (isInside(row, col) && map[row][col] == '_') {
            map[row][col] = '.';
        }
    }

    // This method checks if the given row and column are within the bounds of the map.
    public boolean isInside(int row, int col) {
        return row >= 0 && row < rows && col >= 0 && col < cols;
    }

    // This method checks if the tile at the given row and column is a valid move (not a wall).
    public boolean isValidMove(int row, int col) {
        return isInside(row, col) && !(map[row][col] == '#');
    }

    // This method checks if there is a pellet at the given row and column.
    public boolean hasPellet(int row, int col) {
        return isInside(row, col) && map[row][col] == '.';
    }

    // This method removes the pellet at the given row and column by setting it to an empty space ('_').
    public void removePellet(int row, int col) {
        if (hasPellet(row, col)) {
            map[row][col] = '_';
        }
    }

    // This method returns the character representing the tile at the given row and column. If the position is outside the map, it returns a wall character ('#').
    public char getTile(int row, int col) {
        return isInside(row, col) ? map[row][col] : '#';
    }

    // Returns the number of rows in the map.
    public int getRows() {
        return rows;
    }

    // Returns the number of columns in the map.
    public int getCols() {
        return cols;
    }

    // This method returns the corners of the map as an array of Position objects. 
    public Position[] getCorners() {
        return corners;
    }

    // This method returns the starting position of the player (Pacman).
    public Position getPlayerStart() {
        return playerStart;
    }

    // This method returns the starting position of Pinky, the pink ghost.
    public Position getPinkyStart() {
        return pinkyStart;
    }

    // This method returns the starting position of Inky, the cyan ghost.
    public Position getInkyStart() {
        return inkyStart;
    }

    // This method returns the starting position of Blinky, the red ghost.
    public Position getBlinkyStart() {
        return blinkyStart;
    }
}
