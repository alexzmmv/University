package model.statement;

import model.ProgramState;
import model.exception.AdtException;
import model.exception.ExecutionException;
import model.exception.ExpressionException;
import model.expresion.IExpression;
import model.type.IType;
import model.values.IValue;
import model.values.ReferenceValue;

public class wHStatement implements IStatement{
    IExpression adress;
    IExpression expression;

    public wHStatement(IExpression adress, IExpression expression) {
        this.adress = adress;
        this.expression = expression;
    }

    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        IValue value = adress.evaluate(state);
        IValue value2 = expression.evaluate(state);
        if(!(value.getType() instanceof ReferenceValue)){
            throw new ExecutionException("Heap should only be accessed through references");
        }
        if(!(value2.getType().equals(((ReferenceValue)value).getType()))){
            throw new ExecutionException("Type mismatch");
        }
        state.getHeapTable().write(((ReferenceValue)value).getAddress(), value2);
        return state;
    }

    @Override
    public String toString() {
        return "wH(" + adress.toString() + "," + expression.toString() + ")";
    }

}
