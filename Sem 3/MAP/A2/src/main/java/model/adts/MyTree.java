package model.adts;

import exception.AdtException;

import java.util.ArrayList;
import java.util.List;

public class MyTree<T> implements MyITree {
    private Node<T> root;

    public MyTree(MyIStack<T> executionStack) throws AdtException {
        root = new Node<T>(executionStack.peek());
        executionStack.pop();
        Node<T> current = root;
        while (!executionStack.isEmpty()) {
            current.right = new Node<T>(executionStack.peek());
            executionStack.pop();
            current = current.right;
        }
    }

    public Node<T> getRoot() {
        return root;
    }
    public void setRoot(Node<T> root) {
        this.root = root;
    }

    public MyTree() {
        root=null;
    }

    public void inorderTraversal(List<T> list, Node node) {
        if (node == null) return ;
        inorderTraversal(list, node.left);
        list.add((T) node.value);
        inorderTraversal(list, node.right);
    }

    public boolean isEmpty() {
        return root == null;
    }

    @Override
    public String toString() {
        List<T> list = new ArrayList<T>();
        inorderTraversal(list, root);
        return list.toString();
    }
}
