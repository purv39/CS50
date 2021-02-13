#include<stdio.h>
#include<cs50.h>
#include<string.h>
#include<math.h>

void count_letter();
void count_words();
void count_sentence();


int n;
int l, w, s;

int main(void)
{

    string q = get_string("Text:");

    n = strlen(q);

    //Letters

    count_letter(q);

    //Words

    count_words(q);

    //Sentence

    count_sentence(q);

    float L = ((float)l / w) * 100;

    float S = ((float)s / w) * 100;

    float index = 0.0588 * L - 0.296 * S - 15.8;


    int grade = round(index);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    };

}

void count_letter(string q)
{
    int i = 0;
    l = n;


    while (i < n)
    {

        if ((65 <= q[i] && q[i] <= 90) || (q[i] >= 97 && q[i] <= 122))
        {
            i++;
        }

        else
        {
            l--;
            i++;
        };

    };

}

void count_words(string q)
{
    int j = 0;
    w = 0;

    while (j < n)
    {
        if (q[j] == 32)
        {
            w++;
            j++;
        }
        else
        {
            j++;
        };

    }
    w++;
    float words = w;

}

void count_sentence(string q)
{
    int k = 0;
    s = 0;

    while (k < n)
    {

        if (q[k] == 46 || q[k] == 33 || q[k] == 63)
        {
            s++;
            k++;

        }
        else
        {
            k++;
        };

    };

}



