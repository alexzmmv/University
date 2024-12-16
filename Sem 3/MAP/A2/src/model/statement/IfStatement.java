package model.statement;

import exception.TypeNotMatchException;
import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.adts.MyDictionary;
import model.expresion.IExpression;
import model.type.BoolType;
import model.type.IType;
import model.values.BoolValue;
import model.values.IValue;

public class IfStatement implements IStatement {
    IStatement thenS;
    IStatement elseS;
    IExpression exp;

    public IfStatement(IExpression e, IStatement t, IStatement el) {
        exp = e;
        thenS = t;
        elseS = el;
    }

    @Override
    public ProgramState execute(ProgramState state) throws AdtException, ExpressionException, ExecutionException {
        IValue val = exp.evaluate(state);
        if (!val.getType().equals(new BoolType()))
            throw new ExpressionException("If condition is not a boolean");
        BoolValue bval = (BoolValue) val;
        if (bval.getVal())
            state.getExecutionStack().push(thenS);
        else
            state.getExecutionStack().push(elseS);
        return null;
    }

    @Override
    public String toString() {
        return "if (" + exp + ") then (" + thenS + ")" + (!elseS.equals(new NopStatement()) ? "" : " else (" + elseS + ")");
    }

    @Override
    public MyDictionary<String, IType> typecheck(MyDictionary<String, IType>  typeEnv) throws TypeNotMatchException {
        IType type = null;
        try {
            type = exp.typeCheck(typeEnv);
        } catch (AdtException e) {
            throw new TypeNotMatchException("If statement: " + e.getMessage());
        }
        if (!type.equals(new BoolType()))
            throw new TypeNotMatchException("If condition is not a boolean");
        thenS.typecheck(typeEnv);
        elseS.typecheck(typeEnv);
        return typeEnv;
    }
}
