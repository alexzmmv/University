#9
def product_of_all_proper_factors(pozitive_integer:int)->int :
    if pozitive_integer<2:
        return 0
    if pozitive_integer==2:
        return 2
    divizor=2
    product=1
    while divizor<=n/2:
        if pozitive_integer % divizor == 0:
            product=product*divizor
        divizor+=1
    return product

flag=True
while flag==True:
    n=int(input("Enter a pozitive integer number:"))
    if n>=0:
        print("Product of all propper factors is:",product_of_all_proper_factors(n))
        flag=False
    else:
        print("Let's try again")