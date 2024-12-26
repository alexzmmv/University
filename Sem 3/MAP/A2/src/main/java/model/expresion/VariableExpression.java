package model.expresion;

import exception.TypeNotMatchException;
import model.ProgramState;
import exception.AdtException;
import exception.ExpressionException;
import exception.VariableNotDefinedException;
import model.adts.MyDictionary;
import model.programStateComponents.SymbolTable;
import model.type.IType;
import model.values.IValue;

public class VariableExpression implements IExpression {

    String id;

    public VariableExpression(String id) {
        this.id = id;
    }

    @Override
    public IValue evaluate(ProgramState state) throws ExpressionException, AdtException {
        SymbolTable table = state.getSymbolTable();
        if(!table.isDefined(id))
            throw new VariableNotDefinedException("Variable " + id + " is not defined");
        return table.lookup(id);
    }

    @Override
    public String toString() {
        return id;
    }

    @Override
    public IType typeCheck(MyDictionary<String, IType> typeEnv) throws TypeNotMatchException, AdtException {
        return typeEnv.lookup(id);
    }
}
