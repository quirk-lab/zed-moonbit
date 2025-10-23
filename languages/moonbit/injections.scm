((comment) @injection.content
  (#set! injection.language "comment"))

; Inject external language when:
;
;   extern "c" fn foo() =
;     #|void main() {}
;
(function_definition
  (external_linkage
    "extern" @context
    (string_literal
      (string_fragment) @injection.language))
  "fn"
  (external_source
    (multiline_string_literal
      (multiline_string_fragment
        (multiline_string_content) @injection.content
        (#set! injection.combined)))))

; Inject WebAssembly Text Format (WAT) when:
;
;   extern "wasm" fn foo() =
;     #|(func (param i32))
;
(function_definition
  (external_linkage
    "extern" @context
    (string_literal
      (string_fragment) @lang
      (#eq! @lang "wasm")
      (#set! injection.language "wat")))
  "fn"
  (external_source
    (multiline_string_literal
      (multiline_string_fragment
        (multiline_string_content) @injection.content
        (#set! injection.combined)))))
