#include "UI.h"
#include <stdio.h>
#include <string.h>
void show(Repository *repo) {
    char s[200];
    printf("Found %d medicine:\n", getLengthRepo(repo));
    for (int i = 0; i < getLengthRepo(repo); ++i) {
        medToString(getMed(repo, i), s);
        printf("%s\n", s);
    }
    printf("\n\n");
}

int read_integer()
{
    int input, temp, status;
    status = scanf_s("%d", &input,190);
    while(status!=1){
        while((temp=getchar()) != EOF && temp != '\n');
        printf("\nInvalid input... please enter a number:");
        status = scanf_s("%d", &input,190);
    }

    return input;
}


void startUI(Repository *repo) {
    int option;
    int x;
    char name[40];
    int concentration;
    int quantity;
    float price;
    printf("1. Add medicine\n");
    printf("2. Remove medicine\n");
    printf("3. Update medicine\n");
    printf("4. Filter \n");
    printf("5. Short supply\n");
    printf("6. Undo\n");
    printf("7. Redo\n");
    printf("9. Help\n");
    printf("0. Exit\n");
    while (1) {
        Repository* newRepo = createRepository(10);
        printf("Choose an option:");
        option= read_integer();
        switch (option) {
            case 1:
                printf("Name: ");
                scanf("%s", name);
                printf("Concentration: ");
                concentration= read_integer();
                printf("Quantity: ");
                quantity= read_integer();
                printf("Price: ");
                scanf_s("%f", &price,10);
                if (addMedicine(repo, name, concentration, quantity, price))
                    printf("Successfull operation\n");
                else
                    printf("Meh, didn't work, contact the dev\n");
                break;
            case 2:
                printf("Name: ");
                scanf("%s", name);
                printf("Concentration: ");
                concentration= read_integer();
                if (removeMedicine(repo, name, concentration))
                    printf("Successfull operation\n");
                else
                    printf("Meh, medicine not found\n");
                break;
            case 3:
                printf("Name: ");
                scanf("%s", name);
                printf("Concentration: ");
                concentration= read_integer();
                printf("Quantity: ");
                quantity= read_integer();
                printf("Price: ");
                scanf_s("%f", &price,10);
                if (updateMedicine(repo, name, concentration, quantity, price))
                    printf("Successfull operation\n");
                else
                    printf("Meh, didn't work, contact the dev\n");
                break;
            case 4:
                printf("Type of filtering:\n");
                printf("1. Name\n");
                printf("2. Price lower than:\n");
                while (1) {
                    scanf_s("%d", &x,10);
                    switch (x) {
                        case 1:
                            printf("Name: ");
                            getchar();
                            fgets(name, 40, stdin);
                            if(name[0]=='\n'){
                                show(repo);
                                break;
                            }
                            name[strlen(name) - 1] = '\0';
                            filterByName(repo, newRepo, name);
                            sort_repo(newRepo, compare_by_name);
                            show(newRepo);
                            break;
                        case 2:
                            printf("Price: ");
                            scanf_s("%f", &price,10);
                            filterByPrice(repo, newRepo, price);
                            sort_repo(newRepo, compare_by_price);
                            show(newRepo);
                            break;
                        default:
                            printf("Invalid option\n");
                            break;
                    }
                    break;
                }
                break;
            case 5:
                printf("Quantity: ");
                scanf_s("%d", &x,10);
                shortSupply(repo, newRepo, x);
                printf("Sort by:\n");
                printf("1. Name\n");
                printf("2. Quantity\n");
                printf("3. Price\n");
                x=read_integer();
                switch (x) {
                    case 1:
                        sort_repo(newRepo, compare_by_name);
                        break;
                    case 2:
                        sort_repo(newRepo, compare_by_quantity);
                        break;
                    case 3:
                        sort_repo(newRepo, compare_by_price);
                        break;
                    default:
                        printf("Invalid option\n");
                        break;
                }
                show(newRepo);
                break;
            case 6:
                if(undo(repo))
                    printf("Operation Successfull\n");
                else
                    printf("Operation failed, no more undos\n");
                break;
            case 7:
                if(redo(repo))
                    printf("Operation Successfull\n");
                else
                    printf("Operation failed, no more redos\n");
                break;
            case 9:
                printf("1. Add medicine\n");
                printf("2. Remove medicine\n");
                printf("3. Update medicine\n");
                printf("4. Filter\n");
                printf("5. Short supply\n");
                printf("6. Undo\n");
                printf("7. Redo\n");
                printf("9. Help\n");
                printf("10. Exit\n");
                break;
            case 0:
                return;
            default:
                printf("Invalid option\n");
                break;
        }
        destroyRepository(newRepo);
    }
}