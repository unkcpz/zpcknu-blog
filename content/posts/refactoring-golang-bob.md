+++
title =  "Refactoring Golang Bob"
Description = ""
Tags = []
Categories = []
date = 2018-03-10T12:04:29+08:00
+++

## version1

首先确定所要构造的函数，和函数的类型。
```go
// file: primes.go
// package primes generate prime numbers
package primes

func generatePrimes(m int) []int {
	_ = m
	return []int{1, 2}
}
```

创建函数测试。
```go
// file: primes_test.go
package primes

import (
	"testing"
)

func TestGeneratePrimes(t *testing.T) {
	var tests = []struct {
		input    int
		wantLen  int
		wantLast int
	}{
		{2, 1, 2},
		{3, 2, 3},
		{4, 2, 3},
		{100, 25, 97},
	}
	for _, test := range tests {
		got := generatePrimes(test.input)
		if len(got) != test.wantLen {
			t.Errorf("length of generatePrimes(%d) is %d, want %d.\n", test.input,
				len(got), test.wantLen)
		}
		if lastEle := got[len(got)-1]; lastEle != test.wantLast {
			t.Errorf("Last element of generatePrimes(%d) is %d, want %d.\n",
				test.input, lastEle, test.wantLast)
		}
	}

	for i := 0; i < 2; i++ {
		got := len(generatePrimes(i))
		if got != 0 {
			t.Errorf("length of generatePrimes(%d) is %d, want %d\n", i, got, 0)
		}
	}
}
```

修改函数，使其能够通过测试。
```go
// file: primes.go
// package primes generate prime numbers
package primes

import "math"

func generatePrimes(m int) []int {
	if m < 2 {
		return []int{}
	} else {
		var sieve = make([]bool, m+1)
		for i, _ := range sieve {
			sieve[i] = true
		}
		sieve[0], sieve[1] = false, false

		for i := 2; float64(i) < math.Sqrt(float64(m))+1; i++ {
			for j := 2 * i; j < m+1; j += i {
				sieve[j] = false
			}
		}

		var result []int
		for i, b := range sieve {
			if b {
				result = append(result, i)
			}
		}
		return result
	}
}
```

## version2
显然能够把全部功能变成3个分离的功能。

1. 对变量进行初始化。
2. 执行核心的过滤个哦难做。
3. 把过滤后的结果存放到一个`[]int`类型的slice中。

不同与Bob书中的java实例，1,2功能合并在一起使得go程序更加紧凑。
```go
// file: primes.go
func GeneratePrimes(m int) []int {
	if m < 2 {
		return []int{}
	}
	p := sieve(m)
	return loadPrimes(p)
}

func sieve(m int) []bool {
  // initialize
	var sieve = make([]bool, m+1)
	for i := 2; i < len(sieve); i++ {
		sieve[i] = true
	}

	for i := 2; float64(i) < math.Sqrt(float64(m))+1; i++ {
		for j := 2 * i; j < m+1; j += i {
			sieve[j] = false
		}
	}
	return sieve
}

func loadPrimes(sieve []bool) []int {
	result := make([]int, 0, len(sieve))
	for i, b := range sieve {
		if b {
			result = append(result, i)
		}
	}
	return result
}
```

### version3
函数名和变量名不能清晰的反应作用，比如存放prime的`[]bool`叫做`isPrime`更合适。sieve和
loadPrimes分别改为`crossOutMultiples`和`putPrimesIntoResult`。
同时，加入一个解释为何只需遍历到slice长度的平方根。这引导我把计算部分提取出来放到一个独立的
函数中。这个处理使得我们意外获得了一个无需类型转换的调用。修改后的代码如下：

```go
// file: primes.go
// package primes generate prime numbers
package primes

import (
	"math"
)

func GeneratePrimes(maxValue int) []int {
	if maxValue < 2 {
		return []int{}
	}
	isPrime := crossOutMultiples(maxValue)
	return putPrimesIntoResult(isPrime)
}

func crossOutMultiples(m int) []bool {
	// initialize
	var isPrime = make([]bool, m+1)
	for i := 2; i < len(isPrime); i++ {
		isPrime[i] = true
	}

	for i := 2; i < calcMaxPrimeFactor(m); i++ {
		for j := 2 * i; j < len(isPrime); j += i {
			isPrime[j] = false
		}
	}
	return isPrime
}

func calcMaxPrimeFactor(maxValue int) int {
	// We cross out all multiples of p; where p is prime.
	// Thus, all crossed out multiples have p and q for
	// factors. If p > sqrt of the size of the array , then
	// q will never be greater than 1. Thus p is the
	// largest prime factor in the array , and is also
	// the iteration limit.
	var maxFactor float64 = math.Sqrt(float64(maxValue)) + 1
	return int(maxFactor)
}

func putPrimesIntoResult(isPrime []bool) []int {
	result := make([]int, 0, len(isPrime))
	for i := 2; i < len(isPrime); i++ {
		if isPrime[i] {
			result = append(result, i)
		}
	}
	return result
}
```

### version4
简单的测试不能使我放心。所以我另外编写了测试，用来检查在2～500之间所产生的素数
列表中没有倍数的存在。新的测试通过了，减轻了我的恐惧。

```go
// file: primes_test.go
func TestPrimeExhaustive(t *testing.T) {
	for i := 2; i < 501; i++ {
		verifyPrimeList(t, GeneratePrimes(i))
	}
}

func verifyPrimeList(t *testing.T, pList []int) {
	for _, p := range pList {
		verifyPrime(t, p)
	}
}

func verifyPrime(t *testing.T, n int) {
	for i := 2; i < n; i++ {
		if n%i == 0 {
			t.Errorf("verify %d as prime, but %d %% %d == 0", n, n, i)
		}
	}
}
```
