# Warning:WIP!

# CLOP - C with a Lot Of Parentheses

CLOP is a s-expressions to C transpiler, written in Python3. It is not what provides a full LISP environment on the top of C, but just a bunch of syntax sugar.

## Requirements

- Python3.5+
- gcc (or any C compiler)

## Installation

First, clone this repo

```
$ git clone https://github.com/koji-kojiro/clop.git
```

Then, run seup.py

```
$ cd clop
$ python setup.py install
```

## Usage

```
$ clop --help
usage: clop [-h|-v] [command] [options] file

optional arguments:
  -h, --help      show this help message and exit
  -v, --version   show version info and exit

commands:
  run, translate
```

for more detailed information, try `clop [command] --help`.

## Example

```lisp
(include stdio)

(defun int:main (int:argc char*:argv[])
  (let ((int:i 0))
    (while (< (incf i) argc)
      (printf "%s\n" (aref argv i))))
  (return 0))
```

The code above is translated as follows:

```
$ clop translate src.clop --out dst.c
```

```c
#include <stdio.h>

int main (int argc, char* argv[])
{
  ({
    int i = 0;
    while (++i < argc) 
      printf("%s\n", argv[i]);
  });
  return 0;
}
```

Or, you can run the source directly.

```
$ clop run src.clop --args="a b c"
a
b
c
```

More examples can be found [here](./example).

## License
CLOP is distributed under MIT License.

## Author
[TANI Kojiro](github.com/koji-kojiro)(kojiro0531@gmail.com)
