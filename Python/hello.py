import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.Random;

public class SnakeGame extends JPanel implements ActionListener {
    private final int TILE_SIZE = 25;
    private final int GRID_SIZE = 20;
    private final int SCREEN_SIZE = TILE_SIZE * GRID_SIZE;
    private final int DELAY = 150;

    private final int[] x = new int[GRID_SIZE * GRID_SIZE];
    private final int[] y = new int[GRID_SIZE * GRID_SIZE];
    private int snakeLength;
    private int foodX, foodY;
    private char direction = 'R'; // U=Up, D=Down, L=Left, R=Right
    private boolean running = true;
    private Timer timer;

    public SnakeGame() {
        setPreferredSize(new Dimension(SCREEN_SIZE, SCREEN_SIZE));
        setBackground(Color.black);
        setFocusable(true);
        addKeyListener(new KeyAdapter() {
            public void keyPressed(KeyEvent e) {
                switch (e.getKeyCode()) {
                    case KeyEvent.VK_LEFT: if (direction != 'R') direction = 'L'; break;
                    case KeyEvent.VK_RIGHT: if (direction != 'L') direction = 'R'; break;
                    case KeyEvent.VK_UP: if (direction != 'D') direction = 'U'; break;
                    case KeyEvent.VK_DOWN: if (direction != 'U') direction = 'D'; break;
                }
            }
        });
        startGame();
    }

    private void startGame() {
        snakeLength = 3;
        for (int i = 0; i < snakeLength; i++) {
            x[i] = 100 - i * TILE_SIZE;
            y[i] = 100;
        }
        spawnFood();
        timer = new Timer(DELAY, this);
        timer.start();
    }

    private void spawnFood() {
        Random rand = new Random();
        foodX = rand.nextInt(GRID_SIZE) * TILE_SIZE;
        foodY = rand.nextInt(GRID_SIZE) * TILE_SIZE;
    }

    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (running) {
            g.setColor(Color.red);
            g.fillRect(foodX, foodY, TILE_SIZE, TILE_SIZE);
            for (int i = 0; i < snakeLength; i++) {
                g.setColor(i == 0 ? Color.green : Color.lightGray);
                g.fillRect(x[i], y[i], TILE_SIZE, TILE_SIZE);
            }
        } else {
            g.setColor(Color.white);
            g.drawString("Game Over", SCREEN_SIZE / 2 - 30, SCREEN_SIZE / 2);
        }
    }

    public void actionPerformed(ActionEvent e) {
        if (running) {
            move();
            checkCollision();
            checkFood();
        }
        repaint();
    }

    private void move() {
        for (int i = snakeLength; i > 0; i--) {
            x[i] = x[i - 1];
            y[i] = y[i - 1];
        }
        switch (direction) {
            case 'L': x[0] -= TILE_SIZE; break;
            case 'R': x[0] += TILE_SIZE; break;
            case 'U': y[0] -= TILE_SIZE; break;
            case 'D': y[0] += TILE_SIZE; break;
        }
    }

    private void checkCollision() {
        for (int i = 1; i < snakeLength; i++) {
            if (x[0] == x[i] && y[0] == y[i]) running = false;
        }
        if (x[0] < 0 || x[0] >= SCREEN_SIZE || y[0] < 0 || y[0] >= SCREEN_SIZE) running = false;
    }

    private void checkFood() {
        if (x[0] == foodX && y[0] == foodY) {
            snakeLength++;
            spawnFood();
        }
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("贪吃蛇");
        SnakeGame game = new SnakeGame();
        frame.add(game);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);
    }
}