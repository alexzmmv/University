package exception;

public class TypeNotMatchException extends RuntimeException {
    public TypeNotMatchException(String message) {
        super(message);
    }
}
