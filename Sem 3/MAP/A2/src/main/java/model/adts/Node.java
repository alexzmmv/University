package model.adts;

public class Node<T> {
    T value;
    Node left,right;

    public Node getRight() {
        return right;
    }

    public void setRight(Node right) {
        this.right = right;
    }

    public Node getLeft() {
        return left;
    }

    public void setLeft(Node left) {
        this.left = left;
    }

    public T getValue() {
        return value;
    }

    public void setValue(T value) {
        this.value = value;
    }

    public Node(T value) {
        this.value = value;
        right = null;
        left = null;
    }

    @Override
    public String toString() {
        return value.toString();
    }
}
