package GUI;

import controller.IController;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ListView;
import javafx.scene.input.KeyCode;
import model.Hardcoded;
import model.statement.IStatement;

public class SelectProgramWindowController {
    IController controller;
    GMainController mainWindowController;

    @FXML
    private ListView<IStatement> programsListView;

    @FXML
    private Button selectProgramButton;

    public SelectProgramWindowController(IController controller, GMainController mainWindowController) {
        this.controller = controller;
        this.mainWindowController = mainWindowController;
    }

    @FXML
    public void initialize() {
        programsListView.setItems(FXCollections.observableList(Hardcoded.hardcodedPrograms));
        selectProgramButton.setOnAction(actionEvent -> {
            try{
                int index = programsListView.getSelectionModel().getSelectedIndex();
                if (index < 0) {
                    System.out.println("No index selected");
                } else if (index >= Hardcoded.hardcodedPrograms.size()) {
                    System.out.println("No program at selected index");
                } else {
                    System.out.println("Selected program " + index);
                }
                this.controller.setProgram(Hardcoded.hardcodedPrograms.get(index));
                this.mainWindowController.refresh();
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        });
        this.mainWindowController.refresh();
        this.programsListView.setOnKeyPressed(keyEvent -> {
            if (keyEvent.getCode() == KeyCode.ENTER) {
                selectProgramButton.fire();
            }
        });

    }
}