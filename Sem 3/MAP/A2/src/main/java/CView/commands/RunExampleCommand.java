package CView.commands;

import controller.IController;

public class RunExampleCommand extends Command {
    IController controller;

    public RunExampleCommand(String key, String description, IController controller) {
        super(key, description);
        this.controller = controller;
    }

    @Override
    public void execute() {
        try {
            controller.executeAllSteps();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}
