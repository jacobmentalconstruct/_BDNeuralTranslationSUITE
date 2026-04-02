# Baseline-Leg Shelf

- Query: `lambda expressions`
- Mode: `ann`
- DB: `C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\_analysis\reference_probe_069_semgrav_st_control\cold_anatomy_reference_probe_069_semgrav_st_control.db`
- Retrieval leg: ANN-only vector retrieval over occurrence vectors.
- Provider: `sentence-transformers`
- Model: `sentence-transformers/all-MiniLM-L6-v2`
- Summary: 8 cosine-ranked evidence items surfaced for "lambda expressions" across 4 groups. Top sources: simple_stmts.txt (4), expressions.txt (2), index.txt (1). Top node kinds: fragment_of_md_code_block (2), md_list_item (2), md_heading (2).

| Rank | Origin | Kind | Score | Snippet |
| --- | --- | --- | --- | --- |
| `1` | `expressions.txt` | `fragment_of_md_code_block` | `0.663377` | " expression] expression ::= conditional_expression | lambda_expr Conditional expressions (sometimes called a "ternary operator") have the lowest priority of all Python operations. |
| `2` | `simple_stmts.txt` | `md_list_item` | `0.555987` | expression is evaluated. |
| `3` | `index.txt` | `md_list_item` | `0.543281` | * 6.14. Lambdas |
| `4` | `lexical_analysis.txt` | `fragment_of_md_code_block` | `0.498946` | ersion field, introduced by an exclamation point "'!'" may follow. A format specifier may also be appended, introduced by a colon "':'". A replacement field ends with a closing cur |
| `5` | `simple_stmts.txt` | `md_heading` | `0.498837` | 7.1. Expression statements |
| `6` | `simple_stmts.txt` | `md_paragraph` | `0.493308` | An expression statement evaluates the expression list (which may be a single expression). |
| `7` | `expressions.txt` | `md_heading` | `0.486933` | 6. Expressions |
| `8` | `simple_stmts.txt` | `md_paragraph` | `0.464319` | If an expression list is present, it is evaluated, else "None" is substituted. |
