package model.expresion;

import exception.TypeNotMatchException;
import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.adts.MyDictionary;
import model.programStateComponents.SymbolTable;
import model.type.IType;
import model.type.IntType;
import model.values.BoolValue;
import model.values.IValue;
import model.values.IntValue;

public class ComparisonExpression implements IExpression {
    private final IExpression e1;
    private final IExpression e2;
    private final String op;

    public ComparisonExpression(IExpression e1, IExpression e2, String op) {
        this.e1 = e1;
        this.e2 = e2;
        this.op = op;
    }

    @Override
    public IValue evaluate(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        SymbolTable table = state.getSymbolTable();
        IValue v1=e1.evaluate(state);
        IValue v2=e2.evaluate(state);
        if(!v1.getType().equals(new IntType()) || !v2.getType().equals(new IntType()))
            throw new ExpressionException("Both part of a comparison must be integer types");

        IntValue iv1=(IntValue)v1;
        IntValue iv2=(IntValue)v2;
        BoolValue result=new BoolValue(false);
        switch (op){
            case "<":
                result=new BoolValue(iv1.getVal()<iv2.getVal());
                break;
            case "<=":
                result=new BoolValue(iv1.getVal()<=iv2.getVal());
                break;
            case "==":
                result=new BoolValue(iv1.getVal()==iv2.getVal());
                break;
            case "!=":
                result=new BoolValue(iv1.getVal()!=iv2.getVal());
                break;
            case ">":
                result=new BoolValue(iv1.getVal()>iv2.getVal());
                break;
            case ">=":
                result=new BoolValue(iv1.getVal()>=iv2.getVal());
                break;
            default:
                throw new ExpressionException("Invalid comparison operator");
        }
        return result;
    }

    @Override
    public String toString() {
        return e1.toString() + " " + op + " " + e2.toString();
    }

    @Override
    public IType typeCheck(MyDictionary<String, IType> typeEnv) throws TypeNotMatchException, AdtException {
        IType t1=e1.typeCheck(typeEnv);
        IType t2=e2.typeCheck(typeEnv);
        if(t1.equals(new IntType()) && t2.equals(new IntType()))
            return new BoolValue(true).getType();
        else
            throw new TypeNotMatchException("Comparison operands must be integers");
    }
}
