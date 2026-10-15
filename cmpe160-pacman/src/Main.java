// Ahmet Ensar Usta



import java.awt.event.KeyEvent;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main {

    //frame delay in ms ~50fps
    private static final int FRAME_DELAY_MS = 15;

    //edge trigger flags for keys that should fire only once per press
    private static boolean wasPDown = false;
    private static boolean wasSpaceDown = false;
    private static boolean wasRDown = false;

    public static void main(String[] args) {
        try {
            //load map data this class is immutable
            MapData mapData = loadMapData("data/map.txt");

            //single shared bfs path finder for all enemies
            BFSPathFinder finder = new BFSPathFinder();

            //create the player based on the starting position give in the map data
            Player player = new Player(mapData.getPlayerStart());

            //create enemies with their start positions and the finder
            Enemy[] enemies = new Enemy[]{
                    new Pinky(mapData.getPinkyStart(), finder),
                    new Inky(mapData.getInkyStart(), finder),
                    new Blinky(mapData.getBlinkyStart(), finder)
            };

            Game game = new Game(player, enemies, mapData);

            GameRenderer renderer = new GameRenderer(mapData, game);
            renderer.setupDraw();

            //----------main game loop---------------------------------------------------------------------
            while (true) {
                handleInput(game);

                Game.GameState s = game.getGameState();
                if (s == Game.GameState.PLAYING) {
                    game.update();
                    renderer.tickAnimation();
                } else if (s == Game.GameState.READY) {
                    game.checkReadyTimeout();
                }

                renderer.drawGame();
                StdDraw.pause(FRAME_DELAY_MS);
            }
        } catch (FileNotFoundException e) {
            System.out.println("Map file could not be loaded.");
            e.printStackTrace();
        }
    }

    //-----------------------------Input handling----------------------------------------------

    private static void handleInput(Game game) {
        //q is quit and edge-triggered
        if (StdDraw.isKeyPressed(KeyEvent.VK_Q)) {
            System.exit(0);
        }

        Game.GameState s = game.getGameState();

        //space to start the game and it is also edge triggered
        boolean spaceDown = StdDraw.isKeyPressed(KeyEvent.VK_SPACE);
        if (spaceDown && !wasSpaceDown) {
            if (s == Game.GameState.START_SCREEN) {
                game.startReady();
            }
        }
        wasSpaceDown = spaceDown;

        //p to pause it is also edge triggered
        boolean pDown = StdDraw.isKeyPressed(KeyEvent.VK_P);
        if (pDown && !wasPDown) {
            if (s == Game.GameState.PLAYING || s == Game.GameState.PAUSED) {
                game.togglePause();
            }
        }
        wasPDown = pDown;

        //r to reset and it is also edge triggered
        boolean rDown = StdDraw.isKeyPressed(KeyEvent.VK_R);
        if (rDown && !wasRDown) {
            if (s == Game.GameState.LOST || s == Game.GameState.WON) {
                game.reset();
            }
        }
        wasRDown = rDown;

        //arrow keys to change the requested direction of the player, only in the playing state
        if (s == Game.GameState.PLAYING) {
            if (StdDraw.isKeyPressed(KeyEvent.VK_UP)) {
                game.getPlayer().setRequestedDirection(Game.Direction.UP);
            } else if (StdDraw.isKeyPressed(KeyEvent.VK_DOWN)) {
                game.getPlayer().setRequestedDirection(Game.Direction.DOWN);
            } else if (StdDraw.isKeyPressed(KeyEvent.VK_LEFT)) {
                game.getPlayer().setRequestedDirection(Game.Direction.LEFT);
            } else if (StdDraw.isKeyPressed(KeyEvent.VK_RIGHT)) {
                game.getPlayer().setRequestedDirection(Game.Direction.RIGHT);
            }
        }
    }

    //----------map loader------------------------------

    private static MapData loadMapData(String filePath) throws FileNotFoundException {
        Scanner scanner = new Scanner(new File(filePath));

        int rows = scanner.nextInt();
        int cols = scanner.nextInt();
        scanner.nextLine();

        String[] playerLine = scanner.nextLine().split(" ");
        Position playerStart = new Position(
                Integer.parseInt(playerLine[1]),
                Integer.parseInt(playerLine[2])
        );

        String[] directEnemyLine = scanner.nextLine().split(" ");
        Position directEnemyStart = new Position(
                Integer.parseInt(directEnemyLine[1]),
                Integer.parseInt(directEnemyLine[2])
        );

        String[] randomChaseEnemyLine = scanner.nextLine().split(" ");
        Position randomChaseEnemyStart = new Position(
                Integer.parseInt(randomChaseEnemyLine[1]),
                Integer.parseInt(randomChaseEnemyLine[2])
        );

        String[] closestCornerEnemyLine = scanner.nextLine().split(" ");
        Position closestCornerEnemyStart = new Position(
                Integer.parseInt(closestCornerEnemyLine[1]),
                Integer.parseInt(closestCornerEnemyLine[2])
        );

        String[] cornerHeader = scanner.nextLine().split(" ");
        int cornerCount = Integer.parseInt(cornerHeader[1]);

        Position[] corners = new Position[cornerCount];
        for (int i = 0; i < cornerCount; i++) {
            int r = scanner.nextInt();
            int c = scanner.nextInt();
            scanner.nextLine();
            corners[i] = new Position(r, c);
        }

        char[][] map = new char[rows][cols];
        for (int i = 0; i < rows; i++) {
            String line = scanner.nextLine();
            for (int j = 0; j < cols; j++) {
                map[i][j] = line.charAt(j);
            }
        }

        scanner.close();

        return new MapData(
                map,
                playerStart,
                directEnemyStart,
                randomChaseEnemyStart,
                closestCornerEnemyStart,
                corners
        );
    }
}
