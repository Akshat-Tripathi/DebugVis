module Parsing where

import Data.Maybe

data Token = Ident String | DoubleQuote | SingleQuote | OpenParen | ClosedParen deriving (Show)

data SExp = Atom Token | Exp [SExp]

tokenise :: String -> [Token]
tokenise s = tokenise' s ""
  where
    tokenise' :: String -> String -> [Token]
    tokenise' (c:cs) s
        | c == '('  = addIfNotEmpty s (OpenParen : tokenise' cs "")
        | c == ')'  = addIfNotEmpty s (ClosedParen : tokenise' cs "")
        | c == '"'  = addIfNotEmpty s (DoubleQuote : tokenise' cs "")
        | c == '\'' = addIfNotEmpty s (SingleQuote : tokenise' cs "")
        | c == ' ' = addIfNotEmpty s (tokenise' cs "")
        | otherwise = tokenise' cs (c:s)
        where
            addIfNotEmpty "" ts = ts
            addIfNotEmpty s ts = Ident (reverse s) : ts 
    tokenise' [] s = []