Yet Another Python Sproto Parser
--------------------------------

Introduction
============
[sproto](https://github.com/cloudwu/sproto) is a simple serialize library. I hoped that this parser will be complement to python-sproto, a python-binding library for sproto.
I've tried pypeg2, but I can't handle the nested struct situation, so I wrote my own version. This version simply use Top-down parser. The parser decides struct with one token look ahead.
