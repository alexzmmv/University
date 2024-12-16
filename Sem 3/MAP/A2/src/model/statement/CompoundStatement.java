package model.statement;

import exception.TypeNotMatchException;
import model.ProgramState;
import model.adts.MyDictionary;
import model.adts.MyIStack;
import exception.AdtException;
import exception.ExpressionException;
import model.type.IType;

public class CompoundStatement implements IStatement {
    IStatement first;
    IStatement second;

    public CompoundStatement(IStatement first, IStatement second) {
        this.first = first;
        this.second = second;
    }

    @Override
    public MyDictionary<String, IType> typecheck(MyDictionary<String, IType>  typeEnv) throws TypeNotMatchException {
        return second.typecheck(first.typecheck(typeEnv));
    }

    @Override
    public ProgramState execute(ProgramState state) throws AdtException, ExpressionException {
        MyIStack<IStatement> stack = state.getExecutionStack();
        stack.push(second);
        stack.push(first);
        return null;
    }

    @Override
    public String toString() {
        return first.toString() + " , " + second.toString();
    }
}
