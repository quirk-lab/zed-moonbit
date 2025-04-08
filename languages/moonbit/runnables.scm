; Main function detection
(
  (function_definition
    "fn"
    (function_identifier
      (lowercase_identifier) @run
      (#eq? @run "main")
    )
  )
  (#set! tag "moon-run")
)

; Test function detection
(
  (test_definition
    "test"
    (string_literal)? @run
    (parameters)?
    (block_expression)
  )
  (#set! tag "moon-test")
)
