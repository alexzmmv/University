:- initialization(main).

%helper functions
gcd(X, 0, X) :- !.

gcd(X, Y, Z) :-
    R is X mod Y,
    gcd(Y, R, Z).


%a)
insert([],N,_,[]):-N>1.

insert([],N,X,[X]):-N=:=1.

insert(L,N,X,R):-N=:=1,
    R=[X|L].

insert([H|T],N,X,[H|R]):-
    N>1,
    N1 is N-1,
    insert(T,N1,X,R).

%a modified don't insert, substitute

ainsert([],N,_,[]):-N>2.

ainsert([E],N,X,[X]):-N=:=2.

ainsert([H|T],N,X,R):-N=:=1,
    R=[X|T].

ainsert([H|T],N,X,[H|R]):-
    N>1,
    N1 is N-1,
    ainsert(T,N1,X,R).

%b)gcd of all elements in a list

gcdl([H1],G):-
    G is H1.

gcdl([H|T],G):-
    gcdl(T,G1),
    gcd(H,G1,G).

main:-
    %a test
    List=[8,80,0],
    X=100,
    N=2,
    insert(List,N,X,R),
    write(R),nl,
    gcdl(R,Gcdlist),
    write(Gcdlist),nl,
    Listn=[1,2,3,4],
    Nn=2,
    Xn=1234,
    ainsert(Listn,Nn,Xn,Rlist),
    write(Rlist),nl.

%p3