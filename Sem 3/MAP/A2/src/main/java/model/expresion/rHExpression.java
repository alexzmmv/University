package model.expresion;

import exception.TypeNotMatchException;
import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.adts.MyDictionary;
import model.type.IType;
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
    public IType typeCheck(MyDictionary<String, IType> typeEnv) throws TypeNotMatchException, AdtException {
        IType type = expression.typeCheck(typeEnv);
        if(type instanceof ReferenceType){
            return ((ReferenceType) type).getInner();
        }
        throw new TypeNotMatchException("rH argument should be a reference type");
    }

    @Override
    public String toString() {
        return "rH(" + expression.toString() + ")";
    }
}
