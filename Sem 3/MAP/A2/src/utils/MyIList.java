package utils;

public interface MyIList<T> {
    public void add(T el);
    public T get(int index);
    public int size();
    public boolean contains(T el);
    
}
