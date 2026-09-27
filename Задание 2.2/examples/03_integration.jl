function trapezoid(f, a, b, n::Integer)
    n > 0 || throw(ArgumentError("n must be positive"))
    h = (b - a) / n
    s = (f(a) + f(b)) / 2
    for i in 1:(n - 1)
        s += f(a + i * h)
    end
    return h * s
end
value = trapezoid(x -> x^2, 0.0, 1.0, 1000)
@assert abs(value - 1/3) < 2e-7
println(value)
