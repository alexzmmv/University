%write a prediate to determin gcd of all numbers from a list

%base case
gcd(X, 0, X) :- !.

%recursive case
%mention- tail recursion
gcd(X, Y, Z) :-
    R is X mod Y,
    gcd(Y, R, Z).

%edge case- when list is empty
gcdList([],G):-
    G is -1.

%base case- when list contains one item
gcdList([H1],G):-
    G is H1,!.


%recursive case
gcdList([H|T],G):-
    gcdList(T,G1),
    gcd(H,G1,G).

%l1 homework: 