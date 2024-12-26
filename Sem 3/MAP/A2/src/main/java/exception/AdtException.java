package exception;

public class AdtException extends Exception {
    public AdtException(String message) {
        super(message);
    }
    public AdtException(String message, Throwable cause) {super(message, cause);}
    public AdtException(Throwable cause) {super(cause);}
}
