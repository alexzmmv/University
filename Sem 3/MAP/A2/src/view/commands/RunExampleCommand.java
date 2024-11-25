package view.commands;

import controller.IController;

import java.io.PrintWriter;
import java.util.Scanner;

public class RunExampleCommand extends Command {
    IController controller;

    public RunExampleCommand(String key, String description, IController controller) {
        super(key, description);
        this.controller = controller;
    }

    @Override
    public void execute() {
        System.out.println("Display flag? (y/n)");

        String flag = new Scanner(System.in).nextLine();
        while(!flag.equals("y") && !flag.equals("n")) {
            System.out.println("Invalid flag. Please enter y or n.");
            flag = new Scanner(System.in).nextLine();
        }
        try {
            controller.executeAll(flag.equals("y"));
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}
