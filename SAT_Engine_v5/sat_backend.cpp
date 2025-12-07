#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <random>
#include <omp.h>
#include <cmath>

namespace py = pybind11;

struct SATInstance {
    int n_vars;
    std::vector<std::vector<int>> clauses;

    SATInstance(int n, std::vector<std::vector<int>> cls)
        : n_vars(n), clauses(cls) {}
};

// Evaluar cuántas cláusulas están satisfechas
int evaluate(const SATInstance &inst, const std::vector<int> &assign) {
    int sat = 0;
    for (const auto &C : inst.clauses) {
        for (int lit : C) {
            int v = std::abs(lit) - 1;
            bool val = assign[v];
            if (lit < 0) val = !val;
            if (val) { sat++; break; }
        }
    }
    return sat;
}

// Breakcount: cuántas cláusulas se rompen al flippear x
int breakcount(const SATInstance &inst, const std::vector<int> &assign, int var) {
    int count = 0;
    for (const auto &C : inst.clauses) {
        bool before = false, after = false;
        for (int lit : C) {
            int v = std::abs(lit) - 1;
            bool val = assign[v];
            if (lit < 0) val = !val;
            if (val) before = true;

            if (v == var) val = !val;
            if (lit < 0) val = !val;
            if (val) after = true;
        }
        if (before && !after) count++;
    }
    return count;
}

// WalkSAT real
bool walksat(const SATInstance &inst, std::vector<int> &assign,
             int max_steps, std::mt19937 &rng) {
    std::uniform_int_distribution<> dist_var(0, inst.n_vars-1);
    std::uniform_real_distribution<> prob(0.0, 1.0);

    for (int step = 0; step < max_steps; step++) {
        int sat_now = evaluate(inst, assign);
        if (sat_now == inst.clauses.size()) return true;

        int v = dist_var(rng);

        if (prob(rng) < 0.5) {
            assign[v] = !assign[v];
        } else {
            int best_var = v;
            int best_bc = breakcount(inst, assign, v);
            for (int k = 0; k < 10; k++) {
                int x = dist_var(rng);
                int bc = breakcount(inst, assign, x);
                if (bc < best_bc) {
                    best_bc = bc;
                    best_var = x;
                }
            }
            assign[best_var] = !assign[best_var];
        }
    }

    return false;
}

// GSAT
bool gsat(const SATInstance &inst, std::vector<int> &assign,
          int max_steps, std::mt19937 &rng) {
    std::uniform_int_distribution<> dist_var(0, inst.n_vars-1);

    for (int step = 0; step < max_steps; step++) {
        int sat_now = evaluate(inst, assign);
        if (sat_now == inst.clauses.size()) return true;

        int best_var = -1;
        int best_gain = -999999;

        for (int v = 0; v < inst.n_vars; v++) {
            assign[v] = !assign[v];
            int new_sat = evaluate(inst, assign);
            int gain = new_sat - sat_now;
            assign[v] = !assign[v];

            if (gain > best_gain) {
                best_gain = gain;
                best_var = v;
            }
        }

        assign[best_var] = !assign[best_var];
    }
    return false;
}

// Simulated Annealing
bool anneal(const SATInstance &inst, std::vector<int> &assign,
            int max_steps, double T0, std::mt19937 &rng) {
    std::uniform_int_distribution<> dist_var(0, inst.n_vars-1);
    std::uniform_real_distribution<> prob(0.0, 1.0);

    double T = T0;

    for (int step = 0; step < max_steps; step++) {
        int sat_now = evaluate(inst, assign);
        if (sat_now == inst.clauses.size()) return true;

        int v = dist_var(rng);
        assign[v] = !assign[v];
        int sat_new = evaluate(inst, assign);

        if (sat_new < sat_now) {
            double p = std::exp((sat_new - sat_now) / T);
            if (prob(rng) > p) assign[v] = !assign[v];
        }

        T *= 0.995;
    }
    return false;
}

// Hybrid solver
py::dict solve_parallel(const SATInstance &inst, int max_steps, int threads) {
    omp_set_num_threads(threads);

    bool found = false;

    #pragma omp parallel shared(found)
    {
        std::mt19937 rng(omp_get_thread_num() + 123);

        std::vector<int> assign(inst.n_vars);
        for (int &x : assign) x = rng() % 2;

        if (!found)
            if (gsat(inst, assign, max_steps/3, rng))
                found = true;

        if (!found)
            if (walksat(inst, assign, max_steps/2, rng))
                found = true;

        if (!found)
            if (anneal(inst, assign, max_steps/3, 1.5, rng))
                found = true;
    }

    py::dict result;
    result["found"] = found;
    return result;
}

PYBIND11_MODULE(sat_backend, m) {
    py::class_<SATInstance>(m, "SATInstance")
        .def(py::init<int, std::vector<std::vector<int>>>())
        .def_readwrite("n_vars", &SATInstance::n_vars)
        .def_readwrite("clauses", &SATInstance::clauses);

    m.def("solve_parallel", &solve_parallel);
}




