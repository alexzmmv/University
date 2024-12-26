module com.compa.demo {
    requires javafx.controls;
    requires javafx.fxml;


    opens GView to javafx.fxml;
    exports GView;
}