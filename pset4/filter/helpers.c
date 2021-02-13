#include "helpers.h"
#include<math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float aveg = (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.00;
            int avg = round(aveg);
            image[i][j].rgbtRed = avg ;
            image[i][j].rgbtBlue = avg ;
            image[i][j].rgbtGreen = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {


            int red = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int blue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            int green =  round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);

            if (red > 255)
            {
                image[i][j].rgbtRed = 255 ;
            }
            else
            {
                image[i][j].rgbtRed = red;
            }
            if (blue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = blue;
            }
            if (green > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = green;
            }
        }

    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE r = image[i][j];
            image[i][j] = image[i][width - 1 - j] ;
            image[i][width - 1 - j] = r;
        }
    }
    return;
}




// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int blue, red, green;

    float counter;

    RGBTRIPLE new_image[height][width];

    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            blue = 0;
            green = 0;
            red = 0;
            counter = 0.00;

            for (int k = -1; k < 2; k++)
            {
                if (j + k < 0 || j + k > height - 1)
                {
                    continue;
                }

                for (int h = -1; h < 2; h++)
                {
                    if (i + h < 0 || i + h > width - 1)
                    {
                        continue;
                    }

                    blue += image[j + k][i + h].rgbtBlue;
                    green += image[j + k][i + h].rgbtGreen;
                    red += image[j + k][i + h].rgbtRed;
                    counter++;
                }
            }

            // averages the sum to make picture look blurrier
            new_image[j][i].rgbtBlue = round(blue / counter);
            new_image[j][i].rgbtGreen = round(green / counter);
            new_image[j][i].rgbtRed = round(red / counter);
        }
    }

    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            image[j][i].rgbtBlue = new_image[j][i].rgbtBlue;
            image[j][i].rgbtGreen = new_image[j][i].rgbtGreen;
            image[j][i].rgbtRed = new_image[j][i].rgbtRed;
        }
    }
}
