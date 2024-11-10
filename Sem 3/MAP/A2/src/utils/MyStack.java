package utils;

import java.util.Stack;

public class MyStack<T> implements MyIStack<T>{
    Stack<T> stack;
    public MyStack(){
        stack = new Stack<T>();
    }
    @Override
    public T pop() {
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

}
