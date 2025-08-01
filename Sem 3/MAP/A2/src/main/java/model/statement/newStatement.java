package model.statement;

import exception.TypeNotMatchException;
import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.adts.MyDictionary;
import model.expresion.IExpression;
import model.expresion.ValueExpression;
import model.type.IType;
import model.type.ReferenceType;
import model.values.IValue;
import model.values.IntValue;
import model.values.ReferenceValue;

public class newStatement implements IStatement{
    String name;
    IExpression expression;

    public newStatement(String name) {
        this.name = name;
        expression = new ValueExpression(new IntValue());
    }

    @Override
    public MyDictionary<String, IType> typecheck(MyDictionary<String, IType>  typeEnv) throws TypeNotMatchException {
        IType typevar = null;
        try {
            typevar = typeEnv.lookup(name);
        } catch (AdtException e) {
            throw new TypeNotMatchException("new statement: " + e.getMessage());
        }
        IType typexp = null;
        try {
            typexp = expression.typeCheck(typeEnv);
        } catch (AdtException e) {
            throw new TypeNotMatchException("new statement: " + e.getMessage());
        }
        if(!(typevar instanceof ReferenceType))
            throw new TypeNotMatchException("new statement: variable is not a reference type");
        ReferenceType reftype = (ReferenceType) typevar;
        if (reftype.getInner().equals(typexp))
            return typeEnv;
        else
            throw new TypeNotMatchException("new statement: right hand side and left hand side have different types ");
    }

    public newStatement(String name, IExpression expression) {
        this.name = name;
        this.expression = expression;
    }

    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        IValue value = expression.evaluate(state);
        //if reeference variable internal type is not the same as  as the value type
        IType itype = state.getSymbolTable().lookup(name).getType();
        if(itype instanceof ReferenceType && !((ReferenceType)itype).getInner().equals(value.getType()))
            throw new ExecutionException("Type mismatch in new statement between reference type and value type");
        state.getSymbolTable().give(name,new ReferenceValue(state.getHeapTable().allocate(value), value.getType()));
        return null;
    }

    @Override
    public String toString() {
        return "new(" + name + "," + expression.toString() + ")";
    }
}
