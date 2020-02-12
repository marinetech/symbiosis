/*
 * gcc -O2 xchg.c && ./xchg
 * gcc -O20 -S xchg.c && vi xchg.s
 * */
#include <stdio.h>

int main()
{
    int a = 3, b = -6;
