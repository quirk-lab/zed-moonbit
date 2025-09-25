; Functions
((comment)* @annotation
  .
  (function_definition
    (attributes)? @annotation
    (visibility)? @context
    (external_linkage
      "extern" @context
      (string_literal)? @context.extra)?
    "async"? @context
    "fn" @context
    (function_identifier) @name
      (parameters)? @context.extra
      (return_type)? @context.extra)) @item

; Function alias
(function_alias_definition
  (attributes)? @annotation
  (visibility)? @context
  "fnalias" @context
  (function_alias_targets) @name) @item

; Structs
(struct_definition
  (attributes)? @annotation
  (visibility)? @context
  "struct" @context
  (identifier) @name
  (type_parameters)? @context
  (struct_field_declaration)*) @item

; Enums
(enum_definition
  (attributes)? @annotation
  (visibility)? @context
  "enum" @context
  (identifier) @name
  (type_parameters)? @context) @item

; Traits
(trait_definition
  (attributes)? @annotation
  (visibility)? @context
  "trait" @context
  (identifier) @name
  (trait_method_declaration)*) @item

; Trait alias
(trait_alias_definition
  (attributes)? @annotation
  (visibility)? @context
  "traitalias" @context
  (trait_alias_targets) @name) @item

; Constants
(const_definition
  (attributes)? @annotation
  (pub)? @context
  "const" @context
  (uppercase_identifier) @name
  (type_annotation)? @context.extra) @item

; Type definitions
(type_definition
  (attributes)? @annotation
  (visibility)? @context
  "extern"? @context
  "type" @context
  (identifier) @name) @item

; Error type definitions
(error_type_definition
  (attributes)? @annotation
  (visibility)? @context
  "extern"? @context
  ["suberror" ("type" "!")]? @context
  (identifier) @name) @item

; Type alias
(type_alias_definition
  (attributes)? @annotation
  (visibility)? @context
  "typealias" @context
  (type_alias_targets) @name) @item

; Test functions
((comment)* @annotation
  .
  (test_definition
    (attributes)? @annotation
    "test" @context
    (string_literal)? @name
    (parameters)? @context.extra)) @item

; Implementation blocks
(impl_definition
  (attributes)? @annotation
  (visibility)? @context
  "impl" @context
  (type_parameters)? @context
  (type_name
    (qualified_type_identifier) @context)
  "with" @context
  (function_identifier) @name
  (parameters)? @context.extra
  (return_type)? @context.extra) @item
