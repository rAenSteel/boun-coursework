// Starter code provided by the CMPE 160 course staff
public class Position {
    private final int row;
    private final int col;

    public Position(int row, int col) {
        this.row = row;
        this.col = col;
    }

    public int getRow() {
        return row;
    }
    public int getCol() {
        return col;
    }

    // This method checks if the position is equal to another object. It returns true if the other object is a Position with the same row and column, and false otherwise.
    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }

        Position other = (Position) o;
        return row == other.row && col == other.col;
    }
}

