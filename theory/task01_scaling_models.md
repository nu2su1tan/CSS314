# Task 01: Strong Scaling vs. Weak Scaling

## Summary

Amdahl (1967) and Gustafson (1988) ask two different questions.

- **Amdahl:** "I have one problem. How much faster can I solve it with more processors?"
- **Gustafson:** "I have more processors. How much bigger a problem can I solve in the same time?"

## Amdahl's assumptions (fixed-size, strong scaling)

- The problem size stays the same when P grows.
- A fraction `s` of the work is serial. The rest, `1 - s`, is parallel.
- Only the parallel part gets faster when we add processors.

```
S_Amdahl(P) = 1 / (s + (1 - s) / P)
```

As P goes to infinity:

```
S_Amdahl(P) -> 1 / s
```

So the speedup has a hard ceiling. If `s = 0.05`, the speedup can never pass 20, even with a million cores.

**Problem size as P grows:** constant. We cut the same work into smaller and smaller pieces.

## Gustafson's assumptions (fixed-time, weak scaling)

- The run time stays the same when P grows.
- When we get more processors, we use them to solve a bigger problem.
- The parallel part of the work grows with P. The serial part stays about the same size.

```
S_Gustafson(P) = P - alpha * (P - 1)
```

As P goes to infinity, the speedup keeps growing linearly with P. There is no ceiling. The slope is `1 - alpha`.

**Problem size as P grows:** grows about in proportion to P (for the parallel part).

## Why the names "fixed-size" and "fixed-time"

| | Amdahl | Gustafson |
|---|---|---|
| What stays fixed | Problem size | Run time |
| What changes | Run time (gets shorter) | Problem size (gets bigger) |
| Also called | Strong scaling | Weak scaling |
| Speedup limit | 1 / s | None (grows with P) |
| Typical question | "How fast can I finish this job?" | "How big a job can I finish in an hour?" |

## The real difference: what we want from a bigger machine

In real science and engineering, people rarely want the same answer faster. They want a better answer in the same time. Examples: a finer weather grid, more particles in a simulation, more Monte Carlo samples. For this kind of work, Gustafson's view matches reality.

Amdahl's view fits jobs where the size is fixed by the task itself. Examples: one image to encode, one query to answer, one real-time deadline.

## The key point

The two laws do not disagree about math. They describe two different ways to use a parallel machine. Both are correct for their own setup. The mistake is to use Amdahl's limit on a problem that will grow when more cores are available.
