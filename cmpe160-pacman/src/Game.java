// Ahmet Ensar Usta

public class Game {

    public enum GameState {
        START_SCREEN,
        READY,
        PLAYING,
        PAUSED,
        WON,
        LOST,
    }

    public enum Direction {
        UP(-1, 0), DOWN(1, 0), LEFT(0, -1), RIGHT(0, 1), NONE(0, 0);

        private final int dRow;
        private final int dCol;

        Direction(int dRow, int dCol) {
            this.dRow = dRow;
            this.dCol = dCol;
        }

        public int getDRow() { return dRow; }
        public int getDCol() { return dCol; }
    }

    //--------tunable constants----------------------------
    private static final double PACMAN_VISUAL_SPEED = 0.10;
    private static final double ENEMY_VISUAL_SPEED  = 0.067;
    private static final double COLLISION_THRESHOLD = 0.5;
    private static final double GRID_ALIGN_EPSILON  = 1e-3;
    private static final long   READY_DURATION_MS   = 1000L;

    //-----------------------------fields----------------------------------------------
    private final Player player;
    private final Enemy[] enemies;
    private final MapData mapData;
    private GameState gameState;

    private final int totalPellets;
    private int eatenPellets;

    private long readyStartTime;

    public Game(Player player, Enemy[] enemies, MapData mapData) {
        this.player = player;
        this.enemies = enemies;
        this.mapData = mapData;
        this.gameState = GameState.START_SCREEN;
        this.totalPellets = countPellets();
        this.eatenPellets = 0;
    }

    //getters-----------------------------------------------------------------------------

    public Player getPlayer() {
        return player;
    }

    public Enemy[] getEnemies() {
        return enemies;
    }

    public GameState getGameState() {
        return gameState;
    }

    public MapData getMapData() {
        return mapData;
    }

    public int getTotalPellets() {
        return totalPellets;
    }

    public int getEatenPellets() {
        return eatenPellets;
    }

    //-----------------------------state transitions----------------------------------------------

    public void setGameState(GameState s) {
        this.gameState = s;
    }

    //space is pressed on start screen to start ready state, which then times out into playing.
    public void startReady() {
        this.gameState = GameState.READY;
        this.readyStartTime = System.currentTimeMillis();
    }

    // Called every frame to check if we should transition from READY to PLAYING.
    public void checkReadyTimeout() {
        if (gameState == GameState.READY) {
            if (System.currentTimeMillis() - readyStartTime >= READY_DURATION_MS) {
                gameState = GameState.PLAYING;
            }
        }
    }

    // P is pressed during PLAYING or PAUSED to toggle between them.
    public void togglePause() {
        if (gameState == GameState.PLAYING) {
            gameState = GameState.PAUSED;
        } else if (gameState == GameState.PAUSED) {
            gameState = GameState.PLAYING;
        }
    }

    //-----------------------------main update loop----------------------------------------------

    public void update() {
        if (gameState != GameState.PLAYING) {
            return;
        }
        updatePlayer();
        updateEnemies();
        checkCollision();
        checkWin();
    }

    //--------------player update--------------------------

    private void updatePlayer() {
        //logical step decisions are made only when grid aligned
        if (isPlayerGridAligned()) {
            //try to apply requested direction at the intersection
            if (canMove(player.getPos(), player.getRequestedDirection())) {
                player.setCurrentDirection(player.getRequestedDirection());
            }
            //try to step in the current direction
            if (canMove(player.getPos(), player.getCurrentDirection())) {
                Position np = stepFrom(player.getPos(), player.getCurrentDirection());
                player.setPos(np);
                player.setMoving(true);

                //pellet collection check first then add score then remove
                if (mapData.hasPellet(np.getRow(), np.getCol())) {
                    player.addScore(10);
                    mapData.removePellet(np.getRow(), np.getCol());
                    eatenPellets++;
                }
            } else {
                //wall ahead in current direction stpo movin
                player.setMoving(false);
            }
        }
        //visual approach toward logical position
        approachVisualPlayer(PACMAN_VISUAL_SPEED);
    }

    // ----enemy update ---------------

    private void updateEnemies() {
        for (Enemy enemy : enemies) {
            if (isEnemyGridAligned(enemy)) {
                enemy.move(player, mapData);
            }
            approachVisualEnemy(enemy, ENEMY_VISUAL_SPEED);
        }
    }

