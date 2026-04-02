# Baseline-Leg Compare

- Query shelf size: `16`
- Top-k: `8`
- Branch note: Branch-local diagnostic artifact only. This compare does not alter the live bag path and should not be treated as promotive truth without explicit review.

## Leg Summary

| Leg | DB | Human-facing tops | Same top vs bag | Same origin vs bag |
| --- | --- | --- | --- | --- |
| `fts` | `cold_anatomy_reference_probe_073_semgrav_det_steep.db` | `10/16` | `5/16` | `6/16` |
| `ann_sentence` | `cold_anatomy_reference_probe_069_semgrav_st_control.db` | `13/16` | `6/16` | `7/16` |
| `ann_deterministic` | `cold_anatomy_reference_probe_073_semgrav_det_steep.db` | `14/16` | `4/16` | `5/16` |
| `bag` | `cold_anatomy_reference_probe_073_semgrav_det_steep.db` | `15/16` | `16/16` | `16/16` |

## Difference Read

- FTS-only preserves exact lexical anchors well, but it only matches the bag top on `5/16` queries.
- Sentence-transformers ANN is the closest 'normal vector' leg here, matching the bag top on `6/16` queries.
- Deterministic ANN diverges more from the bag than sentence-transformers ANN (`4` vs `6` same-top hits), which suggests a shifted or specialized field rather than a conventional semantic neighborhood map.
- The bag's added value is anchor stability and readable evidence shaping; it lands a human-facing top item on `15/16` queries in this run.

## Top-Item Compare

