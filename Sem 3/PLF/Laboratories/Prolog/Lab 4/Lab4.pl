decompose(N, A, K) :-
    K > 0,
    Sum is (2 * A + K) * (K + 1) / 2,
    Sum =:= N.

mybetween(Low,High,Num) :-
    Low =< High,
    Num =  Low.

mybetween(Low,High,Num) :-
    Low < High,
    LowNext is Low + 1,
    mybetween(LowNext,High,Num).

find_decompositions(N, L) :-  
    findall([A, K], (mybetween(1, N, A), mybetween(0, N, K), decompose(N, A, K)), Decompositions),
    transform_sublists(Decompositions, L). 



transform_sublist([Start, 0], [Start]).  
transform_sublist([Start, Count], [Start | Rest]) :-
    Count > 0,
    Next is Start + 1,
    NewCount is Count - 1,
    transform_sublist([Next, NewCount], Rest).


transform_sublists([], []).
transform_sublists([[Start, Count] | Tail], [Tr | Rest]) :-
    transform_sublist([Start, Count], Tr),
    transform_sublists(Tail, Rest).
