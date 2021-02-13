#include<stdio.h>
#include<cs50.h>
#include<string.h>
#include<ctype.h>
#include<stdlib.h>

int main(int argc, string argv[])
{
    int k;
    if (argc == 2)
    {
        int n = strlen(argv[1]);

        for (int i = 0; i < n; i++)
        {
            if (isdigit(argv[1][i]) != 0)
            {
                k = atoi(argv[1]);
            }
            else
            {
                printf("Usage: ./caesar key\n");
                return 1;
            };
        };
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    };

    while (k > 26)
    {
        k = k - 26;
    };

    string p = get_string("Plain text:");

    int l = strlen(p);

    int j = 0;

    while (j < l + 1)
    {
        if ((p[j] >= 65 && p[j] <= 90) && ((p[j] + k) > 90))
        {
            p[j] = ((p[j] + k) % 26);

            while (p[j] < 65)
            {
                p[j] = p[j] + 26;
            };
            j++;
        }
        else if ((p[j] >= 65 && p[j] <= 90) && (p[j] + k < 90))
        {
            p[j] = p[j] + k;
            j++;
        }
        else if ((p[j] >= 97 && p[j] <= 122) && (p[j] + k > 122))
        {
            p[j] = ((p[j] + k) % 26);

            while (p[j] < 97)
            {
                p[j] = p[j] + 26;
            };

            j++;
        }
        else if ((p[j] >= 97 && p[j] <= 122) && (p[j] + k <= 122))
        {
            p[j] = p[j] + k;
            j++;
        }
        else
        {
            j++;
        }
    };

    printf("ciphertext: %s\n", p);

}