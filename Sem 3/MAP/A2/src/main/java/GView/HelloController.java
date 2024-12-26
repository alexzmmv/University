package GView;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Label;

public class HelloController {
    @FXML
    private Label welcomeText;

    @FXML
    protected void onHelloButtonClick() {
        welcomeText.setText("Welcome to JavaFX Application!");
    }

    public void onExitButtonClick(ActionEvent actionEvent) {
        System.exit(0);
    }

    public void onAboutButtonClick(ActionEvent actionEvent) {
        welcomeText.setText("This is a simple JavaFX application created using Intelij.");
    }
}