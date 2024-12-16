package model.statement;

import exception.TypeNotMatchException;
import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.adts.MyDictionary;
import model.expresion.IExpression;
import model.type.IType;
import model.type.ReferenceType;
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
    public MyDictionary<String, IType> typecheck(MyDictionary<String, IType>  typeEnv) throws TypeNotMatchException {
        IType type1, type2;
        try {
            type1 = adress.typeCheck(typeEnv);
        } catch (AdtException e) {
            throw new TypeNotMatchException("wH statement: " + e.getMessage());
        }
        try {
            type2 = expression.typeCheck(typeEnv);
        } catch (AdtException e) {
            throw new TypeNotMatchException("wH statement: " + e.getMessage());
        }
        if(type1.equals(new ReferenceType(type2))){
            return typeEnv;
        }
        throw new TypeNotMatchException("Type mismatch");
    }

    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        IValue value = adress.evaluate(state);
        IValue value2 = expression.evaluate(state);
        if(!(value.getType() instanceof ReferenceType)){
            throw new ExecutionException("Heap should only be accessed through references");
        }
        if(!value2.getType().equals( ((ReferenceType)value.getType()).getInner()) ){
            throw new ExecutionException("Type mismatch");
        }
        state.getHeapTable().write(((ReferenceValue)value).getAddress(), value2);
        return null;
    }

    @Override
    public String toString() {
        return "wH(" + adress.toString() + "," + expression.toString() + ")";
    }

}
