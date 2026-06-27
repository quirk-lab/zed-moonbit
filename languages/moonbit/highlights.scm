; Fallback generic identifiers
(lowercase_identifier) @variable
(identifier) @variable

; Keywords
"fn" @keyword.function
[ "let" "mut" "pub" "priv" "readonly" "const" "extern" "async" "defer" "guard" "using" "open" ] @keyword.modifier
[ "if" "else" "match" "while" "for" "in" "return" "break" "continue" "loop" "try" "catch" "raise" ] @keyword.control
[ "struct" "enum" "trait" "type" "typealias" "traitalias" "fnalias" "impl" "with" ] @keyword.type

; Builtin Types
((type_identifier) @type.builtin
 (#any-of? @type.builtin "Int" "Int64" "UInt" "UInt64" "Float" "Double" "Bool" "String" "Char" "Unit" "Byte" "Bytes" "BigInt"))

; Types
(qualified_type_identifier
  (package_identifier) @variable.parameter)
(qualified_type_identifier
  (identifier) @type)
(qualified_type_identifier
  (dot_identifier) @type)

(type_identifier) @type

; Constructors
(uppercase_identifier) @constructor

; Functions (Definition)
(function_definition
  (function_identifier
    (lowercase_identifier) @function))

(trait_method_declaration
  (function_identifier) @function)

(impl_definition
  (function_identifier) @function)

; Function Calls
(apply_expression
  (qualified_identifier
    (lowercase_identifier) @function.call))

(apply_expression
  (qualified_identifier
    (dot_lowercase_identifier) @function.call))

; Method Calls via dot syntax (e.g. rand.uint64)
(dot_apply_expression
  (dot_identifier
    (dot_lowercase_identifier) @function.method))

; Static Method Calls (e.g. Rand::new)
(apply_expression
  (method_expression
    (lowercase_identifier) @function.method))

; Properties and Fields
(access_expression
  (accessor
    (dot_identifier
      (dot_lowercase_identifier) @property)))

(struct_field_declaration
  (lowercase_identifier) @property)

(labeled_expression
  (lowercase_identifier) @property)

(labeled_expression_pun
  (lowercase_identifier) @property)

; Arguments passed to calls (Lilla / Purple)
(argument
  (qualified_identifier
    (lowercase_identifier) @variable.special))

(labelled_argument
  (qualified_identifier
    (lowercase_identifier) @variable.special))

; Parameters (Definition)
[
  (positional_parameter (lowercase_identifier) @variable.parameter)
  (labelled_parameter (label (lowercase_identifier) @variable.parameter))
  (optional_parameter (optional_label (lowercase_identifier) @variable.parameter))
]

(optional_parameter_with_default (label (lowercase_identifier) @variable.parameter))
(optional_parameter_with_default (optional_label (lowercase_identifier) @variable.parameter))

; Nominal/Labelled arguments labels (e.g., limit=100) -> Verdino / Green
(labelled_argument
  . (lowercase_identifier) @variable.parameter)

(optional_argument
  . (optional_label (lowercase_identifier) @variable.parameter))

; Self-like parameters (Lilla / Purple)
(positional_parameter
  (lowercase_identifier) @variable.special
  (#match? @variable.special "^_?self$"))

; Let bindings
[
  (let_expression (lowercase_identifier) @variable)
  (let_mut_expression (lowercase_identifier) @variable)
  (letrec_expression (lowercase_identifier) @variable)
]

; Constants
(const_definition
  (uppercase_identifier) @constant)

; Namespace / module-like paths (Verdino / Green, as requested)
(package_identifier) @variable.parameter

; Literals
(boolean_literal) @boolean
(integer_literal) @number
(float_literal) @number
(double_literal) @number
(string_literal) @string
(multiline_string_literal) @string
(char_literal) @string
(byte_literal) @number
(bytes_literal) @string
(escape_sequence) @string.escape
(regex_literal) @string.special
(string_interpolation) @embedded

; Special strings in foreign bindings
(external_linkage
  (string_literal) @string.special)

(external_source
  [
    (string_literal)
    (multiline_string_literal)
  ] @string.special)

; Comments
((comment) @comment.doc
 (#match? @comment.doc "^///"))

(comment) @comment
(block_comment) @comment

; Brackets
[ "{" "}" "[" "]" "(" ")" ] @punctuation.bracket

; Delimiters
[ "," "." ":" ";" "::" "->" "=>" ] @punctuation.delimiter

; Operators
[
  "+" "-" "*" "/" "%" "==" "!=" "<" "<=" ">" ">=" "&&" "||" "!"
  "=" "+=" "-=" "*=" "/=" "|>" "<+" "<?"
] @operator
