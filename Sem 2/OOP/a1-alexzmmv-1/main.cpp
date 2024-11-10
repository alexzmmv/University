#include <iostream>

using namespace std;

int eras[10000];

bool prime(int n){
    if(n==2)
        return true;
    if (n%2==0 or n<2)
    return false;

    for(int d=3;d*d<=n;d+=2)
        if (n%d==0)
            return false;
    return true;

}

void gen_eras(int n){
    for(int i=1;i<=n;i++){
        eras[i]=prime(i);
    }
}

pair<int, int> max1(pair<int, int> a,pair<int, int> b){
    if(a.second-a.first<b.second-b.first)
        return b;
    return a;
}

pair<int, int> p2(int vec[], int dim) {
    pair<int,int> init_pair=make_pair(1,1),max_pair=make_pair(1,1);
    for (int i=1; i <dim; i++) {
        if(eras[vec[i]+vec[i+1]]==true)
            init_pair.second++;
        else{
            max_pair=max1(init_pair,max_pair);
            init_pair=make_pair(i+1,i+1);
        }
    }
    return max1(max_pair,init_pair);
}

int main()
{
    gen_eras(10000);
    int ch;
    bool stop=false;
    while(!stop){
        cout<<"1.Generate all the prime numbers smaller than a given natural number n\n";
        cout<<"2.Given a vector of numbers, find the longest increasing contiguous subsequence, such the sum of that any 2 consecutive elements is a prime number\n";
        cout<<"3.Exit\n";
        cin>>ch;
        switch (ch){
            case 1:{
                int n;
                cout<<"n=";
                cin>>n;
                for(int i=2;i<n;i++){
                    if(eras[i]==true)
                        cout<<i<<' ';
                }
                cout<<"\n\n";
                break;
            }
            case 2:{
                int vector_dimension,vector[10000];
                cout<<"Vector_dimension=\n";
                cin >> vector_dimension;
                cout<<"\n";
                for(int i=1; i <= vector_dimension; i++){
                    printf("V[%d]=",i);
                    cin >> vector[i];
                    cout<<"\n";
                }
                pair<int,int> indices=p2(vector, vector_dimension);

                for(int i=indices.first; i <= indices.second; i++)
                    cout << vector[i] << ' ';
                cout<<"\n";
                break;
            }
            case 3:{
                stop=true;
                break;
            }
            default:{
                cout<<"Command doesn't exist\n\n";
            }
        }
    }
    return 0;
}
