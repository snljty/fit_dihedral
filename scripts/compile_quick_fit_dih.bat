@echo off

set EIGEN_ROOT=C:\eigen-3.4.1
set FMT_ROOT=C:\fmt-12.1.0
set MATPLOTPP_ROOT=C:\Matplot++-1.2.1

g++ -o quick_fit_dih quick_fit_dih.cpp ^
    -I %EIGEN_ROOT%\include\eigen3 ^
    -I %FMT_ROOT%\include ^
    -I %MATPLOTPP_ROOT%\include ^
    -L %FMT_ROOT%\lib -l fmt ^
    -L %MATPLOTPP_ROOT%\lib -l matplot ^
    -L %MATPLOTPP_ROOT%\lib\Matplot++ -l nodesoup ^
    -l gdi32 ^
    -Bstatic -O2 -s -DNDEBUG ^
    -std=c++17
