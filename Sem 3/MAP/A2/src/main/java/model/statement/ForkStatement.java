package model.statement;

import exception.TypeNotMatchException;
import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.adts.MyDictionary;
import model.programStateComponents.ExecutionStack;
import model.type.IType;

public class ForkStatement implements IStatement{
    IStatement innerStatement;

    public ForkStatement(IStatement innerStatement) {
        this.innerStatement = innerStatement;
    }

    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        return new ProgramState(new ExecutionStack(),state.getSymbolTable().copy(),state.getOutput(),state.getFileTable(), state.getHeapTable(), innerStatement);
    }

    @Override
    public MyDictionary<String, IType> typecheck(MyDictionary<String, IType> typeEnv) throws TypeNotMatchException {
        innerStatement.typecheck(typeEnv.copy());
        return typeEnv;
    }

    @Override
    public String toString() {
        return "fork(" + innerStatement.toString() + ")";
    }
}
