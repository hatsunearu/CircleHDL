top: [(_osnl (moddef | topdef) _osnl)*]


moddef: "def" _s "mod" _s STR _os functional_args _os moddef_body

moddef_body: _osnl "{" _osnl attr_pins* _osnl "}" _osnl

attr_pins: "attr" _s "pins" _os "(" _os NUM _os ")" pins_body

pins_body: _osnl "{" _osnl (pinname_stmt _snl)* "}" _osnl



topdef: "def" _s "top" _s STR _os functional_args _os topdef_body

topdef_body: _osnl "{" _osnl ( (decl_node | decl_mod | connection) _snl)* "}"

decl_node: "!node" _s STR
decl_mod: "!mod" _s STR _os "=" _os call_mod

connection: singular_port _os "--" [_os (double_port ) _os "--"]_os singular_port 

double_port: [ module_as_ports | "|" _osnl singular_port | double_port _os "--" _os double_port]

singular_port: ( mod_pin_numeric | mod_pin_full | node_literal )

module_as_ports: (mod_literal | call_mod)

call_mod: STR functional_args


mod_literal: STR
node_literal: STR


mod_pin_numeric: ( STR "#" STR )
mod_pin_full: (STR ":" STR)

functional_args: "(" [STR ("," _os STR)*] ")"
pinname_stmt: NUM _os ":" _os STR


// optional spaces
_os: (" "|"\t")*
_onl: ("\r" | "\n")*
_osnl: (" " | "\t" | "\r" | "\n")*
_snl: (_osnl "\n" _osnl)+
_s: " "+

STR: ("\\\""|/[^("|"\n"|\s|:|#|\|)]/)+




%import common.STRING_INNER 
%import common.SIGNED_NUMBER -> NUM
%import common.WS_INLINE
%import common.NEWLINE

