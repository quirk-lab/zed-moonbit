; Functions
(function_definition
  "fn" @context
  (function_identifier) @name
  (parameters
    (parameter
      (lowercase_identifier)
      (type_annotation
        (type))?)*)? @context.extra
  (return_type)? @context.extra
  (docstring)? @annotation) @item

; Structs
(struct_definition
  "struct" @context
  (identifier) @name
  (attributes)? @annotation
  (struct_field_declaration)*) @item

; Enums
(enum_definition
  "enum" @context
  (identifier) @name
  (attributes)? @annotation
  (enum_constructor)*) @item

; Traits
(trait_definition
  "trait" @context
  (identifier) @name
  (attributes)? @annotation
  (trait_method_declaration)*) @item

; Constants
(const_definition
  "const" @context
  (uppercase_identifier) @name
  (attributes)? @annotation
  (type_annotation)? @context.extra) @item

; Type definitions
(type_definition
  "type" @context
  (identifier) @name
  (attributes)? @annotation) @item

; Test functions
(test_definition
  "test" @context
  [(string_literal) @name
   (docstring) @annotation]?) @item

; Implementation blocks
(impl_definition
  "impl" @context
  (type_name
    (qualified_type_identifier) @context)
  "with" @context
  (function_identifier) @name
  (parameters)? @context.extra
  (return_type)? @context.extra) @item
