package model.expresion;

import exception.*;
import model.ProgramState;
import model.adts.MyDictionary;
import model.programStateComponents.SymbolTable;
import model.type.IType;
import model.type.IntType;
import model.values.IValue;
import model.values.IntValue;

public class ArithmeticExpression implements IExpression {
    IExpression exp1, exp2;
    int op;//1-plus, 2-minus, 3-multiply, 4-divide

    public ArithmeticExpression(IExpression exp1, IExpression exp2, int op) {
        this.exp1 = exp1;
        this.exp2 = exp2;
        this.op = op;
    }

    @Override
    public IValue evaluate(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        SymbolTable table = state.getSymbolTable();
        IValue v1, v2;
        v1 = exp1.evaluate(state);
        if(v1.getType().equals(new IntType())) {
           v2 = exp2.evaluate(state);
           if(v2.getType().equals(new IntType())){
               IntValue i1 = (IntValue)v1;
                IntValue i2 = (IntValue)v2;
                int n1, n2;
                n1 = i1.getVal();
                n2 = i2.getVal();
                switch(op){
                    case 1:
                        return new IntValue(n1+n2);
                    case 2:
                        return new IntValue(n1-n2);
                    case 3:
                        return new IntValue(n1*n2);
                    case 4:
                        if(n2 == 0)
                            throw new DivisionByZeroException("Division by zero");
                        return new IntValue(n1/n2);
                    default:
                        throw new ExpressionException("Invalid operation");
                }
           }
              else
                throw new ExpressionException("Second operand is not an integer");
        }
        else
            throw new ExpressionException("First operand is not an integer");
    }

    @Override
    public String toString() {
        String s = "";
        switch(op){
            case 1:
                s = "+";
                break;
            case 2:
                s = "-";
                break;
            case 3:
                s = "*";
                break;
            case 4:
                s = "/";
                break;
        }
        return exp1.toString() + s + exp2.toString();
    }

    @Override
    public IType typeCheck(MyDictionary<String, IType> typeEnv) throws TypeNotMatchException, AdtException {
        IType t1, t2;
        t1 = exp1.typeCheck(typeEnv);
        t2 = exp2.typeCheck(typeEnv);
        if(t1.equals(new IntType()) && t2.equals(new IntType()))
            return new IntType();
        else
            throw new TypeNotMatchException("Arithmetic operands must be integers");
    }

}
