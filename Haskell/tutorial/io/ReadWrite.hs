module Main
  where
    
import System.IO
import Control.Exception

main = do
  hSetBuffering stdin LineBuffering
  mainLoop

mainLoop = do
  putStrLn "Would you like to [read] a file, [write] a file or [quit]?"
  command <- getLine
  case command of
    "quit"    -> return ()
    "read"    -> readCommand
    "write"   -> writeCommand
    cmd       -> do putStrLn ("I don't understand command " ++ cmd ++ "!")
                    mainLoop

readCommand = do
  putStrLn "Enter a file name to read:"
  filename <- getLine
  withFile 
    filename 
    ReadMode
    (\h -> do contents <- hGetContents h
              putStr contents)
  mainLoop

writeCommand = do
  putStrLn "Enter a file name to write:"
  filename <- getLine
  putStrLn "Enter text (dot on a line by itself to end):"
  contents <- getInputLines ""
  withFile
    filename
    WriteMode
    (\h -> do hPutStr h contents)
  mainLoop

getInputLines contents = do
  nextLine <- getLine
  case nextLine of
    "." -> return contents
    _   -> do getInputLines (contents ++ nextLine ++ "\n")
