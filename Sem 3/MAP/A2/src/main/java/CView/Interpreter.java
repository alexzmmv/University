package CView;

import controller.*;
import model.*;
import repository.*;
import repository.MultiThreadRepo;
import CView.commands.*;
import model.statement.*;
import model.expresion.*;
import model.type.*;
import model.values.*;
import model.adts.*;
import exception.*;
import model.programStateComponents.*;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Interpreter {
    public static void main(String[] args) {

        TextMenu menu = new TextMenu();

        IStatement ex1 = new CompoundStatement(
                new VariableDeclarationStatement("v", new IntType()),
                new CompoundStatement(
                        new AsignStatement("v", new ValueExpression(new StringValue("idk"))),
                        new PrintStatement(new VariableExpression("v"))
                )
        );
        System.out.println("Checking ex1 type");
        try {
            ex1.typecheck(new MyDictionary<String, IType>());
            ProgramState prg1 = new ProgramState(new ExecutionStack(), new SymbolTable(), new Output(), new FileTable(), new HeapTable(), ex1);
            IRepo repo1 = new MultiThreadRepo(prg1, "log1.txt");
            IController ctr1 = new MultiThreadedController(repo1);
            menu.addCommand(new RunExampleCommand("1", ex1.toString(), ctr1));
            System.out.println("ex1 typecheck done");
        } catch (TypeNotMatchException e) {
            System.out.println("ex1 typecheck problem:"+e.getMessage());
        }
        IStatement ex2= new CompoundStatement(
                new VariableDeclarationStatement("varf", new StringType()),
                new CompoundStatement(
                        new AsignStatement("varf", new ValueExpression(new StringValue("test.in"))),
                        new CompoundStatement(
                                new OpenReadFileStatement(new VariableExpression("varf")),
                                new CompoundStatement(
                                        new VariableDeclarationStatement("varc", new IntType()),
                                        new CompoundStatement(
                                                new ReadFileStatement(new VariableExpression("varf"), "varc"),
                                                new CompoundStatement(
                                                        new PrintStatement(new VariableExpression("varc")),
                                                        new CompoundStatement(
                                                                new ReadFileStatement(new VariableExpression("varf"), "varc"),
                                                                new CompoundStatement(
                                                                        new PrintStatement(new VariableExpression("varc")),
                                                                        new CloseReadFileStatement(new VariableExpression("varf"))
                                                                )
                                                        )
                                                )
                                        )
                                )
                        )
                )
        );
        System.out.println("Checking ex2 type");
        try {
            ex2.typecheck(new MyDictionary<String, IType>());
            ProgramState prg2 = new ProgramState(new ExecutionStack(), new SymbolTable(), new Output(), new FileTable(), new HeapTable(), ex2);
            IRepo repo2 = new MultiThreadRepo(prg2, "log2.txt");
            IController ctr2 = new MultiThreadedController(repo2);
            menu.addCommand(new RunExampleCommand("2", ex2.toString(), ctr2));
            System.out.println("ex2 typecheck done");
        }
        catch (TypeNotMatchException e) {
            System.out.println("ex2 typecheck problem:"+e.getMessage());
        }
        IStatement ex3 = new CompoundStatement(
                new VariableDeclarationStatement("f", new StringType()),
                new CompoundStatement(
                        new AsignStatement("f", new ValueExpression(new StringValue("test.in"))),
                        new CompoundStatement(
                                new VariableDeclarationStatement("a", new IntType()),
                                new CompoundStatement(
                                        new VariableDeclarationStatement("b", new IntType()),
                                        new CompoundStatement(
                                                new OpenReadFileStatement(new VariableExpression("f")),
                                                new CompoundStatement(
                                                        new ReadFileStatement(new VariableExpression("f"), "a"),
                                                        new CompoundStatement(
                                                                new ReadFileStatement(new VariableExpression("f"), "b"),
                                                                new CompoundStatement(
                                                                        new IfStatement(
                                                                                new ComparisonExpression(new VariableExpression("a"), new VariableExpression("b"), ">="),
                                                                                new PrintStatement(new VariableExpression("a")),
                                                                                new NopStatement()
                                                                        ),
                                                                        new CloseReadFileStatement(new VariableExpression("f"))
                                                                )
                                                        )
                                                )
                                        )
                                )
                        )
                ));
        System.out.println("Checking ex3 type");
        try {
            ex3.typecheck(new MyDictionary<String, IType>());
            ProgramState prg3 = new ProgramState(new ExecutionStack(), new SymbolTable(), new Output(), new FileTable(), new HeapTable(), ex3);
            IRepo repo3 = new MultiThreadRepo(prg3, "log3.txt");
            IController ctr3 = new MultiThreadedController(repo3);
            menu.addCommand(new RunExampleCommand("3", ex3.toString(), ctr3));
            System.out.println("ex3 typecheck done");
        }
        catch (TypeNotMatchException e) {
            System.out.println("ex3 problem:"+e.getMessage());
        }

        IStatement ex4 = new CompoundStatement(
                new VariableDeclarationStatement("v", new IntType()),
                new CompoundStatement(
                        new VariableDeclarationStatement("a", new ReferenceType(new IntType())),
                        new CompoundStatement(
                                new AsignStatement("v", new ValueExpression(new IntValue(10))),
                                new CompoundStatement(
                                        new newStatement("a", new ValueExpression(new IntValue(22))),
                                        new CompoundStatement(
                                                new ForkStatement(
                                                        new CompoundStatement(
                                                               new CompoundStatement(new wHStatement(new VariableExpression("a"), new ValueExpression(new IntValue(100))),
                                                                        new AsignStatement("v", new ValueExpression(new IntValue(32)))),
                                                                        new CompoundStatement(
                                                                                new PrintStatement(new VariableExpression("v")),
                                                                                new PrintStatement(new rHExpression(new VariableExpression("a"))))
                                                        )
                                                ),
                                                new CompoundStatement(
                                                        new PrintStatement(new rHExpression(new VariableExpression("a"))),
                                                        new CompoundStatement(new newStatement("a",new ValueExpression(new IntValue(1000))),
                                                            new CompoundStatement(
                                                                new PrintStatement(new VariableExpression("v")),
                                                                new ForkStatement(new newStatement("a",new ValueExpression(new IntValue(999))))
                                                        )
                                                )
                                        )
                                )
                )
        )));
        System.out.println("Checking ex4 type");
        try {
            ex4.typecheck(new MyDictionary<String, IType>());
            ProgramState prg4 = new ProgramState(new ExecutionStack(), new SymbolTable(), new Output(), new FileTable(), new ConcurentHeapTable(), ex4);
            IRepo repo4 = new MultiThreadRepo(prg4, "log4.txt");
            ExecutorService executor = Executors.newFixedThreadPool(2);
            IController ctr4 = new MultiThreadedController(repo4, executor, true);
            menu.addCommand(new RunExampleCommand("4", ex4.toString(), ctr4));
            System.out.println("ex4 typecheck done");
        }
        catch (TypeNotMatchException e) {
            System.out.println("ex4 problem:"+e.getMessage());
        }
        menu.addCommand(new ExitCommand("exit", "Exits the interpreter"));
        System.out.println("\n");
        menu.show();

    }
}