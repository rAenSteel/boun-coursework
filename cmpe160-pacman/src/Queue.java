// Ahmet Ensar Usta

public class Queue<T> {

    private static final int INITIAL_CAPACITY = 16;

    private T[] list;
    private int head;
    private int tail;
    private int count;

    public Queue() {
        this.list = (T[]) new Object[INITIAL_CAPACITY];
        this.head = 0;
        this.tail = 0;
        this.count = 0;
    }

    public boolean isEmpty() {
        return count == 0;
    }

    public int size() {
        return count;
    }

    public void enqueue(T item) {
        if (count == list.length) {
            resize(list.length * 2);
        }
        list[tail] = item;
        tail = (tail + 1) % list.length;
        count++;
    }

    public T dequeue() {
        if (isEmpty()) {
            return null;
        }
        T item = list[head];
        list[head] = null;
        head = (head + 1) % list.length;
        count--;
        return item;
    }

    private void resize(int newCapacity) {
        T[] newArr = (T[]) new Object[newCapacity];
        for (int i = 0; i < count; i++) {
            newArr[i] = list[(head + i) % list.length];
        }
        list = newArr;
        head = 0;
        tail = count;
    }
}
