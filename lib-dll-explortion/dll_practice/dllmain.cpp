// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "pch.h"
#include <stdio.h>
BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        printf("process attach!\n");
        break;
    case DLL_THREAD_ATTACH:
        printf("thread attach!\n");
        break;
    case DLL_THREAD_DETACH:
        printf("thread detach!\n");
        break;
    case DLL_PROCESS_DETACH:
        printf("process detach!\n");
        break;
    }
    return TRUE;
}

