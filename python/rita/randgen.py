"""
randgen.py - Seeded random number generator for RiTa

Implements Mersenne Twister PRNG for reproducible randomness
"""

import time
from typing import List, Union, Callable, Optional, Any
from rita.util import Util

class RandGen:
    """
    Seeded random number generator using Mersenne Twister algorithm

    Provides reproducible randomness for testing and generative applications.
    See: https://en.wikipedia.org/wiki/Mersenne_Twister
    """

    # Mersenne Twister constants
    N = 624
    M = 397
    MATRIX_A = 0x9908b0df
    UPPER_MASK = 0x80000000
    LOWER_MASK = 0x7fffffff

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize random generator

        Args:
            seed: Initial seed value (uses current time if None)
        """
        self.mt = [0] * self.N
        self.mti = self.N + 1

        if seed is None:
            seed = int(time.time() * 1000)
        self.seed(seed)

    def seed(self, num: int):
        """
        Seed the random number generator

        Args:
            num: Seed value (integer)
        """
        self.mt[0] = num & 0xffffffff

        for i in range(1, self.N):
            s = self.mt[i - 1] ^ (self.mt[i - 1] >> 30)
            self.mt[i] = (((((s & 0xffff0000) >> 16) * 1812433253) << 16) +
                         (s & 0x0000ffff) * 1812433253) + i
            self.mt[i] &= 0xffffffff

        self.mti = self.N

    def shuffle(self, arr: List) -> List:
        """
        Shuffle array using Fisher-Yates algorithm

        Args:
            arr: List to shuffle

        Returns:
            New shuffled list (original unchanged)
        """
        new_array = arr.copy()
        length = len(new_array)
        i = length

        while i > 0:
            i -= 1
            p = int(self.random(length))
            new_array[i], new_array[p] = new_array[p], new_array[i]

        return new_array

    def random_ordering(self, arg: Union[List, int]) -> List:
        """
        Generate random permutation of array or range

        Args:
            arg: Either a list to shuffle or an integer (returns shuffled range(n))

        Returns:
            Shuffled list
        """
        if not (isinstance(arg, list) or Util.is_num(arg)):
            raise ValueError('Expects list or int')

        ordering = arg.copy() if isinstance(arg, list) else list(range(int(arg)))

        # Fisher-Yates shuffle
        for i in range(len(ordering) - 1, 0, -1):
            j = int(self.random() * (i + 1))
            ordering[i], ordering[j] = ordering[j], ordering[i]

        return ordering

    def pselect(self, probs: List[float]) -> int:
        """
        Select index from normalized probability distribution

        Args:
            probs: List of probabilities (must sum to 1.0)

        Returns:
            Selected index
        """
        if not probs:
            raise ValueError('Probabilities required')

        point = self._rndf()
        cutoff = 0.0

        for i in range(len(probs) - 1):
            cutoff += probs[i]
            if point < cutoff:
                return i

        return len(probs) - 1

    def pselect2(self, weights: List[float]):
        """
        Select a value from weights using weighted random selection.
        Weights do NOT need to sum to 1 — they are used directly as relative weights.

        Args:
            weights: List of weights (treated as un-normalized probabilities)

        Returns:
            The selected value (not index)
        """
        total = sum(weights)
        rand = self._rndf() * total
        for ele in weights:
            rand -= ele
            if rand < 0:
                return ele
        return weights[-1]

    def ndist(self, weights: List[float], temp: Optional[float] = None) -> List[float]:
        """
        Normalize weights to probability distribution (sum to 1.0)

        If temperature is provided, applies softmax transformation.

        Args:
            weights: List of positive weights
            temp: Temperature parameter (0 < temp < inf)
                  Lower values favor highest weight
                  Higher values even out probabilities

        Returns:
            Normalized probability distribution
        """
        import math

        probs = []
        total = 0.0

        if temp is None:
            # Simple normalization
            for w in weights:
                if w < 0:
                    raise ValueError('Weights must be positive')
                probs.append(w)
                total += w
        else:
            # Softmax with temperature
            if temp < 0.01:
                temp = 0.01

            for w in weights:
                pr = math.exp(w / temp)
                probs.append(pr)
                total += pr

        # Normalize to sum to 1.0
        return [p / total for p in probs]

    def random(self, *args) -> Union[float, Any]:
        """
        Generate random value

        Usage:
            random() -> float in [0, 1)
            random(k) -> float in [0, k)
            random(j, k) -> float in [j, k)
            random(arr) -> random item from arr

        Returns:
            Random value based on arguments
        """
        rand = self._rndf()

        if not args:
            return rand

        if isinstance(args[0], list):
            arr = args[0]
            return arr[int(rand * len(arr))]

        if len(args) == 1:
            return rand * args[0]

        return rand * (args[1] - args[0]) + args[0]

    def random_bias(self, min_val: float, max_val: float,
                    bias: float, influence: float = 0.5) -> float:
        """
        Generate random value centered around bias

        Args:
            min_val: Minimum value
            max_val: Maximum value
            bias: Center point of distribution
            influence: How close result is to bias (0-1)

        Returns:
            Biased random value
        """
        base = self._rndf() * (max_val - min_val) + min_val
        mix = self._rndf() * influence
        return base * (1 - mix) + bias * mix

    # Internal methods

    def _rndi(self) -> int:
        """Generate random 32-bit integer"""
        mag01 = [0x0, self.MATRIX_A]

        if self.mti >= self.N:
            if self.mti == self.N + 1:
                self.seed(5489)

            kk = 0
            while kk < self.N - self.M:
                y = (self.mt[kk] & self.UPPER_MASK) | (self.mt[kk + 1] & self.LOWER_MASK)
                self.mt[kk] = self.mt[kk + self.M] ^ (y >> 1) ^ mag01[y & 0x1]
                kk += 1

            while kk < self.N - 1:
                y = (self.mt[kk] & self.UPPER_MASK) | (self.mt[kk + 1] & self.LOWER_MASK)
                self.mt[kk] = self.mt[kk + (self.M - self.N)] ^ (y >> 1) ^ mag01[y & 0x1]
                kk += 1

            y = (self.mt[self.N - 1] & self.UPPER_MASK) | (self.mt[0] & self.LOWER_MASK)
            self.mt[self.N - 1] = self.mt[self.M - 1] ^ (y >> 1) ^ mag01[y & 0x1]

            self.mti = 0

        y = self.mt[self.mti]
        self.mti += 1

        # Tempering
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9d2c5680
        y ^= (y << 15) & 0xefc60000
        y ^= (y >> 18)

        return y & 0xffffffff

    def _rndf(self) -> float:
        """Generate random float in [0, 1)"""
        return self._rndi() * (1.0 / 4294967296.0)

# For backwards compatibility / convenience
SeededRandom = RandGen
