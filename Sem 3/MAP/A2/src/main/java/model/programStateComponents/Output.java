package model.programStateComponents;


import model.adts.MyList;
import model.values.IValue;

import java.util.List;

public class Output extends MyList<IValue> implements IOutput {
    public Output() {
        super();
    }

    public Output(MyList<IValue> list) {
        super();
    }

    public String toString() {
        return super.toString();
    }

    @Override
    public List<IValue> getOutputAsList() {
        return super.getList();
    }
}
