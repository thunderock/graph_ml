#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <unordered_set>

class RandomWalkSampler {
public:
    RandomWalkSampler(const std::vector<int>& indptr,
                      const std::vector<int>& indices,
                      const std::vector<double>& data,
                      int walk_length = 40,
                      double p = 1,
                      double q = 1,
                      int padding_id = -1)
        : indptr(indptr), indices(indices), data(data), walk_length(walk_length), p(p), q(q), padding_id(padding_id)
    {
        weighted = (!std::all_of(data.begin(), data.end(), [](double d){ return std::abs(d - 1) < 1e-9; }));
        if (weighted) {
            std::vector<double> row_sums(indptr.size() - 1, 0.0);
            for (size_t i = 0; i < data.size(); ++i) {
                row_sums[i / (indptr[i + 1] - indptr[i])] += data[i];
            }
            for (size_t i = 0; i < data.size(); ++i) {
                data[i] /= row_sums[i / (indptr[i + 1] - indptr[i])];
            }
        }
    }

    std::vector<int> sampling(int start) {
        std::vector<int> start_vec = {start};
        return weighted ? _random_walk_weighted(start_vec)[0] : _random_walk(start_vec)[0];
    }

private:
    std::vector<int> indptr, indices;
    std::vector<double> data;
    int walk_length;
    double p, q;
    int padding_id;
    bool weighted;

    std::vector<std::vector<int>> _random_walk(const std::vector<int>& ts) {
        std::vector<std::vector<int>> walks(ts.size(), std::vector<int>(walk_length, padding_id));
        std::default_random_engine generator;
        std::uniform_real_distribution<double> distribution(0.0, 1.0);

        for (size_t walk_id = 0; walk_id < ts.size(); ++walk_id) {
            int t = ts[walk_id];
            walks[walk_id][0] = t;

            auto neighbors = _neighbors(t);
            if (neighbors.empty()) continue;

            walks[walk_id][1] = neighbors[distribution(generator) * neighbors.size()];
            for (int j = 2; j < walk_length; ++j) {
                neighbors = _neighbors(walks[walk_id][j - 1]);
                if (neighbors.empty()) break;

                if (p == 1 && q == 1) {
                    walks[walk_id][j] = neighbors[distribution(generator) * neighbors.size()];
                    continue;
                }

                while (true) {
                    int new_node = neighbors[distribution(generator) * neighbors.size()];
                    double r = distribution(generator);
                    if (new_node == walks[walk_id][j - 2]) {
                        if (r < 1 / p) break;
                    } else if (std::binary_search(neighbors.begin(), neighbors.end(), new_node)) {
                        if (r < 1) break;
                    } else if (r < 1 / q) break;
                }
            }
        }
        return walks;
    }

    std::vector<std::vector<int>> _random_walk_weighted(const std::vector<int>& ts) {
        std::vector<std::vector<int>> walks(ts.size(), std::vector<int>(walk_length, padding_id));
        std::default_random_engine generator;
        std::uniform_real_distribution<double> distribution(0.0, 1.0);

        for (size_t walk_id = 0; walk_id < ts.size(); ++walk_id) {
            int t = ts[walk_id];
            walks[walk_id][0] = t;

            auto neighbors = _neighbors(t);
            if (neighbors.empty()) continue;

            walks[walk_id][1] = neighbors[_weighted_choice(_neighbors_data(t), distribution(generator))];
            for (int j = 2; j < walk_length; ++j) {
                neighbors = _neighbors(walks[walk_id][j - 1]);
                if (neighbors.empty()) break;

                auto neighbors_p = _neighbors_data(walks[walk_id][j - 1]);
                if (p == 1 && q == 1) {
                    walks[walk_id][j] = neighbors[_weighted_choice(neighbors_p, distribution(generator))];
                    continue;
                }

                while (true) {
                    int new_node = neighbors[_weighted_choice(neighbors_p, distribution(generator))];
                    double r = distribution(generator);
                    if (new_node == walks[walk_id][j - 2]) {
                        if (r < 1 / p) break;
                    } else if (std::binary_search(neighbors.begin(), neighbors.end(), new_node)) {
                        if (r < 1) break;
                    } else if (r < 1 / q) break;
                }
            }
        }
        return walks;
    }

    std::vector<int> _neighbors(int t) {
        return std::vector<int>(indices.begin() + indptr[t], indices.begin() + indptr[t + 1]);
    }

    std::vector<double> _neighbors_data(int t) {
        return std::vector<double>(data.begin() + indptr[t], data.begin() + indptr[t + 1]);
    }

    size_t _weighted_choice(const std::vector<double>& weights, double rand_val) {
        double cum_sum = 0.0;
        for (size_t i = 0; i < weights.size(); ++i) {
            cum_sum += weights[i];
            if (rand_val <= cum_sum) return i;
        }
        return weights.size() - 1;
    }
};

int main() {
    // Example usage
    std::vector<int> indptr = {0, 2, 5, 7};
    std::vector<int> indices = {1, 2, 0, 2, 3, 0, 1};
    std::vector<double> data = {0.5, 0.5, 0.3, 0.4, 0.3, 0.6, 0.4};

    RandomWalkSampler sampler(indptr, indices, data);
    auto walk = sampler.sampling(0);

    for (int node : walk) {
        std::cout << node << " ";
    }
    std::cout << std::endl;

    return 0;
}
