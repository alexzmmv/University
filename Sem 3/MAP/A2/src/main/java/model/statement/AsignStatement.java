package model.statement;

import exception.*;
import model.ProgramState;
import model.adts.MyDictionary;
import model.adts.MyIStack;
import model.expresion.IExpression;
import model.programStateComponents.SymbolTable;
import model.type.IType;
import model.values.IValue;

public class AsignStatement implements IStatement {
    String id;
    IExpression expression;

    public AsignStatement(String id, IExpression expression) {
        this.id = id;
        this.expression = expression;
    }

    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        MyIStack<IStatement> stack = state.getExecutionStack();
        SymbolTable symbolTable = state.getSymbolTable();
        if (symbolTable.isDefined(id)) {
            IValue value = expression.evaluate(state);
            IType type = symbolTable.lookup(id).getType();
            if (value.getType().equals(type)) {
                symbolTable.give(id, value);
            } else {
                throw new ExpressionException("Declared type of variable " + id + " and type of the assigned expression do not match");
            }
        }
        else throw new VariableNotDefinedException("The used variable " + id + " was not declared before");
        return null;
    }

    @Override
    public String toString() {
        return id + " = " + expression.toString();
    }

    @Override
    public MyDictionary<String, IType> typecheck(MyDictionary<String, IType>  typeEnv) throws TypeNotMatchException {
        IType typevar = null;
        try {
            typevar = typeEnv.lookup(id);
        } catch (AdtException e) {
            throw new TypeNotMatchException("Assignment statement: " + e.getMessage());
        }
        IType typexp = null;
        try {
            typexp = expression.typeCheck(typeEnv);
        } catch (AdtException e) {
            throw new TypeNotMatchException("Assignment statement: " + e.getMessage());
        }
        if (typevar.equals(typexp))
            return typeEnv;
        else
            throw new TypeNotMatchException("Assignment statement: right hand side and left hand side have different types ");
    }

}