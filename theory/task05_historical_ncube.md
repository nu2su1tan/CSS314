# Task 05: The nCUBE Experiment and "Amdahl's Pessimism"

Note: the numbers about the original experiment are given from general knowledge of the 1988 papers. Check the exact values against the sources listed at the end before you submit.

## Background

By the 1980s, many people used Amdahl's Law to argue that massively parallel computers were not worth building. The argument went like this: even a small serial part limits the speedup. If only 1% of a program is serial, the speedup can never pass 100. So why build a machine with 1,000 processors?

## The experiment

At Sandia National Laboratories, John Gustafson, Gary Montry and Robert Benner ran real scientific programs on an nCUBE 10 hypercube computer with 1,024 processors. They tested three applications:

1. Beam stress analysis (structural mechanics)
2. Surface wave simulation (wave motion)
3. Unstable fluid flow (computational fluid dynamics)

They measured the serial fraction on the parallel machine. It was small: about 0.4% to 0.8% of the run time.

They reported speedups of about 1,000 on 1,024 processors (roughly 1,009 to 1,020, depending on the application).

## Why this looked impossible under Amdahl's Law

Take a serial fraction of 0.4% (`s = 0.004`).

Amdahl's ceiling is:

```
1 / s = 1 / 0.004 = 250
```

And for P = 1,024:

```
S = 1 / (0.004 + 0.996 / 1024)
  = 1 / (0.004 + 0.000973)
  = 1 / 0.004973
  = about 201
```

So Amdahl predicts at most about 201, and never more than 250. The measured speedup was more than 1,000. This looked like a contradiction.

## How problem expansion removes the ceiling

The team did not run the same problem on 1,024 processors and compare it with 1 processor. They did this instead:

- They made the problem bigger when they used more processors. For example, they used a finer grid, so each processor kept a similar amount of work.
- The serial part (setup, input, small control code) did not grow much with the grid size.
- The parallel part (grid computation) grew almost in proportion to the number of processors.

So the serial fraction measured on the 1,024-processor machine was 0.4%, but this is the *scaled* fraction `alpha`. We apply Gustafson's formula:

```
S = P - alpha * (P - 1)
  = 1024 - 0.004 * 1023
  = 1024 - 4.09
  = about 1,020
```

With `alpha = 0.008`:

```
S = 1024 - 0.008 * 1023 = 1024 - 8.18 = about 1,016
```

These match the measured results (about 1,000 or more). The formula explains the data.

## Why Amdahl's number was misleading

Amdahl's `s = 0.004` was treated as a fixed property of the program. But the serial *share* depends on problem size. When the problem grows, the serial share on one processor becomes tiny (see Task 03):

```
s' = alpha / (alpha + (1 - alpha) * P)
   = 0.004 / (0.004 + 0.996 * 1024)
   = about 0.0000039
```

So the "real" Amdahl serial fraction for the scaled problem is about 0.0004%, not 0.4%. With that value, Amdahl's formula also predicts about 1,020. The ceiling of 250 only applied to the small, fixed-size problem.

## Lessons

1. A speedup limit depends on how the problem size changes. It is not a law of nature for the program.
2. Measure the serial fraction on the machine and problem size you really use.
3. Parallel machines are useful because they let us solve bigger problems, not only because they solve old problems faster.
4. This does not make Amdahl wrong. It makes it the right tool for fixed-size problems only.

## Sources to check

- J. L. Gustafson, "Reevaluating Amdahl's Law", *Communications of the ACM*, 31(5), 1988.
- J. L. Gustafson, G. R. Montry, R. E. Benner, "Development of Parallel Methods for a 1024-Processor Hypercube", *SIAM Journal on Scientific and Statistical Computing*, 9(4), 1988.
