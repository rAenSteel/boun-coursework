// Starter code provided by the CMPE 160 course staff
import java.awt.*;

public class GameRenderer {
    //delays for animation frames
    private static final int PACMAN_ANIMATION_DELAY = 2;
    private static final int ENEMY_ANIMATION_DELAY = 6;

    private static final double PLAYER_SIZE = 1;
    private static final double ENEMY_SIZE = 1;

    //pixel size of each sell in the grid
    private static final int CELL_PIXEL_WIDTH = 24;
    private static final int CELL_PIXEL_HEIGHT = 24;
    private static final int HUD_HEIGHT = 2;

    private static final String PACMAN_HALF_IMAGE = "assets/PacmanHalfOpen.png";
    private static final String PACMAN_CLOSED_IMAGE = "assets/PacmanClosed.png";
    private static final String PACMAN_FULL_IMAGE = "assets/PacmanFullOpen.png";

    private static final String READY_IMAGE = "assets/Ready.png";
    private static final String GAME_OVER_IMAGE = "assets/GameOver.png";

    private static final Color BACKGROUND_COLOR = new Color(0, 0, 0);
    private static final Color WALL_COLOR = new Color(0, 110, 255);
    private static final Color PELLET_COLOR = new Color(255, 184, 151);

    private int animationTick;

    private final Game game;
    private final MapData mapData;

    private final int cols;
    private final int rows;

    //constructor
    public GameRenderer(MapData mapData, Game game) {
        this.mapData = mapData;
        this.game = game;
        this.animationTick = 0;
        this.cols = mapData.getCols();
        this.rows = mapData.getRows();
    }

    private int getPacmanAnimationFrame() {
        return (animationTick / PACMAN_ANIMATION_DELAY) % 4;
    }

    //method to be called in the game loop to advance the animation tick, which controls the animation frames for both Pacman and the enemies.
    public void tickAnimation() {
        if (game.getGameState() == Game.GameState.PLAYING) {
            animationTick++;
        }
    }

    private boolean useSecondEnemyFrame() {
        return (animationTick / ENEMY_ANIMATION_DELAY) % 2 == 1;
    }

    private String getPacmanImagePath() {
        if (!game.getPlayer().isMoving()) {
            return PACMAN_HALF_IMAGE;
        }

        int frame = getPacmanAnimationFrame();

        return switch (frame) {
            case 0 -> PACMAN_CLOSED_IMAGE;
            case 2 -> PACMAN_FULL_IMAGE;
            default -> PACMAN_HALF_IMAGE;
        };
    }

    private double getPacmanAngle() {
        Game.Direction dir = game.getPlayer().getCurrentDirection();

        if (dir == Game.Direction.RIGHT) return 0;
        if (dir == Game.Direction.UP) return 90;
        if (dir == Game.Direction.LEFT) return 180;
        if (dir == Game.Direction.DOWN) return 270;
        return 0;
    }

    public void setupDraw() {
        StdDraw.setCanvasSize(
                cols * CELL_PIXEL_WIDTH,
                (rows + HUD_HEIGHT) * CELL_PIXEL_HEIGHT
        );

        StdDraw.setXscale(0, cols);
        StdDraw.setYscale(0, rows + HUD_HEIGHT);

        StdDraw.enableDoubleBuffering();
    }

    private double toScreenX(int col) {
        return col + 0.5;
    }

    private double toScreenY(int row) {
        return rows - row - 0.5;
    }

    private void drawPellets() {
        StdDraw.setPenColor(PELLET_COLOR);

        for (int row = 0; row < rows; row++) {
            for (int col = 0; col < cols; col++) {
                if (mapData.getTile(row, col) == '.') {
                    StdDraw.filledCircle(toScreenX(col), toScreenY(row), 0.07);
                }
            }
        }
    }

    //to draw the walls
    private void drawBoard() {
        for (int row = 0; row < rows; row++) {
            for (int col = 0; col < cols; col++) {
                if (mapData.getTile(row, col) == '#') {
                    double x = toScreenX(col);
                    double y = toScreenY(row);

                    StdDraw.setPenColor(WALL_COLOR);
                    StdDraw.filledSquare(x, y, 0.42);

                    StdDraw.setPenColor(new Color(80, 80, 255));
                    StdDraw.square(x, y, 0.42);
                }
            }
        }
    }

    //pacman drawing
    private void drawPlayer() {
        double x = game.getPlayer().getVisualCol() + 0.5;
        double y = rows - game.getPlayer().getVisualRow() - 0.5;

        String imagePath = getPacmanImagePath();
        double angle = getPacmanAngle();

        StdDraw.picture(x, y, imagePath, PLAYER_SIZE, PLAYER_SIZE, angle);
    }

