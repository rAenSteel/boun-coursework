// Ahmet Ensar Usta



import java.util.ArrayList;

public abstract class Enemy {

    protected Position pos;
    protected Game.Direction direction;
    protected BFSPathFinder finder;

    protected double visualRow;
    protected double visualCol;

    protected Enemy(Position pos) {
        this.pos = pos;
        this.direction = Game.Direction.NONE;
        this.visualRow = pos.getRow();
        this.visualCol = pos.getCol();
    }

    protected Enemy(Position pos, BFSPathFinder finder) {
        this.pos = pos;
        this.finder = finder;
        this.direction = Game.Direction.NONE;
        this.visualRow = pos.getRow();
        this.visualCol = pos.getCol();
    }

    //--------------------getters------------------------------

    public double getVisualRow() {
        return visualRow;
    }

    public double getVisualCol() {
        return visualCol;
    }

    public Position getPos() {
        return pos;
    }

    public Game.Direction getDirection() {
        return direction;
    }

    //--------setters-------------------------------------------------------------------------

    public void setVisualRow(double v) {
        this.visualRow = v;
    }

    public void setVisualCol(double v) {
        this.visualCol = v;
    }

    public void setPos(Position p) {
        this.pos = p;
    }

    public void setDirection(Game.Direction d) {
        this.direction = d;
    }

    //---------------movement-----------------------------
    public void move(Player player, MapData mapData) {
        Position target = selectTarget(player, mapData);
        if (target == null) {
            return;
        }
        ArrayList<Position> path = finder.getFullShortestPath(this.pos, target, mapData);
        if (path == null || path.size() < 2) {
            return;
        }
        Position next = path.get(1);
        Game.Direction newDir = getDirectionFromPositions(this.pos, next);
        setDirection(newDir);
        setPos(next);
    }

    //returns the direction from "from" to "to", or NONE if they are not adjacent
    protected Game.Direction getDirectionFromPositions(Position from, Position to) {
        int dRow = to.getRow() - from.getRow();
        int dCol = to.getCol() - from.getCol();
        if (dRow == -1 && dCol == 0) return Game.Direction.UP;
        if (dRow == 1  && dCol == 0) return Game.Direction.DOWN;
        if (dRow == 0  && dCol == -1) return Game.Direction.LEFT;
        if (dRow == 0  && dCol == 1)  return Game.Direction.RIGHT;
        return Game.Direction.NONE;
    }

    //------------------target selection------------------------------
    public abstract Position selectTarget(Player player, MapData mapData);
}
