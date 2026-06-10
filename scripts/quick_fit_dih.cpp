#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <cmath>
#include <stdexcept>

#include <Eigen/Dense>

#include <fmt/format.h>
#include <fmt/os.h>

#include <matplot/matplot.h>

#ifndef M_PI
#define M_PI 3.1415926535897932384626
#endif

Eigen::VectorXd multiple_to_RB(const Eigen::VectorXd k);

int main(int argc, char const *argv[]) {
    int n = 8;
    if (argc - 1 != 0) n = std::stoi(argv[1]);

    constexpr double phase = 0.;

    std::string line;

    int npoints = 0;
    std::ifstream ifile("QM.txt");
    if (!ifile.is_open()) {
        throw std::ios_base::failure("Cannot open \"QM.txt\" for reading.");
    }

    while (std::getline(ifile, line)) {
        if (line[0] == '#') continue;
        ++ npoints;
    }

    ifile.close();

    std::vector<double> qm_vec(npoints), mm_fitted_vec(npoints), y_vec(npoints), angle_vec(npoints);

    Eigen::Map<Eigen::VectorXd> angle(angle_vec.data(), angle_vec.size()), 
        qm(qm_vec.data(), qm_vec.size()), 
        mm_fitted(mm_fitted_vec.data(), mm_fitted_vec.size()), 
        y(y_vec.data(), y_vec.size());
    Eigen::VectorXd mm(npoints), angle_rad(npoints), t(npoints);

    std::ifstream ifile_QM("QM.txt");
    if (!ifile_QM.is_open()) {
        throw std::ios_base::failure("Cannot open \"QM.txt\" for reading.");
    }
    int i = 0;
    while (std::getline(ifile_QM, line)) {
        if (line[0] == '#') continue;
        std::istringstream iss(line);
        if (!(iss >> angle[i] >> qm[i])) {
            throw std::ios_base::failure("Cannot read data from \"QM.txt\".");
        }
        ++ i;
    }
    ifile_QM.close();

    std::ifstream ifile_MM("MM.xvg");
    if (!ifile_MM.is_open()) {
        throw std::ios_base::failure("Cannot open \"MM.xvg\" for reading.");
    }
    i = 0;
    while (std::getline(ifile_MM, line)) {
        if (line[0] == '#' || line[0] == '@') continue;
        std::istringstream iss(line);
        if (!(iss >> t[i] >> mm[i])) {
            throw std::ios_base::failure("Cannot read data from \"MM.xvg\".");
        }
        ++ i;
    }
    ifile_MM.close();

    qm.array() -= qm[0];
    qm *= 2625.5;
    mm.array() -= mm[0];

    y = qm - mm; // intrinsic
    angle_rad = angle / 180. * M_PI;

    Eigen::MatrixXd X(npoints, n + 1);
    for (int i = 1; i <= n; ++ i) {
        X.col(i) = (i * angle_rad).array().cos();
    }
    X.col(0).fill(1.);

    Eigen::VectorXd k(X.colPivHouseholderQr().solve(y));
    k[0] = - k.tail(n).sum();

    fmt::ostream ofile(fmt::output_file("fit_result.txt"));
    fmt::print("; func    phase        kd        pn\n");
    ofile.print("; func    phase        kd        pn\n");
    int funct = 9;
    for (int i = 0; i <= n; ++ i) {
        fmt::print("     {:1d}    {:6.1f}     {:10.6f}    {:2d}\n", funct, phase, k[i], i);
        ofile.print("     {:1d}    {:6.1f}     {:10.6f}    {:2d}\n", funct, phase, k[i], i);
    }
    ofile.close();

    Eigen::VectorXd fit(Eigen::VectorXd::Constant(npoints, 2. * k[0]));
    for (int i = 1; i <= n; ++ i) {
        fit.array() += k[i] * (1. + (i * angle_rad).array().cos());
    }

    if (n == 5) {
        fmt::print("\n");
        fmt::print("# Ryckaert-Bellemans:\n");
        funct = 3;

        Eigen::VectorXd C(multiple_to_RB(k));
        fmt::ostream ofile_RB(fmt::output_file("fit_result_RB.txt"));

        fmt::print("; func    C0         C1         C2         C3         C4         C5\n");
        ofile_RB.print("; func    C0         C1         C2         C3         C4         C5\n");
        fmt::print("     {:1d}{:11.5f}{:11.5f}{:11.5f}{:11.5f}{:11.5f}{:11.5f}\n", funct, 
            C[0], C[1], C[2], C[3], C[4], C[5]);
        ofile_RB.print("     {:1d}{:11.5f}{:11.5f}{:11.5f}{:11.5f}{:11.5f}{:11.5f}\n", funct, 
            C[0], C[1], C[2], C[3], C[4], C[5]);

        ofile_RB.close();
    }

    mm_fitted = mm + fit;

    fmt::ostream ofile_data(fmt::output_file("fit_data.txt"));
    ofile_data.print("# dihedral     QM          MM        Intrinsic\n");
    for (int i = 0; i < npoints; ++ i) {
        ofile_data.print("{:8.3f}    {:8.3f}    {:8.3f}    {:8.3f}\n", 
            angle[i], qm[i], mm_fitted[i], y[i]);
    }
    ofile_data.close();

    matplot::figure_handle fig(matplot::figure(true));
    fig->size(1440, 1080);
    matplot::axes_handle ax(fig->current_axes());

    std::vector<matplot::line_handle> pl(ax->plot(angle_vec, qm_vec, angle_vec, mm_fitted_vec, angle_vec, y_vec));
    pl[0]->marker("o").marker_face_color("red").marker_size(20).line_width(5).display_name("QM");
    pl[1]->marker("o").marker_face_color("blue").marker_size(20).line_width(5).display_name("MM");
    pl[2]->line_width(5).color("green").display_name("intrinsic");

    double angle_min = angle.minCoeff();
    double angle_max = angle.maxCoeff();
    std::vector<double> xticks(matplot::linspace(angle_min, angle_max, 7));
    ax->x_axis().tick_values(xticks);

    ax->xlabel("Dihedral (\u00B0)");
    ax->ylabel("Relative energy (kJ/mol)");

    double y_min = std::min({qm.minCoeff(), mm_fitted.minCoeff(), y.minCoeff()});
    double y_max = std::max({qm.maxCoeff(), mm_fitted.maxCoeff(), y.maxCoeff()});

    y_min = std::floor(y_min / 10.) * 10.;
    y_max = std::ceil(y_max / 10.) * 10.;

    std::vector<double> yticks;
    for (double y_val = y_min; y_val < y_max + 1.; y_val += 10.) {
        yticks.push_back(y_val);
    }
    ax->y_axis().tick_values(yticks);
    ax->ylim({y_min, y_max});

    ax->title("Fit Result");
    ax->legend();

    fig->save("fit_result.png");
    fig->save("fit_result.svg");

    matplot::show();

    return 0;
}

Eigen::VectorXd multiple_to_RB(const Eigen::VectorXd k) {
    if (k.size() != 6) throw std::invalid_argument("Only 6 terms of Ryckaert-Bellemans's potential is supported.");
    Eigen::VectorXd C(k.size());
    C[0] = 2. * k[0] + k[1] + k[3] + 2. * k[4] + k[5];
    C[1] = - k[1] + 3. * k[3] - 5. * k[5];
    C[2] = 2. * k[2] - 8. *  k[4];
    C[3] = -4. * k[3] + 20. * k[5];
    C[4] = 8. * k[4];
    C[5] = -16. * k[5];
    return C;
}

