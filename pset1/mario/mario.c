#include<stdio.h>
#include<cs50.h>

int main(void)
{
    int n;

    do
    {

        n = get_int("length:\n");

    }

    while (n < 1 || n > 8);

    for (int a = 0; a < n; a++)
    {

        for (int b = n - 1; b > a; b--)
        {
            printf(" ");
        };
        for (int c = 0; c <= a; c++)
        {
            printf("#");
        };

        printf("  ");

        for (int c = 0; c <= a; c++)
        {
            printf("#");
        };

        printf("\n");

    };

}
