package GUI;

import controller.IController;
import controller.MultiThreadedController;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import repository.MultiThreadRepo;

import java.io.IOException;

public class GInterpreter extends Application {
    static IController controller;
    FXMLLoader mainWindowLoader = new FXMLLoader();

    public static void setController(IController controller) {
        GInterpreter.controller = controller;
    }

    @Override
    public void start(Stage stage) throws IOException {
        if(controller == null)
            System.err.println("Controller can not be null");

        mainWindowLoader.setLocation(getClass().getResource("MainWindow.fxml"));
        mainWindowLoader.setControllerFactory(c -> new GMainController(controller));

        Parent mainWindowRoot = mainWindowLoader.load();
        GMainController mainWindowController = mainWindowLoader.getController();

        stage.setTitle("Interpreter MAP 2023 - 2024");
        stage.setScene(new Scene(mainWindowRoot));
        stage.show();

        Stage secondaryStage = new Stage();
        FXMLLoader setProgramLoader = new FXMLLoader();
        setProgramLoader.setControllerFactory(c -> new SelectProgramWindowController(controller, mainWindowController));
        setProgramLoader.setLocation(getClass().getResource("SelectProgramWindow.fxml"));

        Parent setProgramRoot = setProgramLoader.load();
        SelectProgramWindowController setProgramController = setProgramLoader.getController();

        secondaryStage.setTitle("Select program");
        secondaryStage.setScene(new Scene(setProgramRoot));
        secondaryStage.show();
    }

    public void run(String[] args) {
        launch(args);
    }

    public static void main(String[] args) {
        setController(new MultiThreadedController(new MultiThreadRepo())); // Set the controller
        launch(args); // Pass the args parameter
    }
}