import controller.IController;
import controller.MultiThreadedController;
import model.ProgramState;
import model.expresion.ComparisonExpression;
import model.expresion.ValueExpression;
import model.expresion.VariableExpression;
import model.expresion.rHExpression;
import model.programStateComponents.*;
import model.statement.*;
import model.type.IntType;
import model.type.ReferenceType;
import model.type.StringType;
import model.values.IntValue;
import model.values.ReferenceValue;
import model.values.StringValue;
import repository.IRepo;
import repository.MultiThreadRepo;
import view.TextMenu;
import view.commands.ExitCommand;
import view.commands.RunExampleCommand;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Interpreter {
    public static void main(String[] args) {


        IStatement ex1 = new CompoundStatement(
                new VariableDeclarationStatement("v", new IntType()),
                new CompoundStatement(
                        new AsignStatement("v", new ValueExpression(new IntValue(2))),
                        new PrintStatement(new VariableExpression("v"))
                )
        );

        ProgramState prg1 = new ProgramState(new ExecutionStack(), new SymbolTable(), new Output(), new FileTable(),new HeapTable(), ex1);
        IRepo repo1 = new MultiThreadRepo(prg1, "log1.txt");
        IController ctr1 = new MultiThreadedController(repo1);
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
        ProgramState prg2 = new ProgramState(new ExecutionStack(), new SymbolTable(), new Output(), new FileTable(),new HeapTable(), ex2);
        IRepo repo2 = new MultiThreadRepo(prg2, "log2.txt");
        IController ctr2 = new MultiThreadedController(repo2);

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
        ProgramState prg3 = new ProgramState(new ExecutionStack(), new SymbolTable(), new Output(), new FileTable(), new HeapTable(),ex3);
        IRepo repo3 = new MultiThreadRepo(prg3, "log3.txt");
        IController ctr3 = new MultiThreadedController(repo3);

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
                                                        new CompoundStatement(new newStatement("a",new ValueExpression(new StringValue("test"))),
                                                            new PrintStatement(new VariableExpression("v"))
                                                        )
                                                )
                                        )
                                )
                )
        ));
        ProgramState prg4 = new ProgramState(new ExecutionStack(), new SymbolTable(), new Output(), new FileTable(), new ConcurentHeapTable(), ex4);
        IRepo repo4 = new MultiThreadRepo(prg4, "log4.txt");
        //Thread pool of 2 threads
        ExecutorService executor = Executors.newFixedThreadPool(2);
        IController ctr4 = new MultiThreadedController(repo4,executor,true);
        TextMenu menu = new TextMenu();
        menu.addCommand(new RunExampleCommand("1", ex1.toString(), ctr1));
        menu.addCommand(new RunExampleCommand("2", ex2.toString(), ctr2));
        menu.addCommand(new RunExampleCommand("3", ex3.toString(), ctr3));
        menu.addCommand(new RunExampleCommand("4", ex4.toString(), ctr4));

        menu.addCommand(new ExitCommand("exit", "Exits the interpreter"));
        menu.show();

    }
}