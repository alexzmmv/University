package exception;

public class VariableNotDefinedException extends ExpressionException {
    public VariableNotDefinedException(String message) {
        super(message);
    }

    public VariableNotDefinedException(String message, Throwable cause) {
        super(message, cause);
    }

    public VariableNotDefinedException(Throwable cause) {
        super(cause);
    }
}
