package controller;

import model.ProgramState;

import java.util.List;

public interface IGarbageCollector {
    public static void runGarbageCollector(List<ProgramState> prg) {}
    private static List<Integer> getActiveAddressesForState(ProgramState state) {return null;}
}
