package model.statement;

import model.ProgramState;
import model.exception.AdtException;
import model.exception.ExecutionException;
import model.exception.ExpressionException;
import model.expresion.IExpression;
import model.type.BoolType;
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
        return state;
    }

    @Override
    public String toString() {
        return "if (" + exp + ") then (" + thenS + ")" + (!elseS.equals(new NopStatement()) ? "" : " else (" + elseS + ")");
    }
}
