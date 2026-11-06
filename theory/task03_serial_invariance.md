# Task 03: The Serial Fraction and the Frame of Reference

## The apparent paradox

- Amdahl says: a small serial fraction `s` puts a hard limit on speedup (`1/s`).
- Gustafson says: a small serial fraction `alpha` still allows speedup close to P.

Both use "a serial fraction". Yet one predicts a ceiling and the other predicts no ceiling. How can this be?

## The answer: the two fractions are measured in different places

| | Amdahl's `s` | Gustafson's `alpha` |
|---|---|---|
| Measured on | One processor | The P-processor machine |
| Problem size | The original, fixed size | The scaled-up size |
| Meaning | Share of the one-processor run time that is serial | Share of the parallel run time that is serial |

These are two different numbers for the same program. We show how they relate.

## Step 1: Define the times

On the parallel machine, with a scaled problem:

- serial part takes time `t_s`
- parallel part takes time `t_p`

Serial fraction measured on the parallel machine:

```
alpha = t_s / (t_s + t_p)
```

## Step 2: Time on one processor for the same scaled problem

One processor must do all the parallel work alone. That takes `P * t_p`.

```
T_1 = t_s + P * t_p
```

Serial fraction measured on one processor (call it `s'`):

```
s' = t_s / (t_s + P * t_p)
```

## Step 3: Express s' using alpha

Divide the top and bottom by `(t_s + t_p)`:

```
s' = alpha / (alpha + (1 - alpha) * P)
```

Look at this number. For `alpha = 0.05` and `P = 1000`:

```
s' = 0.05 / (0.05 + 0.95 * 1000) = 0.05 / 950.05 = 0.0000526
```

So the serial fraction seen on one processor is tiny: about 0.005%. It shrinks as P grows.

## Step 4: Put s' into Amdahl's formula

Let `D = alpha + (1 - alpha) * P`. Then:

```
s'        = alpha / D
1 - s'    = (1 - alpha) * P / D
```

Amdahl's denominator is:

```
s' + (1 - s') / P = alpha / D + (1 - alpha) / D
                  = (alpha + 1 - alpha) / D
                  = 1 / D
```

So:

```
S_Amdahl = 1 / (1 / D) = D = alpha + (1 - alpha) * P = P - alpha * (P - 1)
```

This is exactly Gustafson's formula.

## What this means

1. **The two laws agree.** Amdahl's formula, applied to the scaled problem with the correct `s'`, gives Gustafson's answer.
2. **The "contradiction" is only a different frame of reference.** Amdahl's `s` is a property of one fixed-size problem. When the problem grows, the serial time (setup, I/O, small control code) stays almost the same, but the parallel work gets much bigger. So the serial share of the one-processor run time shrinks. A big `s'` at small size becomes a tiny `s'` at large size.
3. **Why serial overhead does not stop scaling.** In the scaled run, the serial part takes a fixed share `alpha` of the wall time, and the extra processors fill the rest of the time with useful work. The serial part costs us a loss of about `alpha * (P - 1)` processors' worth of work, which is small compared to P when `alpha` is small.

## Where the model is weak

Measuring `alpha` on the parallel machine is practical, because that is where we run the program. But the model assumes the serial time stays constant when the problem grows. In real programs, serial work often grows too (for example, reading bigger input files, or collecting more results). Then `alpha` is not constant, and the speedup is lower than Gustafson predicts. Task 12 looks at this.
