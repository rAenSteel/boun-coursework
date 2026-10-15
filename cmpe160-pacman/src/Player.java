// Ahmet Ensar Usta
public class Player {

    private Position pos;
    private int score;

    private Game.Direction currentDirection;
    private Game.Direction requestedDirection;

    private double visualRow;
    private double visualCol;

    private boolean moving;

    public Player(Position pos) {
        this.pos = pos;
        this.score = 0;
        this.currentDirection = Game.Direction.NONE;
        this.requestedDirection = Game.Direction.NONE;
        this.visualRow = pos.getRow();
        this.visualCol = pos.getCol();
        this.moving = false;
    }

    // -------- Getters --------

    public Position getPos() {
        return pos;
    }

    public int getScore() {
        return score;
    }

    public Game.Direction getCurrentDirection() {
        return currentDirection;
    }

    public Game.Direction getRequestedDirection() {
        return requestedDirection;
    }

    public double getVisualRow() {
        return visualRow;
    }

    public double getVisualCol() {
        return visualCol;
    }

    public boolean isMoving() {
        return moving;
    }

    // -------- Setters --------

    public void setPos(Position pos) {
        this.pos = pos;
    }

    public void setCurrentDirection(Game.Direction d) {
        this.currentDirection = d;
    }

    public void setRequestedDirection(Game.Direction d) {
        this.requestedDirection = d;
    }

    public void setVisualRow(double v) {
        this.visualRow = v;
    }

    public void setVisualCol(double v) {
        this.visualCol = v;
    }

    public void setMoving(boolean moving) {
        this.moving = moving;
    }

    public void addScore(int points) {
        this.score += points;
    }

    public void setScore(int score) {
        this.score = score;
    }
}