    //-------------------alignemnt and movement helpers-----------------------

    private boolean isPlayerGridAligned() {
        return Math.abs(player.getVisualRow() - player.getPos().getRow()) < GRID_ALIGN_EPSILON
            && Math.abs(player.getVisualCol() - player.getPos().getCol()) < GRID_ALIGN_EPSILON;
    }

    private boolean isEnemyGridAligned(Enemy e) {
        return Math.abs(e.getVisualRow() - e.getPos().getRow()) < GRID_ALIGN_EPSILON
            && Math.abs(e.getVisualCol() - e.getPos().getCol()) < GRID_ALIGN_EPSILON;
    }

    private boolean canMove(Position p, Direction d) {
        if (d == Direction.NONE) return false;
        int nr = p.getRow() + d.getDRow();
        int nc = p.getCol() + d.getDCol();
        return mapData.isValidMove(nr, nc);
    }

    private Position stepFrom(Position p, Direction d) {
        return new Position(p.getRow() + d.getDRow(), p.getCol() + d.getDCol());
    }

    private void approachVisualPlayer(double speed) {
        double dr = player.getPos().getRow() - player.getVisualRow();
        double dc = player.getPos().getCol() - player.getVisualCol();
        if (Math.abs(dr) <= speed) {
            player.setVisualRow(player.getPos().getRow());
        } else {
            player.setVisualRow(player.getVisualRow() + Math.signum(dr) * speed);
        }
        if (Math.abs(dc) <= speed) {
            player.setVisualCol(player.getPos().getCol());
        } else {
            player.setVisualCol(player.getVisualCol() + Math.signum(dc) * speed);
        }
    }

    private void approachVisualEnemy(Enemy e, double speed) {
        double dr = e.getPos().getRow() - e.getVisualRow();
        double dc = e.getPos().getCol() - e.getVisualCol();
        if (Math.abs(dr) <= speed) {
            e.setVisualRow(e.getPos().getRow());
        } else {
            e.setVisualRow(e.getVisualRow() + Math.signum(dr) * speed);
        }
        if (Math.abs(dc) <= speed) {
            e.setVisualCol(e.getPos().getCol());
        } else {
            e.setVisualCol(e.getVisualCol() + Math.signum(dc) * speed);
        }
    }

    //-------------------collision and win detection-----------------------

    private void checkCollision() {
        double pr = player.getVisualRow();
        double pc = player.getVisualCol();
        for (Enemy e : enemies) {
            double dr = pr - e.getVisualRow();
            double dc = pc - e.getVisualCol();
            double dist = Math.sqrt(dr * dr + dc * dc);
            if (dist < COLLISION_THRESHOLD) {
                gameState = GameState.LOST;
                return;
            }
        }
    }

    private void checkWin() {
        //only check win if we're still playing, otherwise we might overwrite a win or loss that just happened
        if (gameState != GameState.PLAYING) {
            return;
        }
        if (eatenPellets >= totalPellets) {
            gameState = GameState.WON;
        }
    }

    //-------------------reset-----------------------

    private int countPellets() {
        int n = 0;
        for (int r = 0; r < mapData.getRows(); r++) {
            for (int c = 0; c < mapData.getCols(); c++) {
                if (mapData.hasPellet(r, c)) n++;
            }
        }
        return n;
    }

    // Resets the game to the initial state, ready for a new playthrough.
    public void reset() {
        //map back to initial state
        mapData.resetMap();

        //player back to start
        Position ps = mapData.getPlayerStart();
        player.setPos(ps);
        player.setVisualRow(ps.getRow());
        player.setVisualCol(ps.getCol());
        player.setCurrentDirection(Direction.NONE);
        player.setRequestedDirection(Direction.NONE);
        player.setMoving(false);
        player.setScore(0);

        //enemies back to start
        for (Enemy e : enemies) {
            Position s;
            if (e instanceof Pinky) {
                s = mapData.getPinkyStart();
            } else if (e instanceof Inky) {
                s = mapData.getInkyStart();
            } else if (e instanceof Blinky) {
                s = mapData.getBlinkyStart();
            } else {
                s = e.getPos();
            }
            e.setPos(s);
            e.setVisualRow(s.getRow());
            e.setVisualCol(s.getCol());
            e.setDirection(Direction.NONE);
        }

        eatenPellets = 0;
        gameState = GameState.START_SCREEN;
    }
}
