package model.expresion;

import exception.TypeNotMatchException;
import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.adts.MyDictionary;
import model.programStateComponents.SymbolTable;
import model.type.BoolType;
import model.type.IType;
import model.values.BoolValue;
import model.values.IValue;

public class LogicExpression implements IExpression{
    public LogicExpression(IExpression e1, IExpression e2, int op) {
        this.e1 = e1;
        this.e2 = e2;
        this.op = op;
    }

    IExpression e1;
    IExpression e2;
    int op; // 1 - and, 2 - or, 3 - not


    @Override
    public IValue evaluate(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        SymbolTable table = state.getSymbolTable();
        if(op == 1){
            IValue v1 = e1.evaluate(state);
            if(v1.getType().equals(new BoolType())){
                IValue v2 = e2.evaluate(state);
                if(v2.getType().equals(new BoolType())){
                    boolean b1 = ((BoolValue)v1).getVal();
                    boolean b2 = ((BoolValue)v2).getVal();
                    return new BoolValue(b1 && b2);
                }
                else
                    throw new ExpressionException("Second operand is not a boolean");
            }
            else
                throw new ExpressionException("First operand is not a boolean");
        }
        else if(op == 2){
            IValue v1 = e1.evaluate(state);
            if(v1.getType().equals(new BoolType())){
                IValue v2 = e2.evaluate(state);
                if(v2.getType().equals(new BoolType())){
                    boolean b1 = ((BoolValue)v1).getVal();
                    boolean b2 = ((BoolValue)v2).getVal();
                    return new BoolValue(b1 || b2);
                }
                else
                    throw new ExpressionException("Second operand is not a boolean");
            }
            else
                throw new ExpressionException("First operand is not a boolean");
        }
        else if(op == 3){
            IValue v1 = e1.evaluate(state);
            if(v1.getType().equals(new BoolType())){
                boolean b1 = ((BoolValue)v1).getVal();
                return new BoolValue(!b1);
            }
            else
                throw new ExpressionException("Operand is not a boolean");
        }
        else
            throw new ExpressionException("Invalid operation");

    }

    @Override
    public String toString() {
        if(op == 1)
            return e1.toString() + " && " + e2.toString();
        else if(op == 2)
            return e1.toString() + " || " + e2.toString();
        else if(op == 3)
            return "!" + e1.toString();
        else
            return "Invalid operation";
    }

    @Override
    public IType typeCheck(MyDictionary<String, IType> typeEnv) throws TypeNotMatchException, AdtException {
        IType t1 = e1.typeCheck(typeEnv);
        IType t2 = e2.typeCheck(typeEnv);
        if(t1.equals(new BoolType()) && t2.equals(new BoolType()))
            return new BoolType();
        else
            throw new TypeNotMatchException("Operands of a logic expression must be boolean");
    }

}
