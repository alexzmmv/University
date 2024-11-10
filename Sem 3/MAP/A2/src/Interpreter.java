import controller.IController;
import controller.SingleThreadedController;
import model.ProgramState;
import model.expresion.ComparisonExpression;
import model.expresion.ValueExpression;
import model.expresion.VariableExpression;
import model.programStateComponents.ExecutionStack;
import model.programStateComponents.FileTable;
import model.programStateComponents.Output;
import model.programStateComponents.SymbolTable;
import model.statement.*;
import model.type.IntType;
import model.type.StringType;
import model.values.IntValue;
import model.values.StringValue;
import repository.IRepo;
import repository.SingleThreadRepo;
import view.TextMenu;
import view.commands.ExitCommand;
import view.commands.RunExampleCommand;

public class Interpreter {
    public static void main(String[] args) {
        IStatement ex1 = new CompoundStatement(
                new VariableDeclarationStatement("v", new IntType()),
                new CompoundStatement(
                        new AsignStatement("v", new ValueExpression(new IntValue(2))),
                        new PrintStatement(new VariableExpression("v"))
                )
        );
        ProgramState prg1 = new ProgramState(new ExecutionStack(), new SymbolTable(), new Output(), new FileTable(), ex1);
        IRepo repo1 = new SingleThreadRepo(prg1, "log1.txt");
        IController ctr1 = new SingleThreadedController(repo1);

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
        ProgramState prg2 = new ProgramState(new ExecutionStack(), new SymbolTable(), new Output(), new FileTable(), ex2);
        IRepo repo2 = new SingleThreadRepo(prg2, "log2.txt");
        IController ctr2 = new SingleThreadedController(repo2);

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
        ProgramState prg3 = new ProgramState(new ExecutionStack(), new SymbolTable(), new Output(), new FileTable(), ex3);
        IRepo repo3 = new SingleThreadRepo(prg3, "log3.txt");
        IController ctr3 = new SingleThreadedController(repo3);

        TextMenu menu = new TextMenu();
        menu.addCommand(new RunExampleCommand("run 1", ex1.toString(), ctr1));
        menu.addCommand(new RunExampleCommand("run 2", ex2.toString(), ctr2));
        menu.addCommand(new RunExampleCommand("run 3", ex3.toString(), ctr3));
        menu.addCommand(new ExitCommand("exit", "Exits the interpreter"));
        menu.show();
    }
}
