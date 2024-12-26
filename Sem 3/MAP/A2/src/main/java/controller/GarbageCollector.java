package controller;

import exception.InvalidAddressException;
import model.ProgramState;
import model.programStateComponents.IHeap;
import model.type.ReferenceType;
import model.values.IValue;
import model.values.ReferenceValue;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class GarbageCollector implements IGarbageCollector {

    public static void runGarbageCollector(List<ProgramState> states){
        if(states.size() < 1){
            return ;
        }
        IHeap heap = states.get(0).getHeapTable();
        List<Integer> activeAddresses = states.stream().flatMap(e -> GarbageCollector.getActiveAddressesForState(e).stream()).toList();
        heap.toMap().keySet().stream().filter(e -> !activeAddresses.contains(e)).forEach(e -> {
            try {
                heap.deallocate(e);
            } catch (InvalidAddressException ex) {
                throw new RuntimeException(ex);
            }
        });
    }

    private static List<Integer> getActiveAddressesForState(ProgramState state) {
        return state.getSymbolTable().toMap().values().stream()
                .filter(e -> e.getType() instanceof ReferenceType)
                .map(e -> (ReferenceValue) e)
                .flatMap(value -> {
                    List<Integer> addresses = new ArrayList<Integer>();
                    while (true) {
                        if(value.getAddress() == 0){
                            break;
                        }
                        addresses.add(value.getAddress());
                        IValue next_value;
                        try {
                            next_value = state.getHeapTable().read(value.getAddress());
                        } catch (InvalidAddressException e) {
                            throw new RuntimeException(e);
                        }
                        if (!(next_value.getType() instanceof ReferenceType)) {
                            break;
                        }
                        value = (ReferenceValue) next_value;
                    }
                    return addresses.stream();
                }).collect(Collectors.toList());
    }

}
