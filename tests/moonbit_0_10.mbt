trait Logger {
  fn[X : Show] write_object(Self, X) -> Unit
}

impl Logger for StringBuilder with fn[X] write_object(self, x : X) {
  self.write_string(x.to_string())
}

fn moonbit_0_10_syntax(logger : Option[StringBuilder]) {
  let xs = ["cd", "ef"]
  let nested = "ab\{xs.join(";")}"

  let buf = StringBuilder()
  buf <+ "<ul prop=foo>"
  logger <? "[tag] message \{nested}"

  for i in 0..<10; p1 = 1, p2 = 0 {
    println("fib#\{i + 1} = \{p1}")
  }

  let fibs = [
    for _ in 0..<10; p1 = 1, p2 = 0; p1 = p1 + p2, p2 = p1 => {
      p1
    }
  ]
  ignore(fibs)
}
