% Base cases
merge([], L, L).
merge(L, [], L).


merge([H1|T1], [H2|T2], [H1|T]) :-
    H1 < H2,  
    merge(T1, [H2|T2], T).

merge([H1|T1], [H2|T2], [H2|T]) :-
    H1 > H2,
    merge([H1|T1], T2, T).

merge([H|T1], [H|T2], [H|T]) :-
    merge(T1, T2, T).




sortL([], []).
sortL([X], [X]).

sortL([X | T], Sorted) :-
    sortL(T, SortedTail),
    insert(X, SortedTail, Sorted).

insert(X, [], [X]). 
insert(X, [Y | T], [X, Y | T]) :- X =< Y.  
insert(X, [Y | T], [Y | SortedTail]) :- X > Y, insert(X, T, SortedTail).

mmerge([], L, L).

mmerge([H|T], Prev, Result) :-
    number(H),
    mmerge(T, Prev, Result).

mmerge([H|T], Prev, Result) :-
    is_list(H),
    sortL(H, Hn),            
    merge(Prev, Hn, Act),   
    mmerge(T, Act, Result). 
