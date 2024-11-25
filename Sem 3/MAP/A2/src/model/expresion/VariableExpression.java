package model.expresion;

import model.ProgramState;
import model.exception.AdtException;
import model.exception.ExpressionException;
import model.exception.VariableNotDefinedException;
import model.programStateComponents.SymbolTable;
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
}