    private String getEnemyImagePath(Enemy enemy) {
        Game.Direction dir = enemy.getDirection();
        boolean secondFrame = useSecondEnemyFrame();

        if (enemy instanceof Pinky) {
            if (dir == Game.Direction.UP) return secondFrame ? "assets/PinkyUp2.png" : "assets/PinkyUp.png";
            if (dir == Game.Direction.DOWN) return secondFrame ? "assets/PinkyDown2.png" : "assets/PinkyDown.png";
            if (dir == Game.Direction.LEFT) return secondFrame ? "assets/PinkyLeft2.png" : "assets/PinkyLeft.png";
            if (dir == Game.Direction.RIGHT) return secondFrame ? "assets/PinkyRight2.png" : "assets/PinkyRight.png";
            return "assets/PinkyRight.png";
        }

        if (enemy instanceof Inky) {
            if (dir == Game.Direction.UP) return secondFrame ? "assets/InkyUp2.png" : "assets/InkyUp.png";
            if (dir == Game.Direction.DOWN) return secondFrame ? "assets/InkyDown2.png" : "assets/InkyDown.png";
            if (dir == Game.Direction.LEFT) return secondFrame ? "assets/InkyLeft2.png" : "assets/InkyLeft.png";
            if (dir == Game.Direction.RIGHT) return secondFrame ? "assets/InkyRight2.png" : "assets/InkyRight.png";
            return "assets/InkyRight.png";
        }

        if (enemy instanceof Blinky) {
            if (dir == Game.Direction.UP) return secondFrame ? "assets/BlinkyUp2.png" : "assets/BlinkyUp.png";
            if (dir == Game.Direction.DOWN) return secondFrame ? "assets/BlinkyDown2.png" : "assets/BlinkyDown.png";
            if (dir == Game.Direction.LEFT) return secondFrame ? "assets/BlinkyLeft2.png" : "assets/BlinkyLeft.png";
            if (dir == Game.Direction.RIGHT) return secondFrame ? "assets/BlinkyRight2.png" : "assets/BlinkyRight.png";
            return "assets/BlinkyRight.png";
        }

        return "assets/PinkyRight.png";
    }

    //method to draw the enemies
    private void drawEnemies() {
        for (Enemy enemy : game.getEnemies()) {
            double x = enemy.getVisualCol() + 0.5;
            double y = rows - enemy.getVisualRow() - 0.5;

            String imagePath = getEnemyImagePath(enemy);
            StdDraw.picture(x, y, imagePath, ENEMY_SIZE, ENEMY_SIZE);
        }
    }

    //HUD drawing method
    private void drawHUD() {
        StdDraw.setPenColor(StdDraw.WHITE);
        StdDraw.textLeft(0.5, rows + 0.5, "Score: " + game.getPlayer().getScore());
    }

    //ready picture drawing method
    private void drawReadyMessage() {
        StdDraw.picture((double) cols / 2, (double) rows / 2, READY_IMAGE, 3.0, 0.8);
    }

    //this draws the start screen
    private void drawStartScreen() {
        StdDraw.setPenColor(Color.YELLOW);
        StdDraw.text((double) cols / 2, (double) rows / 2 + 1.0, "PACMAN");
        StdDraw.setPenColor(Color.WHITE);
        StdDraw.text((double) cols / 2, (double) rows / 2 - 0.5, "PRESS SPACE TO START");
    }

    //pause screen drawer
    private void drawPauseScreen() {
        StdDraw.setPenColor(Color.WHITE);
        StdDraw.text((double) cols / 2, (double) rows / 2, "PAUSED");
        StdDraw.text((double) cols / 2, (double) rows / 2 - 1.0, "PRESS P TO CONTINUE");
    }

    //game over screen drawer
    private void drawGameOverScreen() {
        StdDraw.picture((double) cols / 2, (double) rows / 2, GAME_OVER_IMAGE, 6.0, 1.5);
        StdDraw.setPenColor(Color.WHITE);
        StdDraw.text((double) cols / 2, (double) rows / 2 - 1.5, "Score: " + game.getPlayer().getScore());

        StdDraw.setPenColor(new Color(180, 0, 0));
        StdDraw.filledRectangle((double) cols / 2, (double) rows / 2 - 3.0, (double) cols / 2, 0.6);
        StdDraw.setPenColor(Color.WHITE);
        StdDraw.text((double) cols / 2, (double) rows / 2 - 3.0, "Press R to Restart   |   Press Q to Quit");
    }

    //win screen
    private void drawWonScreen() {
        StdDraw.setPenColor(Color.YELLOW);
        StdDraw.text((double) cols / 2, (double) rows / 2 + 1.0, "YOU WIN!");
        StdDraw.setPenColor(Color.WHITE);
        StdDraw.text((double) cols / 2, (double) rows / 2 - 0.5, "Score: " + game.getPlayer().getScore());

        StdDraw.setPenColor(new Color(180, 0, 0));
        StdDraw.filledRectangle((double) cols / 2, (double) rows / 2 - 3.0, (double) cols / 2, 0.6);
        StdDraw.setPenColor(Color.WHITE);
        StdDraw.text((double) cols / 2, (double) rows / 2 - 3.0, "Press R to Restart   |   Press Q to Quit");
    }


    // This method draws the entire game state on the screen, including the board, pellets, player, enemies, and HUD.
    // It also checks the game state to determine if it should draw the start screen, ready message, pause screen, game over screen, or won screen.
    public void drawGame() {
        StdDraw.clear(BACKGROUND_COLOR);

        drawBoard();
        drawPellets();
        drawPlayer();
        drawEnemies();
        drawHUD();

        if (game.getGameState() == Game.GameState.START_SCREEN) {
            drawStartScreen();
        } else if (game.getGameState() == Game.GameState.READY) {
            drawReadyMessage();
        } else if (game.getGameState() == Game.GameState.PAUSED) {
            drawPauseScreen();
        } else if (game.getGameState() == Game.GameState.LOST) {
            drawGameOverScreen();
        } else if (game.getGameState() == Game.GameState.WON) {
            drawWonScreen();
        }

        StdDraw.show();
    }
}
