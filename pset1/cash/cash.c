#include<stdio.h>
#include<cs50.h>
#include<math.h>

void money(int c);

int n, cents;

int main(void)
{
    float change;

    do
    {

        change = get_float("Change owed:");

    }

    while (change < 0);

    cents = round(change * 100);

    money(25);

    int a = n;

    money(10);

    int b = n;

    money(5);

    int c = n;

    money(1);

    int d = n;

    printf("%i\n", a + b + c + d);

}

void money(int c)
{
    n = 0;

    while (c * n <= cents)
    {
        n++;
    }

    n--;

    cents = cents - c * n;

}