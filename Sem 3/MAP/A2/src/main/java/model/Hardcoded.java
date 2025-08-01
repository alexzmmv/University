package model;


import com.sun.jdi.IntegerType;
import model.expresion.ComparisonExpression;
import model.expresion.ValueExpression;
import model.expresion.VariableExpression;
import model.expresion.rHExpression;
import model.statement.*;
import model.type.IntType;
import model.type.ReferenceType;
import model.type.StringType;
import model.values.IntValue;
import model.values.StringValue;

import java.util.ArrayList;
import java.util.List;

public class Hardcoded {
    public static final List<IStatement> hardcodedPrograms = new ArrayList<IStatement>(List.of(
            new CompoundStatement(
                    new VariableDeclarationStatement("v", new IntType()),
                    new CompoundStatement(
                            new AsignStatement("v", new ValueExpression(new StringValue("idk"))),
                            new PrintStatement(new VariableExpression("v"))
                    )
            ),
            new CompoundStatement(
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
            ),

            new CompoundStatement(
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
                    )),

            new CompoundStatement(
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
                            )))

    ));
}