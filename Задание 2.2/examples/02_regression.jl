using LinearAlgebra, Statistics
x = collect(0.0:4.0)
y = [1.0, 3.0, 5.0, 7.0, 9.0]
X = hcat(ones(length(x)), x)
beta = X \ y
predicted = X * beta
mse = mean((predicted .- y).^2)
@assert isapprox(beta, [1.0, 2.0]; atol=1e-12)
@assert mse < 1e-24
println((coefficients=beta, mse=mse))
