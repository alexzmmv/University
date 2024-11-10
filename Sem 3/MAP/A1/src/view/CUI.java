package view;

import controller.Controller;
import model.Atendee;
import model.Pair;

import java.util.Scanner;

public class CUI {
    Scanner scanner;
    Controller controller;
    public CUI(Scanner scanner, Controller controller){
        System.out.println("Welcome to the conference management system");
        try {
            this.controller = controller;
            this.scanner = scanner;
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
    public void run(){
        while(true){
            printMenu();
            String option = scanner.nextLine();
            switch(option){
                case "1":
                    System.out.println("Enter the name of the attendee");
                    String name = scanner.nextLine();
                    System.out.println("Enter the type of the attendee (professor, student, expert)");
                    String type = scanner.nextLine();
                    System.out.println("Is the attendee presenting? (yes/no)");
                    String present = scanner.nextLine();
                    Boolean is_presenting = present.equals("yes");
                    try {
                        controller.addAttendee(name, is_presenting, type);
                    } catch (Exception e) {
                        printError(e.getMessage());
                    }
                    break;
                case "2":
                    System.out.println("Enter the name of the attendee to delete");
                    String nameToDelete = scanner.nextLine();
                    try {
                        controller.deleteAttendee(nameToDelete);
                        printMessage("Attendee succefully deleted");
                    } catch (Exception e) {
                        printError(e.getMessage());
                    }
                    break;
                case "3":
                    Pair<Atendee[],Integer> atendees = controller.getAtendees();
                    printMessage("---------------------------------");
                    for(int i=0;i<atendees.getSecond();i++){
                        printAttendee(atendees.getFirst()[i].toString());
                    }
                    printMessage("---------------------------------");
                    break;
                case "4":
                    Pair<Atendee[],Integer> presentators = controller.getPresentingAtendees();
                    printMessage("---------------------------------");
                    printMessage("Presentators:");
                    for(int i=0;i<presentators.getSecond();i++){
                        printAttendee(presentators.getFirst()[i].toString());
                    }
                    printMessage("---------------------------------");
                    break;
                case "0":
                    printMessage("Goodbye!");
                    System.exit(0);
                    break;
                default:
                    System.out.println("Invalid option");
            }
        }
    }
    void printMenu() {
        System.out.println("1. Add an attendee");
        System.out.println("2. Delete an attendee");
        System.out.println("3. List all attendees");
        System.out.println("4. List all presenters");
        System.out.println("0. Exit");
    }

    void printError(String error) {
        System.out.println("Error: " + error);
    }

    void printMessage(String message) {
        System.out.println(message);
    }

    void printAttendee(String attendee) {
        System.out.println(attendee);
    }
}
