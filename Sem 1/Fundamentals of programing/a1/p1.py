#1
def is_positive_integer_prime(pozitive_integer :int) -> bool :
    if pozitive_integer < 2:
        return False
    if pozitive_integer == 2 :
        return True
    if pozitive_integer % 2 == 0:
        return False
    for i in range(3,pozitive_integer//2,2) :
        if pozitive_integer % i == 0:
            return False
    return True

def Subproblem_1(n :int)->int:
    if is_positive_integer_prime(n) == True :
       n+=1
    while is_positive_integer_prime(n) == False :
        n+=1
    return n

n=int(input("Enter a number:"))
print("Next prime number after",n,"is:",Subproblem_1(n))