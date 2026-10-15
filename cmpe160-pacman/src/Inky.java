// Ahmet Ensar Usta

import java.util.ArrayList;

public class Inky extends Enemy {

    public Inky(Position pos) {
        super(pos);
    }

    public Inky(Position pos, BFSPathFinder finder) {
        super(pos, finder);
    }

    @Override
    public Position selectTarget(Player player, MapData mapData) {
        if (Math.random() < 0.6) {
            return player.getPos();
        }
        // 40% case random valid neighbor
        ArrayList<Position> validNeighbors = new ArrayList<Position>();
        int r = this.pos.getRow();
        int c = this.pos.getCol();
        if (mapData.isValidMove(r - 1, c)) validNeighbors.add(new Position(r - 1, c));
        if (mapData.isValidMove(r + 1, c)) validNeighbors.add(new Position(r + 1, c));
        if (mapData.isValidMove(r, c - 1)) validNeighbors.add(new Position(r, c - 1));
        if (mapData.isValidMove(r, c + 1)) validNeighbors.add(new Position(r, c + 1));

        if (validNeighbors.isEmpty()) {
            return player.getPos();   // fallback
        }
        int idx = (int) (Math.random() * validNeighbors.size());
        return validNeighbors.get(idx);
    }
}
