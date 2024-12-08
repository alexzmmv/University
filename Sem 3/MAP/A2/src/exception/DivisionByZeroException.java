package exception;

public class DivisionByZeroException extends ExpressionException{
    public DivisionByZeroException(String message) {
        super(message);
    }
    public DivisionByZeroException(String message, Throwable cause) {super(message, cause);}
    public DivisionByZeroException(Throwable cause) {super(cause);}
}
