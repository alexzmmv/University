package model.programStateComponents;

import model.statement.IStatement;

import java.util.List;

public interface IExecutionStack {
    boolean isEmpty();
    List<IStatement> toList();


}