| Query | FTS | ANN (ST) | ANN (Det) | Bag |
| --- | --- | --- | --- | --- |
| `lexical analysis` | `index.txt` `md_list_item` :: * 2. Lexical analysis | `lexical_analysis.txt` `md_heading` :: 2. Lexical analysis | `index.txt` `md_list_item` :: * 2. Lexical analysis | `index.txt` `md_list_item` :: * 2. |
| `encoding declarations` | `lexical_analysis.txt` `md_heading` :: 2.1.4. Encoding declarations | `lexical_analysis.txt` `md_heading` :: 2.1.4. Encoding declarations | `lexical_analysis.txt` `md_paragraph` :: The following example shows various indentation errors: | `lexical_analysis.txt` `md_heading` :: 2.1.4. Encoding declarations |
| `yield expressions` | `simple_stmts.txt` `md_paragraph` :: For full details of "yield" semantics, refer to the Yield expressions section. | `expressions.txt` `md_heading` :: 6.2.9. Yield expressions | `index.txt` `md_list_item` :: * 3.3. Special method names | `expressions.txt` `md_heading` :: 6.2.9. Yield expressions |
| `operator precedence` | `index.txt` `md_list_item` :: * 6.17. Operator precedence | `index.txt` `md_list_item` :: * 6.17. Operator precedence | `index.txt` `md_list_item` :: * 6.17. Operator precedence | `index.txt` `md_list_item` :: * 6.17. |
| `assignment expressions` | `executionmodel.txt` `md_list_item` :: * assignment expressions, | `executionmodel.txt` `md_list_item` :: * assignment expressions, | `index.txt` `md_list_item` :: * 6.12. Assignment expressions | `index.txt` `md_list_item` :: * 6.12. |
| `lambda expressions` | `expressions.txt` `fragment_of_md_code_block` :: " expression] expression ::= conditional_expression | lambda_expr Conditional expressions (sometimes called a "ternary operator") have the lowest priority of all Python operations. | `expressions.txt` `fragment_of_md_code_block` :: " expression] expression ::= conditional_expression | lambda_expr Conditional expressions (sometimes called a "ternary operator") have the lowest priority of all Python operations. | `expressions.txt` `fragment_of_md_code_block` :: " expression] expression ::= conditional_expression | lambda_expr Conditional expressions (sometimes called a "ternary operator") have the lowest priority of all Python operations. | `index.txt` `md_list_item` :: * 6.14. |
| `function definitions` | `executionmodel.txt` `md_list_item` :: * function definitions, | `executionmodel.txt` `md_list_item` :: * function definitions, | `index.txt` `md_list_item` :: * 8.7. Function definitions | `index.txt` `md_list_item` :: * 8.7. |
| `import statements` | `executionmodel.txt` `md_list_item` :: * "import" statements. | `executionmodel.txt` `md_list_item` :: * "import" statements. | `index.txt` `md_list_item` :: * 7. Simple statements | `executionmodel.txt` `md_list_item` :: * "import" statements. |
| `module imports` | `import.txt` `md_blockquote` :: >> import spam >> spam.foo <module 'spam.foo' from '/tmp/imports/spam/foo.py'> >> spam.Foo <class 'spam.foo.Foo'> | `simple_stmts.txt` `md_paragraph` :: "importlib.import_module()" is provided to support applications that determine dynamically the modules to be loaded. | `compound_stmts.txt` `md_heading` :: 8. Compound statements | `executionmodel.txt` `md_list_item` :: * "import" statements. |
| `resolution of names` | `executionmodel.txt` `md_heading` :: 4.2.2. Resolution of names | `executionmodel.txt` `md_heading` :: 4.2.2. Resolution of names | `simple_stmts.txt` `md_list_item` :: expression is evaluated. | `executionmodel.txt` `md_heading` :: 4.2.2. Resolution of names |
| `name lookup` | `datamodel.txt` `fragment_of_md_code_block` :: , "object.__getattribute__(self, name)". Note: This method may still be bypassed when looking up special methods as the result of implicit invocation via language syntax or built-i | `expressions.txt` `md_code_block` :: name ::= othername | `simple_stmts.txt` `md_list_item` :: * Otherwise: the name is bound to the object in the global namespace or the outer namespace determined by "nonlocal", respectively. | `executionmodel.txt` `md_heading` :: 4.2.2. Resolution of names |
| `eval input` | `toplevel_components.txt` `md_code_block` :: eval_input ::= expression_list NEWLINE* | `toplevel_components.txt` `md_paragraph` :: "eval()" is used for expression input. It ignores leading whitespace. The string argument to "eval()" must have the following form: | `datamodel.txt` `md_paragraph` :: The appropriate metaclass for a class definition is determined as follows: | `toplevel_components.txt` `md_heading` :: 9.4. Expression input |
| `interactive input` | `index.txt` `md_list_item` :: * 9.3. Interactive input | `toplevel_components.txt` `md_heading` :: 9.3. Interactive input | `import.txt` `md_list_item` :: * interactive prompt | `toplevel_components.txt` `md_heading` :: 9.3. Interactive input |
| `repl input` | `` `None` :: None | `simple_stmts.txt` `md_paragraph` :: In interactive mode, if the value is not "None", it is converted to a string using the built-in "repr()" function and the resulting string is written to standard output on a line b | `compound_stmts.txt` `md_code_block` :: if x < y < z: print(x); print(y); print(z) | `toplevel_components.txt` `md_heading` :: 9.3. Interactive input |
| `function calls` | `import.txt` `md_paragraph` :: Module loaders provide the critical function of loading: module execution. The import machinery calls the "importlib.abc.Loader.exec_module()" method with a single argument, the mo | `executionmodel.txt` `md_list_item` :: * function definitions, | `index.txt` `md_list_item` :: * 8.7. Function definitions | `expressions.txt` `fragment_of_md_code_block` :: | tests and identity tests | +-------------------------------------------------+---------------------------------------+ | "not x" | Boolean NOT | +-----------------------------... |
| `decorators` | `compound_stmts.txt` `fragment_of_md_code_block` :: Support for forward references within annotations by preserving annotations in a string form at runtime instead of eager evaluation. **PEP 318** - Decorators for Functions and Meth | `compound_stmts.txt` `fragment_of_md_code_block` :: for the decorator expressions are the same as for function decorators. The result is then bound to the class name. Changed in version 3.9: Classes may be decorated with any valid " | `index.txt` `md_list_item` :: * 2.3. Identifiers and keywords | `datamodel.txt` `md_paragraph` :: Below is a list of the types that are built into Python. |
