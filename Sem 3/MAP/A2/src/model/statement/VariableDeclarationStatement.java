package model.statement;

import exception.TypeNotMatchException;
import model.ProgramState;
import model.adts.MyDictionary;
import model.adts.MyIDictionary;
import exception.AdtException;
import exception.ExpressionException;
import model.type.IType;
import model.values.IValue;

public class VariableDeclarationStatement implements IStatement{

    String name;
    IType type;

    public VariableDeclarationStatement(String name, IType type) {
        this.name = name;
        this.type = type;
    }

    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException {
        MyIDictionary<String, IValue> symbolTable = state.getSymbolTable();
        if (symbolTable.isDefined(name)) {
            throw new ExpressionException("Variable " + name + " is already declared");
        }
        symbolTable.put(name, type.defaultValue());
        return null;
    }

    @Override
    public String toString() {
        return type.toString() + " " + name;
    }

    @Override
    public MyDictionary<String, IType> typecheck(MyDictionary<String, IType>  typeEnv) throws TypeNotMatchException {
        try {
            typeEnv.put(name, type);
        } catch (AdtException e) {
            throw new TypeNotMatchException("Variable declaration statement: " + e.getMessage());
        }
        return typeEnv;
    }
}
