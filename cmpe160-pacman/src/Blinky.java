// Ahmet Ensar Usta

public class Blinky extends Enemy {

    public Blinky(Position pos) {
        super(pos);
    }

    public Blinky(Position pos, BFSPathFinder finder) {
        super(pos, finder);
    }

    @Override
    public Position selectTarget(Player player, MapData mapData) {
        Position[] corners = mapData.getCorners();
        Position playerPos = player.getPos();

        Position best = corners[0];
        int bestDist = manhattan(playerPos, best);

        for (int i = 1; i < corners.length; i++) {
            int d = manhattan(playerPos, corners[i]);
            if (d < bestDist) {           // strict <: first-found wins on tie
                bestDist = d;
                best = corners[i];
            }
        }
        return best;
    }

    private int manhattan(Position a, Position b) {
        int dr = a.getRow() - b.getRow();
        int dc = a.getCol() - b.getCol();
        if (dr < 0) dr = -dr;
        if (dc < 0) dc = -dc;
        return dr + dc;
    }
}
