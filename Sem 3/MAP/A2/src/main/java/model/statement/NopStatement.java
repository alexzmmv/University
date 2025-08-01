package model.statement;

import exception.TypeNotMatchException;
import model.ProgramState;
import exception.AdtException;
import exception.ExpressionException;
import model.adts.MyDictionary;
import model.type.IType;

public class NopStatement implements IStatement {

    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException {
        return null;
    }

    public String toString() {
        return "nop";
    }

    @Override
    public MyDictionary<String, IType> typecheck(MyDictionary<String, IType>  typeEnv) throws TypeNotMatchException {
        return typeEnv;
    }
}
