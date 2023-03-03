# good_enough_good_enough_golvers

Python port of [https://github.com/islemaster/good-enough-golfers].

Slower than the original with a normal python distribution.
Faster than the javascript version when using [https://www.pypy.org/].

Only implemented with python standard library features.

## Usage

```python
from GeneticSolver import GeneticSolver

solver = GeneticSolver(
    numberOfGroups=5, sizeOfGroups=5, numberOfRounds=5)
result = solver.solve()
print(result)
```
## Modifications to the algorithm

### Calculation of mutated group scores
Instead of calculating the sum of the weights for each pair inside a group the score is calculated
by using the score of the ancestor.

Since we only swap one element, we can subtract the weights for all pairs of the member swapped out.
Then we add the weights for all pairs containing the member that is swapped in.

This should make the loop for group scores faster for larger groups (group size n) yields a loop size of: 
```
2(n-1) vs n(n-1)/2
```

### Calculation of pow(weights,2)
The square of the weights are save during each weight calculation, as this value is used to calculate the score
for each group. This uses more memory, but the calculation of the square is only done once per round, instead of
twice every mutation.

## TODO
- [ ] implement avoided and discouraged pairings
- [ ] return the sum of all weights for each pair in each group. (this would be an more usefull indicator than the returned round score )




