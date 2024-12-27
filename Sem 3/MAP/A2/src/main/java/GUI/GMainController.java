package GUI;

import controller.IController;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleObjectProperty;
import javafx.fxml.FXML;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.input.KeyCode;
import javafx.util.Pair;
import model.ProgramState;
import model.programStateComponents.IFileTable;
import model.programStateComponents.IHeap;
import model.programStateComponents.IOutput;
import model.statement.IStatement;
import model.values.IValue;

import java.util.List;
import java.util.NoSuchElementException;

public class GMainController {
    IController controller;
    IHeap heap;
    IOutput output;
    IFileTable fileTable;

    public GMainController(IController controller) {
        this.controller = controller;
    }
    @FXML
    private Label programStatesLabel;

    @FXML
    private ListView<Integer> programStatesListView;

    @FXML
    private ListView<IStatement> executionStackListView;

    @FXML
    private ListView<String> fileTableListView;

    @FXML
    private ListView<String> outListView;

    @FXML
    private TableView<Pair<Integer, IValue>> heapTableTableView;

    @FXML
    private TableColumn<Pair<Integer, IValue>, Integer> heapAddressesColumn;

    @FXML
    private TableColumn<Pair<Integer, IValue>, String> heapValuesColumn;

    @FXML
    private TableView<Pair<String, IValue>> symbolTableTableView;

    @FXML
    private TableColumn<Pair<String, IValue>, String> symbolNameColumn;

    @FXML
    private TableColumn<Pair<String, IValue>, String> symbolValueColumn;

    @FXML
    private Button runButton;

    @FXML
    private Button oneStepButton;

    public void refresh() {
        Integer selectedProgramId = this.programStatesListView.getSelectionModel().getSelectedItem();
        this.programStatesListView.getItems().clear();
        this.heapTableTableView.getItems().clear();
        this.outListView.getItems().clear();
        this.fileTableListView.getItems().clear();
        this.symbolTableTableView.getItems().clear();
        this.executionStackListView.getItems().clear();
       if(this.controller==null)
           System.err.println("Controller is null");
        this.programStatesLabel.setText("Program states: " + this.controller.getProgramList().size());
        this.controller.getProgramList().forEach(progState -> this.programStatesListView.getItems().add(progState.getId()));

        if (!this.controller.getProgramList().isEmpty()) {
            this.heap = this.controller.getProgramList().get(0).getHeapTable();
            this.output = this.controller.getProgramList().get(0).getOutput();
            this.fileTable = this.controller.getProgramList().get(0).getFileTable();

        }

        if (this.heap != null) {
            this.heap.toMap().forEach((key, value) ->
                    this.heapTableTableView.getItems().add(new Pair<>(key, value)));
        }

        if (this.output != null) {
            this.output.getOutputAsList().forEach(output
                    -> this.outListView.getItems().add(output.toString()));
        }

        if (this.fileTable != null) {
            this.fileTable.getFileList().forEach(key
                    -> this.fileTableListView.getItems().add(key.toString()));
        }

        ProgramState current;
        try{
            current = this.controller.getProgramList().stream().filter(x -> Integer.valueOf(x.getId()).equals(selectedProgramId)).findAny().get();
            current.getSymbolTable().toMap().forEach((x, y) -> this.symbolTableTableView.getItems().add(new Pair<>(x,y)));
            List<IStatement> statementList = current.getExecutionStack().toList();
            for(int i = statementList.size() - 1;i >= 0;i--){
                this.executionStackListView.getItems().add(statementList.get(i));
            }
            this.programStatesListView.getSelectionModel().select(selectedProgramId);
        } catch (NoSuchElementException e) {
            return;
        } finally {
            this.programStatesListView.refresh();
            this.heapTableTableView.refresh();
            this.outListView.refresh();
            this.fileTableListView.refresh();
            this.symbolTableTableView.refresh();
            this.executionStackListView.refresh();
        }
    }

    @FXML
    public void initialize() {
        this.heapAddressesColumn.setCellValueFactory(p -> new SimpleIntegerProperty(p.getValue().getKey()).asObject());
        this.heapValuesColumn.setCellValueFactory(p -> new SimpleObjectProperty<>(p.getValue().getValue().toString()));
        this.symbolNameColumn.setCellValueFactory(p -> new SimpleObjectProperty<>(p.getValue().getKey()));
        this.symbolValueColumn.setCellValueFactory(p -> new SimpleObjectProperty<>(p.getValue().getValue().toString()));
        this.refresh();

        this.oneStepButton.setOnAction(actionEvent -> {
            try {
                this.controller.executeOneStep();
            } catch (Exception e) {
                Alert alert = new Alert(Alert.AlertType.ERROR, e.getMessage());
                alert.show();
            }
            this.refresh();
        });

        this.runButton.setOnAction(actionEvent -> {
            try {
                this.controller.executeAllSteps();
            } catch (Exception e) {
                Alert alert = new Alert(Alert.AlertType.ERROR, e.getMessage());
                alert.show();
            }
            this.refresh();
        });
        this.programStatesListView.setOnMouseClicked(x -> this.refresh());
    }
}