package exception;

public class ExecutionException extends Exception{
    public ExecutionException(String message) {
        super(message);
    }
    public ExecutionException(String message, Throwable cause) {super(message, cause);}
    public ExecutionException(Throwable cause) {super(cause);}
}