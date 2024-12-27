package model.adts;

import exception.AdtException;

import java.util.List;
import java.util.Stack;

public class MyStack<T> implements MyIStack<T>{
    Stack<T> stack;
    public MyStack(){
        stack = new Stack<T>();
    }
    @Override
    public T pop() throws AdtException {
        if(stack.isEmpty())
            throw new AdtException("Stack is empty");
        return stack.pop();
    }

    @Override
    public void push(T el) {
        stack.push(el);
    }

    @Override
    public T top() {
        return stack.peek();
    }

    @Override
    public boolean isEmpty() {
        return stack.isEmpty();
    }

    @Override
    public T peek() {
        return stack.peek();
    }

    @Override
    public String toString() {
        String outS = "";
        for (T el : stack) {
            outS = outS + el.toString() + "|";
        }
        return outS;
    }

    protected List<T> getList() {
        return (List<T>) stack;
    }
}
