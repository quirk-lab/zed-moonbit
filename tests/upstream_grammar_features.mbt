///|
/// MoonBit 0.10.4 syntax coverage supported by the pinned Tree-sitter grammar.

trait Render {
  fn render(Self) -> String
}

struct Task {
  title : String
}

impl Render for Task with fn render(self) {
  "Task(\{self.title})"
}

///|
/// Explicit trait method extension.
extend Task with Render::{render}

enum Coordinate {
  Point(Int, Int)
  Origin
}

///|
/// Or-pattern with one default binding.
fn option_or_default(value : Int?) -> Int {
  match value {
    Some(number) | None with number = 0 => number
  }
}

///|
/// Or-pattern with multiple default bindings.
fn coordinate_values(value : Coordinate) -> (Int, Int) {
  match value {
    Point(x, y) | Origin with x = 0, y = 0 => (x, y)
  }
}

///|
/// Conditional spread.
fn conditional_spread(include_extra : Bool) -> Array[Int] {
  let extra = [3, 4]
  [1, 2, ..if include_extra { extra }, 5]
}

///|
/// Basic lexscan.
fn scan_line(source) {
  lexscan source {
    (re"\r?\n", before=line, after=_) => line
    _ => source
  }
}

///|
/// Longest-match lexscan.
fn scan_longest(source) {
  lexscan source with longest {
    ((re"if" | re"else") as keyword, before=prefix, after~) => prefix
    re"[0-9]+" => ()
    re"[a-z]+" => ()
    _ => ()
  }
}

fn main {
  let task = Task::{ title: "Update Zed extension" }
  println(task.render())

  println(option_or_default(None))

  let (x, y) = coordinate_values(Origin)
  println("origin=(\{x}, \{y})")

  println(conditional_spread(true))
}