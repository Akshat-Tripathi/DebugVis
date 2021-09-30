module Main where
import Parsing

main :: IO ()
main = do print (tokenise "\"hello\" \"there\" 'g'eneral kenobi'")