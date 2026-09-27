using LinearAlgebra
A = [3.0 1.0; 1.0 2.0]
b = [9.0, 8.0]
x = A \ b
@assert isapprox(x, [2.0, 3.0]; atol=1e-12)
@assert norm(A * x - b) < 1e-12
println(x)
