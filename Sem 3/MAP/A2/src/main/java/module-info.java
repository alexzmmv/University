module com.compa.demo {
    requires javafx.controls;
    requires javafx.fxml;
    requires jdk.jdi;


    opens GUI to javafx.fxml;
    exports GUI;
    exports controller;
    opens controller to javafx.fxml;
}