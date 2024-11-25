package model.expresion;

import model.ProgramState;
import model.exception.AdtException;
import model.exception.ExecutionException;
import model.exception.ExpressionException;
import model.type.ReferenceType;
import model.values.IValue;
import model.values.ReferenceValue;

public class rHExpression implements IExpression {
    IExpression expression;

    public rHExpression(IExpression expression) {
        this.expression = expression;
    }

    @Override
    public IValue evaluate(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        IValue value = expression.evaluate(state);
        if(!(value.getType() instanceof ReferenceType)){
            throw new ExecutionException("Heap should only be accessed through references");
        }
        return state.getHeapTable().read(((ReferenceValue)value).getAddress());
    }

    @Override
    public String toString() {
        return "rH(" + expression.toString() + ")";
    }
}
